from flask import render_template


def list(clientes):
    return render_template('clientes/index.html', clientes = clientes)


def registrar():
    return render_template('clientes/registrar.html')


def editar(cliente):
    return render_template('clientes/editar.html', cliente = cliente)
