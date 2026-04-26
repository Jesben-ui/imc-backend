def calcul_IMC(poids, taille):
	taille /=100
	return poids/(taille*taille)

def resultat_IMC(imc):
	if imc < 18.5:
		return"Maigre"
	elif imc < 25:
		return"Normal"
	elif imc < 30:
	    return"Surpoids"	
	else:
	   return"Obèse" 
   

def afficher_resultats(df):
	print("=== DONNÉES ===")
	print(df)

	print("\n=== STATISTIQUES IMC ===")
	print(df["IMC"].describe())

	print("\n === CATEGORIES ===")
	print(df["categorie"].value_counts())