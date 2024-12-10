from database import db

class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    # Definición de las columnas de la tabla
    id_emp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(200))

    compras = db.relationship('Compra',back_populates='empleado')

    # Constructor para inicializar los valores
    def __init__(self, nombre, apellidos, cargo, contrasena, estado):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.contrasena = contrasena
        self.estado = estado

    # Método de instancia para verificar la contraseña (comparación directa)
    def verify_password(self, contrasena):
        return self.contrasena == contrasena  # Comparación directa

    # Método para guardar el empleado en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Empleado.query.all()
    
    @staticmethod
    def get_by_id(id_emp):
        return Empleado.query.get(id_emp)
    
    def update(self, nombre=None, apellidos=None, cargo=None, contrasena=None, estado=None):
        if nombre and apellidos and cargo and contrasena and estado:
            self.nombre = nombre
            self.apellidos = apellidos
            self.cargo = cargo
            self.contrasena = contrasena
            self.estado = estado
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

