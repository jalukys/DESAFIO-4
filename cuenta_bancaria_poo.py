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
import mysql.connector
from mysql.connector import Error
from decouple import config
import json

class CuentaBancaria:
    def __init__(self, dni, nombre, apellido, cuenta, saldo):
        self.__dni = self.validar_dni(dni) 
        self.__nombre = nombre
        self.__apellido = apellido
        self.__cuenta = cuenta
        self.__saldo = self.validar_saldo(saldo)
        #Con doble __ se aplica encapsulamiento para proteger la información, por lo tanto hay q proveer los métodos para acceder a esa información y usarlos. Dado a que al estar oculto no se puede acceder a ellos desde otra clase.

    @property #Con esta función se convierte este atributo en una propiedad de la clase
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
        return self.__saldo
    
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
            if saldo_num < 0:
                raise ValueError("El saldo debe ser numérico positivo.")
            return saldo_num
        except ValueError:
            raise ValueError("El saldo debe ser un número válido.")

    def to_dict(self): #Metodo para devolver un diccionario
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cuenta": self.cuenta,
            "saldo": self.saldo
        }

    def __str__(self): #Metodo para devolver una cadena de texto
        return f"{self.nombre} {self.apellido}"

class CuentaBancariaCorriente(CuentaBancaria):
    def __init__(self, dni, nombre, apellido, cuenta, saldo, corriente):
        super().__init__(dni, nombre, apellido, cuenta, saldo)
        self.__corriente = corriente
        #super hace los atributos de la super clase pasen a esta Subclase

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
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user= config('DB_USER')
        self.password=config('DB_PASSWORD')
        self.port = config('DB_PORT')

    def connect(self):
        '''Establecer una conexión con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )

            if connection.is_connected():
                return connection

        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None
###
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
###
    def crear_cuentabancaria(self, cuentabancaria):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el DNI ya existe
                    cursor.execute('SELECT dni FROM cuentabancaria WHERE dni = %s', (cuentabancaria.dni,))
                    if cursor.fetchone():
                        print(f'Error: Ya existe un colaborador con DNI {cuentabancaria.dni}')
                        return
                    
                    # Insertar colaborador dependiendo del tipo
                    if isinstance(cuentabancaria, CuentaBancariaCorriente):
                        query = '''
                        INSERT INTO cuentabancaria (dni, nombre, apellido, cuenta, saldo)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (cuentabancaria.dni, cuentabancaria.nombre, cuentabancaria.apellido, cuentabancaria.cuenta, cuentabancaria.saldo))

                        query = '''
                        INSERT INTO cuentabancariacorriente (dni, corriente)
                        VALUES (%s, %s)
                        '''

                        cursor.execute(query, (cuentabancaria.dni, cuentabancaria.corriente))

                    elif isinstance(cuentabancaria, CuentaBancariaAhorro):
                        query = '''
                        INSERT INTO cuentabancaria (dni, nombre, apellido, cuenta, saldo)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (cuentabancaria.dni, cuentabancaria.nombre, cuentabancaria.apellido, cuentabancaria.cuenta, cuentabancaria.saldo))

                        query = '''
                        INSERT INTO cuentabancariaahorro (dni, ahorro)
                        VALUES (%s, %s)
                        '''

                        cursor.execute(query, (cuentabancaria.dni, cuentabancaria.ahorro))

                    connection.commit()
                    print(f'Cuenta Bancaria {cuentabancaria.nombre} {cuentabancaria.apellido} creada correctamente')
        except Exception as error:
            print(f'Error inesperado al crear la Cuenta Bancaria: {error}')

    def leer_cuentabancaria(self, dni):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM cuentabancaria WHERE dni = %s', (dni,))
                    cuentabancaria_data = cursor.fetchone()

                    if cuentabancaria_data:
                        cursor.execute('SELECT corriente FROM cuentabancariacorriente WHERE dni = %s', (dni,))
                        corriente = cursor.fetchone()

                        if corriente:
                            cuentabancaria_data['corriente'] = corriente['corriente']
                            cuentabancaria = CuentaBancariaCorriente(**cuentabancaria_data)
                        else:
                            cursor.execute('SELECT ahorro FROM cuentabancariaahorro WHERE dni = %s', (dni,))
                            ahorro = cursor.fetchone()
                            if ahorro:
                                cuentabancaria_data['ahorro'] = ahorro['ahorro']
                                cuentabancaria = CuentaBancariaAhorro(**cuentabancaria_data)
                            else:
                                cuentabancaria = CuentaBancaria(**cuentabancaria_data)

                        print(f'Cuenta Bancaria encontrada: {cuentabancaria}')

                    else:
                        print(f'No se encontró Cuenta Bancaria con DNI {dni}.')

        except Error as e:
            print('Error al leer Cuenta Bancaria: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_cuentabancaria(self, dni, nuevo_saldo):
        '''Actualizar el saldo de una cuenta bancaria en la base de datos'''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el DNI existe
                    cursor.execute('SELECT * FROM cuentabancaria WHERE dni = %s', (dni,))
                    if not cursor.fetchone():
                        print(f'No se encontro Cuenta Bancaria con DNI {dni}.')
                        return
                    
                    # Actualizar salario
                    cursor.execute('UPDATE cuentabancaria SET saldo = %s WHERE dni = %s', (nuevo_saldo, dni))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Saldo actualizado para la Cuenta Bancaria con DNI: {dni}')
                    else:
                        print(f'no se encontró Cuenta Bancaria con DNI: {dni}')

        except Exception as e:
            print(f'Error al actualizar Cuenta Bancaria: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_CuentaBancaria(self, dni):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                   # Verificar si el DNI existe
                    cursor.execute('SELECT * FROM cuentabancaria WHERE dni = %s', (dni,))
                    if not cursor.fetchone():
                        print(f'No se encontro cuentabancaria con DNI {dni}.')
                        return 

                    # Eliminar el colaborador
                    cursor.execute('DELETE FROM cuentabancariacorriente WHERE dni = %s', (dni,))
                    cursor.execute('DELETE FROM cuentabancariaahorro WHERE dni = %s', (dni,))
                    cursor.execute('DELETE FROM cuentabancaria WHERE dni = %s', (dni,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Cuenta Bancaria con DNI: {dni} eliminada correctamente')
                    else:
                        print(f'No se encontró Cuenta Bancaria con DNI: {dni}')

        except Exception as e:
            print(f'Error al eliminar el Cuenta Bancaria: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def leer_todas_las_cuentabancaria(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM cuentabancaria')
                    cuentabancaria_data = cursor.fetchall()

                    cuentabancaria = [] 
                                       
                    for cuentabancaria_data in cuentabancaria_data:
                        dni = cuentabancaria_data['dni']

                        cursor.execute('SELECT corriente FROM cuentabancariacorriente WHERE dni = %s', (dni,))
                        corriente = cursor.fetchone()

                        if corriente:
                            cuentabancaria_data['corriente'] = corriente['corriente']
                            cuentabancaria = CuentaBancariaCorriente(**cuentabancaria_data)
                        else:
                            cursor.execute('SELECT ahorro FROM cuentabancariaahorro WHERE dni = %s', (dni,))
                            ahorro = cursor.fetchone()
                            cuentabancaria_data['ahorro'] = ahorro['ahorro']
                            cuentabancaria = CuentaBancariaAhorro(**cuentabancaria_data)

                        cuentabancaria.append(cuentabancaria)

        except Exception as e:
            print(f'Error al mostrar las cuentas bancarias: {e}')
        else:
            return cuentabancaria
        finally:
            if connection.is_connected():
                connection.close()