from database import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cli = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    telefono = db.Column(db.Integer)

    compras = db.relationship('Compra', back_populates='cliente', cascade="all, delete-orphan")

    def __init__(self, nombre_completo, estado, email, telefono):
        self.nombre_completo = nombre_completo
        self.estado = estado
        self.email = email
        self.telefono = telefono



    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cliente.query.all()
    
    @staticmethod
    def get_by_id(id_cli):
        return Cliente.query.get(id_cli)
    
    def update(self,nombre_completo=None,estado=None,email=None,telefono=None):
        if nombre_completo:
            self.nombre_completo = nombre_completo
        if estado:
            self.estado = estado
        if email:
            self.email = email
        if telefono:
            self.telefono = telefono
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        