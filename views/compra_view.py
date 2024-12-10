from flask import render_template

def list(compras):
    return render_template('compras/index.html', compras=compras)

def registrar(clientes, productos):
    return render_template('compras/registrar.html', clientes=clientes, productos=productos)

def editar(compra, clientes, productos):
    return render_template('compras/editar.html', compra=compra, clientes=clientes, productos=productos)
