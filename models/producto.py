# models/producto.py
from database import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id_pro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    disponibilidad = db.Column(db.String(50), nullable=False)

    # Relaciones bidireccionales con Compra y Venta
    compras = db.relationship('Compra', back_populates='producto', cascade='all, delete-orphan')

    def __init__(self, nombre, precio, stock, disponibilidad=None):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.disponibilidad = disponibilidad if disponibilidad else ("Disponible" if stock > 0 else "No Disponible")

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        return Producto.query.all()

    @staticmethod
    def get_by_id(id_pro):
        return Producto.query.get(id_pro)

    def update(self, nombre=None, precio=None, stock=None):
        if nombre is not None:
            self.nombre = nombre
        if precio is not None:
            self.precio = precio
        if stock is not None:
            self.stock = stock
            self.disponibilidad = "Disponible" if stock > 0 else "No Disponible"
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Producto(id_pro={self.id_pro}, nombre='{self.nombre}', precio={self.precio}, stock={self.stock}, disponibilidad='{self.disponibilidad}')>"
