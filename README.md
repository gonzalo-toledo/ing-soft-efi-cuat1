# Sistema de Gestión de Aerolínea

## 📋 Descripción del Proyecto

Este es un sistema de gestión de aerolínea desarrollado en **Django 5.2.3** que permite administrar vuelos, aviones, pasajeros, reservas y aeropuertos. El sistema incluye funcionalidades de autenticación de usuarios, gestión de vuelos, reservas de asientos y administración de datos maestros como nacionalidades y aeropuertos.

## 🏗️ Arquitectura del Proyecto

### Aplicaciones Django

El proyecto está organizado en las siguientes aplicaciones:

- **`home`**: Aplicación principal con autenticación, nacionalidades y página de inicio
- **`vuelos`**: Gestión de vuelos y aeropuertos
- **`aviones`**: Gestión de aviones y asientos
- **`pasajeros`**: Gestión de información de pasajeros
- **`reservas`**: Sistema de reservas de vuelos

### Modelos de Datos

#### Home App
- **Nacionalidad**: Código de país, nombre del país y gentilicio

#### Vuelos App
- **Aeropuerto**: Información completa de aeropuertos (IATA, nombre, ciudad, coordenadas, etc.)
- **Vuelo**: Relaciona avión, origen, destino, fechas, estado y precio

#### Aviones App
- **Avion**: Modelo, capacidad, filas y columnas
- **Asiento**: Número, fila, columna, tipo (Económico/Primera Clase) y estado

#### Reservas App
- **Pasajero**: Información personal del pasajero
- **Reserva**: Relaciona pasajero, vuelo y asiento con estado de la reserva

## 🚀 Guía de Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ing-soft-efi-cuat1
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos

```bash
# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser
```

### Paso 5: Cargar Datos Iniciales

El proyecto incluye comandos personalizados para cargar datos maestros:

```bash
# Cargar nacionalidades
python manage.py cargar_nacionalidades

# Cargar aeropuertos
python manage.py cargar_aeropuertos
```

### Paso 6: Ejecutar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 📁 Estructura del Proyecto

```
ing-soft-efi-cuat1/
├── aerolinea/                 # Configuración principal del proyecto
│   ├── settings.py           # Configuraciones de Django
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # Configuración WSGI
├── home/                     # Aplicación principal
│   ├── models.py             # Modelo Nacionalidad
│   ├── views.py              # Vistas de autenticación y home
│   ├── forms.py              # Formularios de registro y login
│   ├── urls.py               # URLs de la app home
│   ├── templates/            # Templates HTML
│   └── management/           # Comandos personalizados
│       └── commands/
│           └── cargar_nacionalidades.py
├── vuelos/                   # Aplicación de vuelos
│   ├── models.py             # Modelos Vuelo y Aeropuerto
│   ├── views.py              # Vistas de vuelos
│   ├── urls.py               # URLs de vuelos
│   └── management/           # Comandos personalizados
│       └── commands/
│           └── cargar_aeropuertos.py
├── aviones/                  # Aplicación de aviones
│   ├── models.py             # Modelos Avion y Asiento
│   └── admin.py              # Configuración del admin
├── pasajeros/                # Aplicación de pasajeros
│   └── models.py             # Modelo Pasajero
├── reservas/                 # Aplicación de reservas
│   ├── models.py             # Modelos Pasajero y Reserva
│   └── admin.py              # Configuración del admin
├── manage.py                 # Script de gestión de Django
├── requirements.txt          # Dependencias del proyecto
├── db.sqlite3               # Base de datos SQLite
└── README.md                # Este archivo
```

## 🔧 Configuración del Entorno de Desarrollo

## 🎯 Funcionalidades Principales

### Autenticación de Usuarios
- Registro de nuevos usuarios
- Inicio de sesión
- Cerrar sesión
- Sistema de mensajes para errores y éxito

### Gestión de Vuelos
- Visualización de vuelos disponibles
- Información detallada de vuelos (origen, destino, fechas, precio)
- Estados de vuelo (Programado, En Vuelo, Aterrizado, Cancelado, Retrasado)

### Sistema de Reservas
- Creación de reservas de vuelos
- Selección de asientos
- Estados de reserva (Confirmada, Pendiente, Cancelada)
- Validación de asientos únicos por vuelo

### Gestión de Aviones
- Configuración automática de asientos al crear un avión
- Tipos de asiento (Económico y Primera Clase)
- Estados de asiento (Disponible, Reservado, Ocupado)

### Datos Maestros
- Nacionalidades con códigos de país
- Aeropuertos con información completa (IATA, coordenadas, etc.)

## 🛠️ Comandos Útiles

### Comandos de Django

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar tests
python manage.py test

# Shell de Django
python manage.py shell
```

### Comandos Personalizados

```bash
# Cargar nacionalidades desde JSON
python manage.py cargar_nacionalidades

# Cargar aeropuertos desde JSON
python manage.py cargar_aeropuertos
```
Accede al admin en: `http://127.0.0.1:8000/admin/`

**¡Bienvenido al proyecto! 🚀**

