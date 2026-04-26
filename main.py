from fastapi import FastAPI, Depends
from routes.user import router as user_router
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.user import Submission
from schemas.user import UserCreate
from imc import calcul_IMC, resultat_IMC, afficher_resultats
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt


#création des tables
Base.metadata.create_all(bind = engine)

app =  FastAPI()

#Dépendance de la BD

def get_db():
	db = SessionLocal()
	try:
		yield db

	finally:
		db.close()	 

app.include_router(user_router)

@app.post("/submit")
def submit_data(data: UserCreate, db: Session = Depends(get_db)):
	new_entry = Submission(
		name = data.name,
		poids = data.poids,
		taille = data.taille,
		sexe = data.sexe,
		age = data.age,
		)
	db.add(new_entry)
	db.commit()
	db.refresh(new_entry)

	return{
	"message": "Données enregistrées avec succès",
	"id": new_entry.id
	}

df = pd.read_csv("data.csv")
print("COLONNES :",df.columns)
print(df.head)

df["IMC"] = df["poids"]/((df["taille"]/100)**2)
df["categorie"] = df["IMC"].apply(resultat_IMC)
afficher_resultats(df)

plt.hist(df["IMC"] , bins=5)
plt.title("Distribution des IMC")
plt.xlabel("IMC")
plt.ylabel("Nombre de personnes")

sns.countplot(x="categorie", data=df)
plt.title("Repartition des categories IMC ")

plt.scatter(df["age"], df["IMC"])
plt.title("IMC selon l'âge")
plt.xlabel("Âge")
plt.ylabel("IMC")

plt.show()

