# controllers/producto.py
from flask import request, redirect, url_for, Blueprint, flash
from utils.utils import login_required
from models.producto import Producto
from views import producto_view
from models.compra import Compra
from database import db

producto_bp = Blueprint('producto', __name__, url_prefix="/productos")

@producto_bp.route("/")
@login_required
def index():
    productos = Producto.get_all()
    return producto_view.list(productos)

@producto_bp.route("/registrar", methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        stock = int(request.form['stock'])

        producto = Producto(nombre, precio, stock)
        producto.save()
        return redirect(url_for('producto.index'))

    return producto_view.registrar()

@producto_bp.route("/editar/<int:id_pro>", methods=['GET', 'POST'])
@login_required
def editar(id_pro):
    producto = Producto.get_by_id(id_pro)
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        stock = int(request.form['stock'])

        producto.update(nombre=nombre, precio=precio, stock=stock)
        return redirect(url_for('producto.index'))
    
    return producto_view.editar(producto)

# Ruta para eliminar un producto
@producto_bp.route("/delete/<int:id_pro>")
def delete(id_pro):
    producto = Producto.get_by_id(id_pro)
    if not producto:
        flash("Cliente no encontrado", "error")
        return redirect(url_for('producto.index'))

    # Actualizar las compras relacionadas, asignando un producto por defecto
    compras = Compra.query.filter_by(producto_id=id_pro).all()
    for compra in compras:
        compra.producto_id = 0  # Asigna un valor por defecto o un producto genérico
        db.session.add(compra)
    
    db.session.commit()

    # Ahora puedes eliminar el producto
    producto.delete()

    flash("Producto eliminado exitosamente", "success")
    return redirect(url_for('producto.index'))