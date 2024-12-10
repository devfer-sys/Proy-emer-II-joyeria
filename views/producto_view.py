from flask import render_template


def list(productos):
    return render_template('productos/index.html', productos = productos)


def registrar():
    return render_template('productos/registrar.html')


def editar(producto):
    return render_template('productos/editar.html', producto = producto)