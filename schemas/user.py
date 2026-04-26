from pydantic import BaseModel

class UserCreate(BaseModel):
	poids: float
	taille: float
	sexe : str
	age : int
	message: str