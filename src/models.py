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

    @classmethod
    def save(cls, name, price):
        new_drink = cls(precio=price, name=name)
        db.session.add(new_drink)
        db.session.commit()
        return new_drink


        

    def __repr__(self):
        return f'<Drink {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mark": self.precio,
        }
    
# Many to Many only
association_table_orders = db.Table(
    "association_table_orders",
    db.metadata,
    db.Column("orders", db.ForeignKey("orders.id")),
    db.Column("drink", db.ForeignKey("drink.id")),
)
    
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    drinks = db.relationship(Drink, secondary=association_table_orders)

    def get_total(self):
        total = 0
        for drink in self.drinks:
            total += drink.precio
        return total
    
    def serialize(self):
        return {
            "id": self.id,
            "drinks": [ drink.serialize() for drink in self.drinks ],
            "total": f"$ {self.get_total()}"
        }