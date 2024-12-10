from flask import Blueprint, request, redirect, url_for, flash, make_response
from models.venta import Venta
from views import venta_view
from utils.utils import login_required
from fpdf import FPDF

venta_bp = Blueprint('venta', __name__, url_prefix="/ventas")

# Ruta para listar todas las ventas
@venta_bp.route("/", methods=['GET'])
@login_required
def index():
    filtro = request.args.get('filtro')
    ventas = Venta.get_all(filtro=filtro)
    
    # Calcular el total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas if venta.compra_id is not None)
    
    return venta_view.list(ventas, total_ingresos=total_ingresos)

# Ruta para listar solo ventas con compra_id = None (Reembolsos)
@venta_bp.route("/reembolsos", methods=['GET'])
@login_required
def reembolsos():
    ventas = Venta.get_all(filtro="reembolsos")
    
    # Calcular el total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas if venta.compra_id is not None)
    
    return venta_view.list(ventas, total_ingresos=total_ingresos)

# Ruta para listar solo ventas exitosas (compra_id no es None)
@venta_bp.route("/exitosos", methods=['GET'])
@login_required
def exitoso():
    ventas = Venta.get_all(filtro="exitoso")
    
    # Calcular el total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas if venta.compra_id is not None)
    
    return venta_view.list(ventas, total_ingresos=total_ingresos)

# Ruta para listar solo ventas de un trabajador específico
@venta_bp.route("/trabajador/<nombre_empleado>", methods=['GET'])
@login_required
def ventas_trabajador(nombre_empleado):
    ventas = Venta.get_by_trabajador(nombre_empleado)
    
    # Calcular el total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas if venta.compra_id is not None)
    
    return venta_view.list(ventas, total_ingresos=total_ingresos)

# Ruta para listar por precio más alto
@venta_bp.route("/precio_alto", methods=['GET'])
@login_required
def precio_alto():
    ventas = Venta.get_all(filtro="precio_alto")
    
    # Calcular el total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas if venta.compra_id is not None)
    
    return venta_view.list(ventas, total_ingresos=total_ingresos)

# Ruta para listar por cantidad más alta
@venta_bp.route("/cantidad_alta", methods=['GET'])
@login_required
def cantidad_alta():
    ventas = Venta.get_all(filtro="cantidad_alta")
    
    # Calcular el total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas if venta.compra_id is not None)
    
    return venta_view.list(ventas, total_ingresos=total_ingresos)

# Ruta para listar por ingresos más altos
@venta_bp.route("/ingresos_altos", methods=['GET'])
@login_required
def ingresos_altos():
    ventas = Venta.get_all(filtro="ingresos_altos")
    
    # Calcular el total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas if venta.compra_id is not None)
    
    return venta_view.list(ventas, total_ingresos=total_ingresos)

# Ruta para generar el reporte de todas las ventas en PDF con orientación horizontal
@venta_bp.route("/reporte/pdf", methods=['GET'])
@login_required
def reporte_pdf():
    ventas = Venta.query.all()  # Obtener todas las ventas
    if not ventas:
        flash("No hay ventas registradas", "error")
        return redirect(url_for('venta.index'))
    
    pdf = FPDF('L', 'mm', 'A4')  # 'L' para Landscape (horizontal)
    pdf.add_page()

    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Ventas Joyeria-Luxor', ln=True, align='C')
    pdf.ln(10)

    # Encabezado de la tabla
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(25, 10, 'Nro. Venta', border=1, align='C')
    pdf.cell(30, 10, 'Proceso', border=1, align='C')  
    pdf.cell(30, 10, 'Producto', border=1, align='C')
    pdf.cell(40, 10, 'Cantidad Vendida', border=1, align='C')
    pdf.cell(30, 10, 'Precio', border=1, align='C')
    pdf.cell(30, 10, 'Empleado', border=1, align='C')
    pdf.cell(30, 10, 'Fecha', border=1, align='C')
    pdf.cell(30, 10, 'Ingresos', border=1, align='C')
    pdf.ln()

    # Información de las ventas
    pdf.set_font('Arial', '', 12)
    for venta in ventas:
        proceso = "Reembolso" if venta.compra_id is None else "Exitoso"  # Condición para proceso
        pdf.cell(25, 10, str(venta.id_ven), border=1, align='C')
        pdf.cell(30, 10, proceso, border=1, align='C')  
        pdf.cell(30, 10, venta.nombre_producto, border=1, align='C')
        pdf.cell(40, 10, str(venta.cant_vend), border=1, align='C')
        pdf.cell(30, 10, f'${venta.precio_producto:.2f}', border=1, align='C')
        pdf.cell(30, 10, venta.nombre_empleado, border=1, align='C')
        pdf.cell(30, 10, venta.fecha_venta.strftime('%Y-%m-%d'), border=1, align='C')
        pdf.cell(30, 10, f'${venta.ingresos:.2f}', border=1, align='C')
        pdf.ln()

    # Total de ingresos
    total_ingresos = sum(venta.ingresos for venta in ventas)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(215, 10, 'Ingreso Total:', border=1, align='C')
    pdf.cell(30, 10, f'${total_ingresos:.2f}', border=1, align='C')

    # Crear el archivo PDF y devolverlo
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_ventas.pdf'
    return response



