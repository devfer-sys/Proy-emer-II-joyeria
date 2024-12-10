from models.empleado import Empleado
from models.producto import Producto
from models.cliente import Cliente
from database import db

# Lista de empleados con sus datos (nombre, apellidos, cargo, contrasena)
empleados = [
    ('Mario', 'Torrez', 'Administrador', '72068397', 'Activo'),
    ('Ana', 'Arce', 'Administrador', '13760190', 'Activo'),
    ('Franklin', 'Fernandez', 'Administrador', '6954009', 'Activo')
]

# Lista de clientes con datos únicos (nombre_completo, email, telefono)
clientes = [
    ("Juan Perez", "Activo", "juan.perez@example.com", 123456789),
    ("Maria Gomez", "No Activo", "maria.gomez@example.com", 987654321),
    ("Carlos Lopez", "Activo", "carlos.lopez@example.com", 456123789),
    ("Ana Torres", "No Activo", "ana.torres@example.com", 789654123),
    ("Luis Fernandez", "Activo", "luis.fernandez@example.com", 159753486),
    ("Paula Ramirez", "No Activo", "paula.ramirez@example.com", 753951852),
    ("Jose Martinez", "Activo", "jose.martinez@example.com", 321654987),
    ("Clara Rojas", "No Activo", "clara.rojas@example.com", 987321654),
    ("Diego Suarez", "Activo", "diego.suarez@example.com", 852456159),
    ("Laura Castillo", "No Activo", "laura.castillo@example.com", 159357852),
    ("Fernando Vargas", "Activo", "fernando.vargas@example.com", 951753852),
    ("Silvia Moreno", "No Activo", "silvia.moreno@example.com", 753486951),
    ("Oscar Mendoza", "Activo", "oscar.mendoza@example.com", 456987123),
    ("Rosa Salazar", "No Activo", "rosa.salazar@example.com", 789321654),
    ("Manuel Ortega", "Activo", "manuel.ortega@example.com", 852159753),
    ("Diana Villarroel", "No Activo", "diana.villarroel@example.com", 123987456),
    ("Hector Alvarez", "Activo", "hector.alvarez@example.com", 951357852),
    ("Sandra Jimenez", "No Activo", "sandra.jimenez@example.com", 654789321),
    ("Victor Cabrera", "Activo", "victor.cabrera@example.com", 357951486),
    ("Elena Paredes", "No Activo", "elena.paredes@example.com", 987456321)
]


# Lista de productos con datos únicos (nombre, precio, stock, disponibilidad)
productos = [
    ("Collar de Oro", 500, 20),
    ("Anillo de Plata", 300, 50),
    ("Pulsera de Oro", 700, 15),
    ("Reloj de Acero", 250, 30),
    ("Aretes de Perla", 150, 40),
    ("Cadena de Plata", 350, 25),
    ("Dije de Diamante", 1000, 10),
    ("Brazalete de Cuarzo", 400, 20),
    ("Anillo de Titanio", 600, 18),
    ("Broche de Rubí", 800, 12),
    ("Anillo de Oro", 900, 22),
    ("Pendientes de Esmeralda", 600, 16),
    ("Reloj de Oro", 1200, 8),
    ("Collar de Plata", 450, 35),
    ("Pulsera de Diamante", 1500, 5),
    ("Anillo de Zafiro", 1100, 10),
    ("Dije de Esmeralda", 800, 14),
    ("Brazalete de Oro", 950, 9),
    ("Aretes de Rubí", 700, 19),
    ("Reloj de Diamante", 2000, 3)
]

# Función para insertar los empleados en la base de datos
def insertar_empleados(app):
    with app.app_context():  # Asegura que el contexto de la aplicación esté disponible
        # Insertar Empleados
        for nombre, apellidos, cargo, contrasena, estado in empleados:
            # Verificar si el empleado ya existe en la base de datos
            existe = Empleado.query.filter_by(nombre=nombre, apellidos=apellidos).first()
            
            if existe:
                
                continue  # Salta a la siguiente iteración si ya existe
            
            # Crear un nuevo empleado si no existe
            empleado = Empleado(
                nombre=nombre,
                apellidos=apellidos,
                cargo=cargo,
                contrasena=contrasena,
                estado=estado
            )
            db.session.add(empleado)  # Agregar el empleado a la sesión

        # Insertar clientes
        for nombre_completo, estado, email, telefono in clientes:
            # Verificar si el cliente ya existe en la base de datos
            existe_cliente = Cliente.query.filter_by(email=email).first()
            if existe_cliente:
                
                continue
            
            # Crear un nuevo cliente si no existe
            cliente = Cliente(
                nombre_completo=nombre_completo,
                estado=estado,
                email=email,
                telefono=telefono
            )
            db.session.add(cliente)
        
        # Insertar productos
        for nombre, precio, stock in productos:
            # Verificar si el producto ya existe en la base de datos
            existe_producto = Producto.query.filter_by(nombre=nombre).first()
            if existe_producto:
                
                continue
            
            # Crear un nuevo producto si no existe
            producto = Producto(
                nombre=nombre,
                precio=precio,
                stock=stock
            )
            db.session.add(producto)
        
        
        
        db.session.commit()  # Confirmar los cambios en la base de datos

        
