# controllers/compra.py
from flask import request, redirect, url_for, Blueprint, flash, make_response, session
from datetime import datetime
from fpdf import FPDF
from models.compra import Compra
from models.producto import Producto
from models.cliente import Cliente
from utils.utils import login_required
from views import compra_view
from models.empleado import Empleado
from models.venta import Venta

compra_bp = Blueprint('compra', __name__, url_prefix="/compras")

@compra_bp.route("/")
@login_required
def index():
    compras = Compra.get_all()
    return compra_view.list(compras)

@compra_bp.route("/registrar", methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        fecha_str = request.form['fecha']

        if not cliente_id or not producto_id or not cantidad or not fecha_str:
            flash("Todos los campos son requeridos", "error")
            return redirect(url_for('compra.registrar'))

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Fecha en formato incorrecto. Use AAAA-MM-DD", "error")
            return redirect(url_for('compra.registrar'))

        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado", "error")
            return redirect(url_for('compra.registrar'))

        if producto.stock < cantidad:
            flash("Stock insuficiente para realizar la compra", "error")
            return redirect(url_for('compra.registrar'))

        # Obtener el cliente y sus datos
        cliente = Cliente.get_by_id(cliente_id)
        if not cliente:
            flash("Cliente no encontrado", "error")
            return redirect(url_for('compra.registrar'))

        # Obtener el ID del empleado logueado
        empleado_id = session.get('empleado_id')
        if not empleado_id:
            flash("No se encontró el empleado en sesión", "error")
            return redirect(url_for('compra.registrar'))
        
        empleado = Empleado.get_by_id(empleado_id)  
        if not empleado:
            flash("Empleado no encontrado", "error")
            return redirect(url_for('compra.registrar'))

        # Crear y guardar la compra con los datos adicionales
        compra = Compra(
            cliente_id=cliente_id,
            producto_id=producto_id,
            empleado_id=empleado_id,
            cantidad=cantidad,
            fecha=fecha,
            nombre_cliente=cliente.nombre_completo,  # Guardamos el nombre del cliente
            nombre_producto=producto.nombre         # Guardamos el nombre del producto
        )
        compra.save()

        venta = Venta(
            compra_id=compra.id_com,
            producto_id=producto_id,
            cant_vend=cantidad,
            ingresos=producto.precio * cantidad,
            nombre_cliente=cliente.nombre_completo,  # Nombre del cliente
            nombre_producto=producto.nombre,         # Nombre del producto
            precio_producto=producto.precio,         # Precio del producto
            nombre_empleado=empleado.nombre,  # Nombre del empleado
            fecha_venta=fecha  # Fecha de la venta
        )
        venta.save()
        # Actualizar el stock del producto
        producto.update(stock=producto.stock - cantidad)

        flash("Compra registrada exitosamente", "success")
        return redirect(url_for('compra.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return compra_view.registrar(clientes, productos)

# controllers/compra.py
@compra_bp.route("/editar/<int:id_com>", methods=['GET', 'POST'])
@login_required
def editar(id_com):
    compra = Compra.get_by_id(id_com)
    if not compra:
        flash("Compra no encontrada", "error")
        return redirect(url_for('compra.index'))

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        fecha_str = request.form['fecha']

        if not cliente_id or not producto_id or not cantidad or not fecha_str:
            flash("Todos los campos son requeridos", "error")
            return redirect(url_for('compra.editar', id_com=id_com))

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Fecha en formato incorrecto. Use YYYY-MM-DD", "error")
            return redirect(url_for('compra.editar', id_com=id_com))

        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado", "error")
            return redirect(url_for('compra.editar', id_com=id_com))

        # Restaurar el stock anterior
        producto.update(stock=producto.stock + compra.cantidad)

        if producto.stock < cantidad:
            flash("Stock insuficiente para realizar la compra", "error")
            return redirect(url_for('compra.editar', id_com=id_com))

        # Actualizar el stock con la nueva cantidad
        producto.update(stock=producto.stock - cantidad)

        # Actualizar el cliente y el producto en los campos fijos
        cliente = Cliente.get_by_id(cliente_id)
        if cliente:
            nombre_cliente = cliente.nombre_completo
        else:
            nombre_cliente = compra.nombre_cliente  # Mantener el nombre si no se encuentra el cliente

        producto = Producto.get_by_id(producto_id)
        if producto:
            nombre_producto = producto.nombre
        else:
            nombre_producto = compra.nombre_producto  # Mantener el nombre si no se encuentra el producto

        # Actualizar la compra con los nuevos valores
        compra.update(cliente_id=cliente_id, producto_id=producto_id, cantidad=cantidad, fecha=fecha, 
                      nombre_cliente=nombre_cliente, nombre_producto=nombre_producto)

        flash("Compra actualizada exitosamente", "success")
        return redirect(url_for('compra.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return compra_view.editar(compra, clientes, productos)

@compra_bp.route("/delete/<int:id_com>")
@login_required  # Protegiendo esta ruta con el decorador
def delete(id_com):
    compra = Compra.get_by_id(id_com)
    if not compra:
        flash("Compra no encontrada", "error")
        return redirect(url_for('compra.index'))

    # Recuperar el producto asociado a la compra
    producto = Producto.get_by_id(compra.producto_id)
    if producto:
        # Restaurar el stock del producto
        producto.update(stock=producto.stock + compra.cantidad)

    # Eliminar la compra
    compra.delete()
    flash("Compra eliminada exitosamente", "success")
    return redirect(url_for('compra.index'))


@compra_bp.route("/facturar/<int:id_com>/pdf", methods=['GET'])
@login_required
def facturar_pdf(id_com):
    compra = Compra.get_by_id(id_com)
    if not compra:
        flash("Compra no encontrada", "error")
        return redirect(url_for('compra.index'))
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Factura de Compra', ln=True, align='C')
    pdf.ln(10)

    # Información de la compra
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Factura ID: {compra.id_com}', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Fecha: {compra.fecha.strftime("%Y-%m-%d")}', ln=True)
    pdf.ln(5)

    # Información del cliente
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Información del Cliente:', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Nombre: {compra.cliente.nombre_completo}', ln=True)
    pdf.cell(0, 10, f'Correo: {compra.cliente.email}', ln=True)
    pdf.cell(0, 10, f'Teléfono: {compra.cliente.telefono}', ln=True)
    pdf.ln(5)

    # Información del producto
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Detalles del Producto:', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Producto: {compra.producto.nombre}', ln=True)
    pdf.cell(0, 10, f'Cantidad: {compra.cantidad}', ln=True)
    pdf.cell(0, 10, f'Precio Unitario: ${compra.producto.precio:.2f}', ln=True)
    pdf.ln(5)

    # Total
    total = compra.cantidad * compra.producto.precio
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Total: ${total:.2f}', ln=True)

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=factura_{compra.id_com}.pdf'  # Cambiar a 'attachment'
    return response

