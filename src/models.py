from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Drink(db.Model):
    __tablename__ = "drink"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(380), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __init__(self, name, precio):
        self.name = name
        self.precio = precio


    def __repr__(self):
        return f'<Drink {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mark": self.precio,
        }