from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Usuario(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Paises(db.Model):
    __tablename__ = 'paises'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.name

class Provincia(db.Model):
    __tablename__ = 'provincia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.Integer, db.ForeignKey('paises.id'), nullable=False, default=True)

    pais_obj = db.relationship('Paises')

    def __str__(self):
        return self.name
    
class Localidad(db.Model):
    __tablename__ = 'localidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False, default=True)

    prov_obj = db.relationship('Provincia')

    def __str__(self):
        return self.name    

class Personas(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    numtel = db.Column(db.Integer, nullable=False)
    localidad = db.Column(db.Integer, db.ForeignKey('localidad.id'), nullable=False)
    domicilio = db.Column(db.String(100), nullable=False)
    f_nac = db.Column(db.Date, nullable=False)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


