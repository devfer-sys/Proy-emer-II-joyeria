from flask import Blueprint, render_template
from models.producto import Producto

# Crear el Blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

# Ruta para la página principal
@main_bp.route("/")
def index():
    # Obtener todos los productos
    productos = Producto.get_all()

    # Renderizar la plantilla y pasar los productos
    return render_template("index.html", productos=productos)

