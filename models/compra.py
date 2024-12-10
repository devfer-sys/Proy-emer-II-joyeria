# models/compra.py
from database import db

class Compra(db.Model):
    __tablename__ = 'compras'
    id_com = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id_cli'), nullable=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id_pro'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id_emp'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    
    # Campos adicionales para evitar eliminación de datos
    nombre_cliente = db.Column(db.String(100), nullable=False)  # Nuevo campo
    nombre_producto = db.Column(db.String(100), nullable=False)  # Nuevo campo

    # Relaciones
    cliente = db.relationship('Cliente', back_populates='compras')
    producto = db.relationship('Producto', back_populates='compras')
    ventas = db.relationship('Venta', back_populates='compra', cascade='save-update, merge')
    empleado = db.relationship('Empleado', back_populates='compras')

    def __init__(self, cliente_id, producto_id, empleado_id, cantidad, fecha, nombre_cliente, nombre_producto):
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.empleado_id = empleado_id
        self.cantidad = cantidad
        self.fecha = fecha
        self.nombre_cliente = nombre_cliente
        self.nombre_producto = nombre_producto

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Compra.query.all()

    @staticmethod
    def get_by_id(id_com):
        return Compra.query.get(id_com)

    def update(self, cliente_id=None, producto_id=None, cantidad=None, fecha=None, nombre_cliente=None, nombre_producto=None):
        if cliente_id is not None:
            self.cliente_id = cliente_id
        if producto_id is not None:
            self.producto_id = producto_id
        if cantidad is not None:
            self.cantidad = cantidad
        if fecha is not None:
            self.fecha = fecha
        if nombre_cliente is not None:
            self.nombre_cliente = nombre_cliente
        if nombre_producto is not None:
            self.nombre_producto = nombre_producto
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
