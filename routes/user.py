from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import Submission
from schemas.user import UserCreate


router = APIRouter()

#Dépendance de la BD

def get_db():
	db = SessionLocal()
	try:
		yield db

	finally:
		db.close()

@router.post("/submit")

def submit_data(data: UserCreate, db: Session = Depends(get_db)):
	new_entry = Submission(
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

@router.get("/Submissions")

def get_submissions(id: int, db: Session = Depends(get_db)):
	data = db.query(Submission).all()

	return data

@router.get("/Submission/{id}")

def get_submission(id: int, db: Session = Depends(get_db)):
	data = db.query(Submission).filter(Submission.id == id).first()

	return data

@router.delete("/Submission/{id}")

def delete_submission(id: int, db: Session = Depends(get_db)):
	data = db.query(Submission).filter(Submission.id == id).first() 
	if data:
		db.delete(data)
		db.commit()
		return{"message": "Suppression Reussite"}

	return {"erreur": "Donnée non trouvée"}

@router.put("/submission/{id}")

def update_submission(id: int, updated: UserCreate, db: Session = Depends(get_db)):
	data = db.query(Submission).filter(Submission.id == id).first() 
	if data:
		data.poids = updated.poids
		data.taille = updated.taille
		data.sexe = updated.sexe
		data.age = updated.age


		db.commit()
		return{"message": "Mise à jour Reussite"}

	return {"erreur": "Donnée non trouvée"}

