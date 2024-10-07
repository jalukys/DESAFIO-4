CREATE DATABASE cuentabancaria;
USE cuentabancaria; -- siempre se pone este comando para que las tablas dentro
					-- de la base de datos creada.-

CREATE TABLE CuentaBancaria (
	dni char(8) primary key,
	nombre varchar(50) not null,
	apellido varchar(50) not null,
	cuenta INT not null,
	saldo decimal (10,2) not null
);

CREATE TABLE CuentaBancariaCorriente (
	dni char(8) primary key,
	corriente varchar(50) not null,
    foreign key (dni) references CuentaBancaria(dni) -- Relación con cta bcaria
);

CREATE TABLE CuentaBancariaAhorro (
	dni char(8) primary key,
	ahorro varchar(50) not null,
    foreign key (dni) references CuentaBancaria(dni) -- Relación con cta bcaria
);
