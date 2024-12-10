from flask import Flask

from database import db
from controllers import cliente_controller, producto_controller, venta_controller, compra_controller, main_controller, empleado_controller
from insert import insertar_empleados 

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///joyeria.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key"  # Asegúrate de tener una clave secreta para sesiones

# Inicializar la base de datos
db.init_app(app)

# Registro de blueprints
app.register_blueprint(main_controller.main_bp)
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(producto_controller.producto_bp)
app.register_blueprint(venta_controller.venta_bp)
app.register_blueprint(compra_controller.compra_bp)
app.register_blueprint(empleado_controller.empleado_bp)

# Crear la base de datos si no existe
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
        insertar_empleados(app)  
    app.run(host='0.0.0.0', port=5000, debug=True)

