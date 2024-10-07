import os
import platform

from cuenta_bancaria_poo import (
    CuentaBancariaCorriente,
    CuentaBancariaAhorro,
    GestionCuentaBancaria,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Cuenta Bancaria ==========")
    print('1. Agregar Cuenta Bancaria Corriente')
    print('2. Agregar Cuenta Bancaria Ahorro')
    print('3. Buscar Cuenta Bancaria por DNI')
    print('4. Actualizar Cuenta Bancaria')
    print('5. Eliminarar Cuenta Bancaria por DNI')
    print('6. Mostrar Todas las Cuenta Bancaria')
    print('7. Salir')
    print('======================================================')

def agregar_cuentabancaria(gestion, tipo_cuentabancaria):
    try:
        dni = input('Ingrese DNI del titular de la Cuenta Bancaria: ')
        nombre = input('Ingrese nombre del titular: ')
        apellido = input('Ingrese apellido del titular: ')
        cuenta = int(input('Ingrese número de la Cuenta Bancaria: '))
        saldo = float(input('Ingrese saldo de la Cuenta Bancaria: '))

        if tipo_cuentabancaria == '1':
            corriente = 'Cuenta Corriente'
            cuentabancaria = CuentaBancariaCorriente(dni, nombre, apellido, cuenta, saldo, corriente)
        elif tipo_cuentabancaria == '2':
            ahorro = 'Cuenta ahorro'
            cuentabancaria = CuentaBancariaAhorro(dni, nombre, apellido, cuenta, saldo, ahorro)
        else:
            print('Opción inválida')
            return

        gestion.crear_cuentabancaria(cuentabancaria)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_cuentabancaria_por_dni(gestion):
    dni = input('Ingrese el DNI de la cuenta bancaria a buscar: ')
    gestion.leer_cuentabancaria(dni)
    input('Presione enter para continuar...')

def actualizar_saldo_leer_cuentabancaria(gestion):
    dni = input('Ingrese el DNI del titular de la cuenta para actualizar saldo: ')
    saldo = float(input('Ingrese el saldo de la cuenta bancaria: '))
    gestion.actualizar_cuentabancaria(dni, saldo)
    input('Presione enter para continuar...')

def eliminar_cuentabancaria_por_dni(gestion):
    dni = input('Ingrese el DNI del titula de la cuenta bancaria a eliminar: ')
    gestion.eliminar_CuentaBancaria(dni)
    input('Presione enter para continuar...')

def mostrar_todas_las_cuentas_bancarias(gestion):
    print('=============== Listado completo de las  Cuentas Bancarias ==============')
    for cuentabancaria in gestion.leer_datos().values():
        if 'Cuenta Corriente' in cuentabancaria:
            print(f"{cuentabancaria['nombre']} - Cuenta Corriente {cuentabancaria['Cuenta Corriente']}")
        else:
            print(f"{cuentabancaria['nombre']} - Cuenta Ahorro {cuentabancaria['Cuenta Ahorro']}")
    print('=====================================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_cuentabancaria = 'cuentabancaria_db.json'
    gestion_cuentabancaria = GestionCuentaBancaria(archivo_cuentabancaria)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_cuentabancaria(gestion_cuentabancaria, opcion)
        
        elif opcion == '3':
            buscar_cuentabancaria_por_dni(gestion_cuentabancaria)

        elif opcion == '4':
            actualizar_saldo_leer_cuentabancaria(gestion_cuentabancaria)

        elif opcion == '5':
            eliminar_cuentabancaria_por_dni(gestion_cuentabancaria)

        elif opcion == '6':
            mostrar_todas_las_cuentas_bancarias(gestion_cuentabancaria)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1 al 7)')
        

