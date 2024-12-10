# models/venta.py
from database import db

class Venta(db.Model):
    __tablename__ = 'ventas'

    id_ven = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id_com', ondelete='SET NULL'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id_pro'), nullable=False)
    cant_vend = db.Column(db.Integer, nullable=False)
    ingresos = db.Column(db.Integer, nullable=False)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    nombre_producto = db.Column(db.String(100), nullable=False)
    precio_producto = db.Column(db.Float, nullable=False)
    nombre_empleado = db.Column(db.String(100), nullable=False)
    fecha_venta = db.Column(db.DateTime, nullable=False)

    compra = db.relationship('Compra', back_populates='ventas')

    def __init__(self, compra_id, producto_id, cant_vend, ingresos, nombre_cliente, nombre_producto, precio_producto, nombre_empleado, fecha_venta):
        self.compra_id = compra_id
        self.producto_id = producto_id
        self.cant_vend = cant_vend
        self.ingresos = ingresos
        self.nombre_cliente = nombre_cliente
        self.nombre_producto = nombre_producto
        self.precio_producto = precio_producto
        self.nombre_empleado = nombre_empleado
        self.fecha_venta = fecha_venta

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(filtro=None):
        if filtro == "reembolsos":
            return Venta.query.filter(Venta.compra_id == None).all()
        elif filtro == "exitoso":
            return Venta.query.filter(Venta.compra_id != None).all()  # Ventas exitosas
        elif filtro == "precio_alto":
            return Venta.query.order_by(Venta.precio_producto.desc()).all()
        elif filtro == "cantidad_alta":
            return Venta.query.order_by(Venta.cant_vend.desc()).all()
        elif filtro == "ingresos_altos":
            return Venta.query.order_by(Venta.ingresos.desc()).all()
        else:
            return Venta.query.all()

    @staticmethod
    def get_by_trabajador(nombre_empleado):
        return Venta.query.filter(Venta.nombre_empleado == nombre_empleado).all()

    @staticmethod
    def get_by_id(id_ven):
        return Venta.query.get(id_ven)

    def update(self, compra_id=None, producto_id=None, cant_vend=None, ingresos=None, nombre_cliente=None, nombre_producto=None, precio_producto=None, nombre_empleado=None, fecha_venta=None):
        if compra_id is not None:
            self.compra_id = compra_id
        if producto_id is not None:
            self.producto_id = producto_id
        if cant_vend is not None:
            self.cant_vend = cant_vend
        if ingresos is not None:
            self.ingresos = ingresos
        if nombre_cliente is not None:
            self.nombre_cliente = nombre_cliente
        if nombre_producto is not None:
            self.nombre_producto = nombre_producto
        if precio_producto is not None:
            self.precio_producto = precio_producto
        if nombre_empleado is not None:
            self.nombre_empleado = nombre_empleado
        if fecha_venta is not None:
            self.fecha_venta = fecha_venta
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
