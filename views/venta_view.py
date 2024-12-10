from flask import render_template

# En el archivo views/venta_view.py o en el lugar donde se renderiza la vista
def list(ventas, total_ingresos):
    return render_template('ventas/index.html', ventas=ventas, total_ingresos=total_ingresos)

