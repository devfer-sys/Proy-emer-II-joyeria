from flask import render_template


def list(empleados):
    return render_template('empleados/index.html', empleados = empleados)


def registrar():
    return render_template('empleados/registrar.html')


def editar(empleado):
    return render_template('empleados/editar.html', empleado = empleado)