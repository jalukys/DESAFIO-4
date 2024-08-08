import os
import platform

from cuenta_bancaria_poo.py import (
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

def agregar_CuentaBancaria(gestion, tipo_CuentaBancaria):
    try:
        dni = input('Ingrese DNI del titular de la Cuenta Bancaria: ')
        nombre = input('Ingrese nombre del titular: ')
        apellido = input('Ingrese apellido del titular: ')
        cuenta = int(input('Ingrese número de la Cuenta Bancaria: '))
        saldo = float(input('Ingrese saldo de la Cuenta Bancaria: '))

        if tipo_CuentaBancaria == '1':
            corriente = input('Ingrese cuenta corriente: ')
            CuentaBancaria = CuentaBancariaCorriente(dni, nombre, apellido, cuenta, saldo, corriente)
        elif tipo_CuentaBancaria == '2':
            ahorro = int(input('Ingrese cuenta ahorro: '))
            CuentaBancaria = CuentaBancariaAhorro(dni, nombre, apellido, cuenta, saldo, ahorro)
        else:
            print('Opción inválida')
            return

        gestion.crear_CuentaBancaria(CuentaBancaria)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_CuentaBancaria_por_dni(gestion):
    dni = input('Ingrese el DNI de la cuenta bancaria a buscar: ')
    gestion.leer_CuentaBancaria(dni)
    input('Presione enter para continuar...')

def actualizar_saldo_leer_CuentaBancaria(gestion):
    dni = input('Ingrese el DNI del titular de la cuenta para actualizar saldo: ')
    saldo = float(input('Ingrese el saldo de la cuenta bancaria: '))
    gestion.actualizar_CuentaBancaria(dni, saldo)
    input('Presione enter para continuar...')

def eliminar_CuentaBancaria_por_dni(gestion):
    dni = input('Ingrese el DNI del titula de la cuenta bancaria a eliminar: ')
    gestion.eliminar_CuentaBancaria(dni)
    input('Presione enter para continuar...')

def mostrar_todas_las_Cuentas_Bancarias(gestion):
    print('=============== Listado completo de los  Colaboradores ==============')
    for CuentaBancaria in gestion.leer_datos().values():
        if 'corriente' in CuentaBancaria:
            print(f"{CuentaBancaria['nombre']} - Corriente {CuentaBancaria['corriente']}")
        else:
            print(f"{CuentaBancaria['nombre']} - Ahorro {CuentaBancaria['ahorro']}")
    print('=====================================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_CuentaBancaria = 'CuentaBancaria_db.json'
    gestion = GestionCuentaBancaria(archivo_CuentaBancaria)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_CuentaBancaria(gestion, opcion)
        
        elif opcion == '3':
            buscar_CuentaBancaria_por_dni(gestion)

        elif opcion == '4':
            actualizar_saldo_leer_CuentaBancaria(gestion)

        elif opcion == '5':
            eliminar_CuentaBancaria_por_dni(gestion)

        elif opcion == '6':
            mostrar_todas_las_Cuentas_Bancarias(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
        

