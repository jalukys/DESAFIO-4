'''
Desafío 4: Sistema de Gestión de Cuentas Bancarias

Objetivo: Desarrollar un sistema para administrar cuentas bancarias de clientes.

Requisitos:

    Crear una clase base CuentaBancaria con atributos como número de cuenta, saldo, titular de la cuenta, etc.
    Definir al menos 2 clases derivadas para diferentes tipos de cuentas bancarias (por ejemplo, CuentaBancariaCorrientes, CuentaBancariaAhorro) con atributos y métodos específicos.
    Implementar operaciones CRUD para gestionar las cuentas bancarias.
    Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
    Persistir los datos en archivo JSON
'''
import json

class CuentaBancaria:
    def __init__(self, dni, nombre, apellido, cuenta, saldo):
        self.__dni = self.validar_dni(dni)
        self.__nombre = nombre
        self.__apellido = apellido
        self.__cuenta = cuenta
        self.__saldo = self.validar_saldo(saldo)

    @property
    def dni(self):
        return self.__dni
    
    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def apellido(self):
        return self.__apellido.capitalize()
    
    @property
    def cuenta(self):
        return self.__cuenta
    
    @property
    def saldo(self):
        return self.__salado
    
    @saldo.setter
    def saldo(self, nuevo_saldo):
        self.__saldo = self.validar_saldo(nuevo_saldo)

    def validar_dni(self, dni):
        try:
            dni_num = int(dni)
            if len(str(dni)) not in [7, 8]:
                raise ValueError("El DNI debe tener 7 u 8 dígitos.")
            if dni_num <= 0:
                raise ValueError("El DNI debe ser numérico positivo.")
            return dni_num
        except ValueError:
            raise ValueError("El DNI debe ser numérico y estar compuesto por 7 u 8 dígitos.")

    def validar_saldo(self, saldo):
        try:
            saldo_num = float(saldo)
            if saldo_num <= 0:
                raise ValueError("El saldo debe ser numérico positivo.")
            return saldo_num
        except ValueError:
            raise ValueError("El saldo debe ser un número válido.")

    def to_dict(self):
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cuenta": self.cuenta,
            "saldo": self.saldo
        }

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class CuentaBancariaCorriente(CuentaBancaria):
    def __init__(self, dni, nombre, apellido, cuenta, saldo, corriente):
        super().__init__(dni, nombre, apellido, cuenta, saldo)
        self.__corriente = corriente

    @property
    def corriente(self):
        return self.__corriente

    def to_dict(self):
        data = super().to_dict()
        data["corriente"] = self.corriente
        return data

    def __str__(self):
        return f"{super().__str__()} - Cuenta Corriente: {self.corriente}"

class CuentaBancariaAhorro(CuentaBancaria):
    def __init__(self, dni, nombre, apellido, cuenta, saldo, ahorro):
        super().__init__(dni, nombre, apellido, cuenta, saldo)
        self.__ahorro = ahorro

    @property
    def ahorro(self):
        return self.__ahorro

    def to_dict(self):
        data = super().to_dict()
        data["ahorro"] = self.ahorro
        return data

    def __str__(self):
        return f"{super().__str__()} - Cuenta Ahorro: {self.ahorro}"

class GestionCuentaBancaria:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_CuentaBancaria(self, CuentaBancaria):
        try:
            datos = self.leer_datos()
            dni = CuentaBancaria.dni
            if not str(dni) in datos.keys():
                datos[dni] = CuentaBancaria.to_dict()
                self.guardar_datos(datos)
                print(f"La Cuenta Bancaria de {CuentaBancaria.nombre} {CuentaBancaria.apellido} se ha creado correctamente.")
            else:
                print(f"Ya existe cuenta bancacia con DNI '{dni}'.")
        except Exception as error:
            print(f'Error inesperado al crear la cuenta bancaria: {error}')

    def leer_CuentaBancaria(self, dni):
        try:
            datos = self.leer_datos()
            if dni in datos:
                CuentaBancaria_data = datos[dni]
                if 'corriente' in CuentaBancaria_data:
                    CuentaBancaria = CuentaBancariaCorriente(**CuentaBancaria_data)
                else:
                    CuentaBancaria = CuentaBancariaAhorro(**CuentaBancaria_data)
                print(f'Cuenta bancaria encontrada con DNI {dni}')
            else:
                print(f'No se encontró ha encontrado Cuenta Bancaria con DNI {dni}')

        except Exception as e:
            print('Error al leer Cuenta Bancaria: {e}')

    def actualizar_CuentaBancaria(self, dni, nuevo_saldo):
        try:
            datos = self.leer_datos()
            if str(dni) in datos.keys():
                 datos[dni]['saldo'] = nuevo_saldo
                 self.guardar_datos(datos)
                 print(f'Saldo actualizado para la Cuenta Bancaria DNI:{dni}')
            else:
                print(f'No se encontró Cuenta Bancaria con DNI:{dni}')
        except Exception as e:
            print(f'Error al actualizar la Cuenta Bancaria: {e}')

    def eliminar_CuentaBancaria(self, dni):
        try:
            datos = self.leer_datos()
            if str(dni) in datos.keys():
                 del datos[dni]
                 self.guardar_datos(datos)
                 print(f'Cuenta Bancaria DNI:{dni} eliminada correctamente')
            else:
                print(f'No se encontró Cuenta Bancaria con DNI:{dni}')
        except Exception as e:
            print(f'Error al eliminar la Cuenta Bancaria: {e}')