#Sandra Colomé 2-19-0138 Ejercicio 1 - Paralelos
import mysql.connector
import os
import logging
import csv
from multiprocessing import Process
import time

# Configurar el logger
logging.basicConfig(filename='floristeria.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Función para conectar a la base de datos
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='floristeriascm'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
     # Función para iniciar sesión
def login(user, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM login WHERE user = %s AND pass = %s"
        cursor.execute(query, (user, password))
        result = cursor.fetchone()  # Obtiene un solo registro

        cursor.close()
        conn.close()

        if result:
            return True  # Login exitoso
        else:
            return False  # Login fallido

    return False  # Conexión fallida
#-------------------------------------------------------------------------------------------------------------------------


# Función para registrar un cliente
def registrar_cliente(nombre, email, telefono, direccion):
    logging.info(f"Iniciando el registro del cliente: {nombre}")
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, email, telefono, direccion))
        conn.commit()
        logging.info(f"Cliente registrado: {nombre}, Email: {email}")
        print("Cliente registrado exitosamente.")
        cursor.close()
        conn.close()

        # Registrar en el CSV
        with open('reporte_floristeria.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "Registrar Cliente", f"Nombre: {nombre}, Email: {email}"])

    logging.info(f"Registro del cliente completado: {nombre}")

# Función para registrar un pedido
def registrar_pedido(cliente_id, total):
    logging.info(f"Iniciando el registro del pedido para el cliente ID: {cliente_id}")
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO pedidos (cliente_id, total) VALUES (%s, %s)"
        cursor.execute(query, (cliente_id, total))
        conn.commit()
        logging.info(f"Pedido registrado para cliente ID: {cliente_id}, Total: {total}")
        print(f"Pedido registrado exitosamente para cliente ID: {cliente_id}.")
        cursor.close()
        conn.close()

        # Registrar en el CSV
        with open('reporte_floristeria.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "Registrar Pedido", f"Cliente ID: {cliente_id}, Total: {total}"])

    logging.info(f"Registro del pedido completado para el cliente ID: {cliente_id}")

# Función para consultar clientes
def consultar_clientes():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM clientes"
        cursor.execute(query)
        clientes = cursor.fetchall()
        print("\n--- Clientes registrados ---")
        for cliente in clientes:
            print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Email: {cliente[2]}, Teléfono: {cliente[3]}, Dirección: {cliente[4]}")
        cursor.close()
        conn.close()

# Función para consultar productos
def consultar_productos():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()
        print("\n--- Productos disponibles ---")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: DOP {producto[3]}, Stock: {producto[4]}")
        cursor.close()
        conn.close()

# Función para consultar pedidos por cliente
def consultar_pedidos_por_cliente(cliente_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM pedidos WHERE cliente_id = %s"
        cursor.execute(query, (cliente_id,))
        pedidos = cursor.fetchall()
        print(f"\n--- Pedidos para el cliente ID {cliente_id} ---")
        if pedidos:
            for pedido in pedidos:
                print(f"ID: {pedido[0]}, Fecha: {pedido[2]}, Total: DOP {pedido[3]}, Estado: {pedido[4]}")
        else:
            print("No hay pedidos registrados para este cliente.")
        cursor.close()
        conn.close()
#-------------------------------------------------------------------------------------------------------------------------
# Función para mostrar el menú
def mostrar_menu():
    print("\n--- Menú de Floristería Sandrix ---")
    print("1. Registrar cliente")
    print("2. Registrar pedido")
    print("3. Consultar clientes")
    print("4. Consultar productos")
    print("5. Consultar pedidos por cliente")
    print("6. Salir")
    print("-----------------------------\n")
#-------------------------------------------------------------------------------------------------------------------------

# Función para limpiar la terminal
def limpiar_terminal():
    # Limpiar la terminal dependiendo del sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

# Función principal
def main():
    # Solicitar credenciales
    while True:
        username = input("Ingresa tu usuario: ")
        password = input("Ingresa tu contraseña: ")
        if login(username, password):
            limpiar_terminal()  # Limpiar la terminal al iniciar sesión
            print("Inicio de sesión exitoso!")
            break  # Salir del bucle si el login es exitoso
        else:
            limpiar_terminal()  # Limpiar la terminal al intentar de nuevo
            print("Usuario o contraseña incorrectos. Intenta de nuevo.")

    # Menú principal
    while True:
       while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ")

        if opcion == '1':
            nombre = input("Nombre del cliente: ")
            email = input("Email del cliente: ")
            telefono = input("Teléfono del cliente: ")
            direccion = input("Dirección del cliente: ")
            p_cliente = Process(target=registrar_cliente, args=(nombre, email, telefono, direccion))
            p_cliente.start()
            p_cliente.join()  # Esperar a que el proceso termine antes de continuar
            logging.info(f"Cliente registrado: {nombre}")  # Registrar la acción

        elif opcion == '2':
            cliente_id = input("ID del cliente: ")
            total = input("Total del pedido: ")
            p_pedido = Process(target=registrar_pedido, args=(cliente_id, total))
            p_pedido.start()
            p_pedido.join()  # Esperar a que el proceso termine antes de continuar
            logging.info(f"Pedido registrado para cliente ID: {cliente_id}, Total: {total}")  # Registrar la acción

        elif opcion == '3':
            p_clientes = Process(target=consultar_clientes)
            p_clientes.start()
            p_clientes.join()  # Esperar a que el proceso termine antes de continuar
            logging.info("Consulta de clientes realizada.")  # Registrar la acción

        elif opcion == '4':
            p_productos = Process(target=consultar_productos)
            p_productos.start()
            p_productos.join()  # Esperar a que el proceso termine antes de continuar
            logging.info("Consulta de productos realizada.")  # Registrar la acción

        elif opcion == '5':
            cliente_id = input("Ingrese el ID del cliente para consultar sus pedidos: ")
            p_pedidos_cliente = Process(target=consultar_pedidos_por_cliente, args=(cliente_id,))
            p_pedidos_cliente.start()
            p_pedidos_cliente.join()  # Esperar a que el proceso termine antes de continuar
            logging.info(f"Consulta de pedidos realizada para cliente ID: {cliente_id}.")  # Registrar la acción

        elif opcion == '6':
            print("Saliendo del programa. ¡byebyeflower!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
