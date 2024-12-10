from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from models.empleado import Empleado
from utils.utils import login_required
from views import empleado_view

empleado_bp = Blueprint('empleado', __name__, url_prefix='/empleados')

@empleado_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de autenticación
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        empleado = Empleado.query.filter_by(nombre=nombre).first()

        if empleado and empleado.verify_password(contrasena):  # Comparación de contraseña
            # Verificación del estado del empleado
            if empleado.estado == 'Activo':
                session['empleado_id'] = empleado.id_emp
                session['empleado_nombre'] = empleado.nombre
                session['empleado_cargo'] = empleado.cargo  # Guardar el cargo en la sesión
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Tu cuenta está inactiva. Por favor, contacta con el administrador.', 'danger')
        else:
            flash('Credenciales incorrectas, intenta de nuevo', 'danger')

    return render_template('login.html')


@empleado_bp.route('/logout')
def logout():
    session.pop('empleado_id', None)
    session.pop('empleado_nombre', None)
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('main.index'))





# Ruta para registrar un empleado
@empleado_bp.route("/registrar", methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        cargo = request.form['cargo']
        contrasena = request.form['contrasena']
        estado = request.form.get('estado', 'Activo')

        # Validaciones básicas antes de guardar
        if not nombre or not apellidos or not cargo or not contrasena:
            flash("Todos los campos son requeridos", "error")
            return redirect(url_for('empleado.registrar'))

        empleado = Empleado(nombre, apellidos, cargo, contrasena, estado)
        empleado.save()  # Guardar el nuevo empleado en la base de datos
        flash("Empleado registrado exitosamente", "success")
        return redirect(url_for('empleado.index'))

    return empleado_view.registrar()


# Ruta para editar un empleado
@empleado_bp.route("/editar/<int:id_emp>", methods=['GET', 'POST'])
@login_required
def editar(id_emp):
    empleado = Empleado.get_by_id(id_emp)
    if not empleado:
        flash("empleado no encontrado", "error")
        return redirect(url_for('empleado.index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        cargo = request.form['cargo']
        contrasena = request.form['contrasena']
        estado = request.form['estado']

        # Validaciones básicas antes de actualizar
        if not nombre or not apellidos or not cargo or not contrasena or not estado:
            flash("Todos los campos son requeridos", "error")
            return redirect(url_for('empleado.editar', id_emp=id_emp))

        empleado.update(nombre=nombre, apellidos=apellidos, cargo=cargo, contrasena=contrasena,estado=estado)
        flash("empleado actualizado exitosamente", "success")
        return redirect(url_for('empleado.index'))

    return empleado_view.editar(empleado)


# Ruta para eliminar un empleado
@empleado_bp.route("/delete/<int:id_emp>")
@login_required
def delete(id_emp):
    empleado = Empleado.get_by_id(id_emp)
    if not empleado:
        flash("empleado no encontrado", "error")
        return redirect(url_for('empleado.index'))

    empleado.delete()  # Eliminar el empleado de la base de datos
    flash("empleado eliminado exitosamente", "success")
    return redirect(url_for('empleado.index'))


@empleado_bp.route('/')
@login_required
def index():
    empleados = Empleado.get_all()  # Obtiene la lista de empleados desde el modelo
    return empleado_view.list(empleados)  # Renderiza la vista con los empleados
