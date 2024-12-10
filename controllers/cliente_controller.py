from flask import request, redirect, url_for, Blueprint, flash
from models.cliente import Cliente
from utils.utils import login_required
from views import cliente_view
from database import db
from models.compra import Compra

cliente_bp = Blueprint('cliente', __name__, url_prefix="/clientes")

# Ruta para listar todos los clientes
@cliente_bp.route("/")
@login_required
def index():
    clientes = Cliente.get_all()  # Obtener todos los clientes desde la base de datos
    return cliente_view.list(clientes)

# Ruta para registrar un cliente
@cliente_bp.route("/registrar", methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        estado = request.form.get('estado', 'Activo')  # Establecer 'Activo' por defecto
        email = request.form['email']
        telefono = request.form['telefono']

        # Validaciones básicas antes de guardar
        if not nombre_completo or not email or not telefono:
            flash("Todos los campos son requeridos", "error")
            return redirect(url_for('cliente.registrar'))

        cliente = Cliente(nombre_completo, estado, email, telefono)
        cliente.save()  # Guardar el nuevo cliente en la base de datos
        flash("Cliente registrado exitosamente", "success")
        return redirect(url_for('cliente.index'))

    return cliente_view.registrar()

# Ruta para editar un cliente
@cliente_bp.route("/editar/<int:id_cli>", methods=['GET', 'POST'])
@login_required
def editar(id_cli):
    cliente = Cliente.get_by_id(id_cli)
    if not cliente:
        flash("Cliente no encontrado", "error")
        return redirect(url_for('cliente.index'))

    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        estado = request.form['estado']
        email = request.form['email']
        telefono = request.form['telefono']

        # Validaciones básicas antes de actualizar
        if not nombre_completo or not estado or not email or not telefono:
            flash("Todos los campos son requeridos", "error")
            return redirect(url_for('cliente.editar', id_cli=id_cli))

        cliente.update(nombre_completo=nombre_completo, estado=estado, email=email, telefono=telefono)
        flash("Cliente actualizado exitosamente", "success")
        return redirect(url_for('cliente.index'))

    return cliente_view.editar(cliente)

# Ruta para eliminar un cliente
@cliente_bp.route("/delete/<int:id_cli>")
def delete(id_cli):
    cliente = Cliente.get_by_id(id_cli)
    if not cliente:
        flash("Cliente no encontrado", "error")
        return redirect(url_for('cliente.index'))

    # Actualizar las compras relacionadas, asignando un cliente por defecto
    compras = Compra.query.filter_by(cliente_id=id_cli).all()
    for compra in compras:
        compra.cliente_id = 0  # Asigna un valor por defecto o un cliente genérico
        db.session.add(compra)
    
    db.session.commit()

    # Ahora puedes eliminar el cliente
    cliente.delete()

    flash("Cliente eliminado exitosamente", "success")
    return redirect(url_for('cliente.index'))



