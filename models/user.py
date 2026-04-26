from sqlalchemy import Column,Integer,String,Float
from database import Base


class Submission(Base):

	__tablename__ = "submissions"

	id = Column(Integer, primary_key= True, index = True) 
	poids = Column(Float, index = True)
	taille = Column(Float, index = True)
	sexe = Column(String, index = True)
	age = Column(Integer, index = True)

	message = Column(String)
