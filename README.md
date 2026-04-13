# Flask Project - Backend con JWT y CORS

Proyecto educativo de backend para aprender Flask con ejemplos básicos de autenticación JWT, CORS, y conceptos fundamentales de desarrollo web con Python.

## Equipo de Desarrollo

| Rol | Nombre | GitHub |
|-----|--------|--------|
| Developer | German Illan | [GitHub](https://github.com/GermanIllan) |
| Scrum Master | Yeremi Peralta | [GitHub](https://github.com/yeremijesus9) |
| Product Owner | Yoandres La Cruz | [GitHub](https://github.com/ylcruzdev) |

## Tabla de Contenidos

- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Endpoints Principales](#endpoints-principales)
- [Testing](#testing)
- [Estado del Proyecto](#estado-del-proyecto)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Tecnologías

- **Flask 3.1** - Framework web Python
- **Flask-JWT-Extended** - Autenticación JWT
- **Flask-CORS** - Configuración de CORS
- **Flask-SQLAlchemy** - ORM para bases de datos
- **Flask-Bcrypt** - Hash de contraseñas
- **SQLite** - Base de datos ligera
- **Python-dotenv** - Variables de entorno
- **Pytest** - Framework de testing

## Estructura del Proyecto

```
flask_project/
├── app/
│   ├── api/
│   │   ├── auth/              # Endpoints de autenticación
│   │   │   ├── models.py      # Modelo de Usuario
│   │   │   ├── routes.py     # Rutas: /register, /login, /logout
│   │   │   └── services.py    # Lógica de autenticación
│   │   ├── basics/            # Ejemplos básicos (German)
│   │   │   └── routes.py
│   │   ├── examples_yeremi/    # Ejemplos intermedios (Yeremi)
│   │   │   ├── routes/        # Rutas básicas
│   │   │   ├── crud/          # Operaciones CRUD
│   │   │   ├── sqlite/        # Persistencia con SQLite
│   │   │   └── modularization/# Estructura modular
│   │   └── main/              # Endpoints principales
│   ├── core/
│   │   ├── blueprints.py      # Registro de blueprints
│   │   ├── config.py          # Configuración por entorno
│   │   ├── cors_config.py     # Configuración CORS
│   │   ├── errors.py          # Manejo de errores
│   │   ├── extensions.py      # Extensiones Flask
│   │   ├── jwt_config.py      # Configuración JWT
│   │   ├── jwt_handlers.py    # Callbacks JWT
│   │   ├── models.py          # Modelos base
│   │   └── utils.py           # Utilidades
│   └── templates/             # Plantillas HTML
├── instance/                  # Archivos de instancia (DB)
├── tests/                     # Suite de tests
│   ├── cors/                  # Tests de CORS
│   └── test_jwt/              # Tests de JWT
├── run.py                     # Punto de entrada
├── requirements.txt           # Dependencias
└── .env.example               # Variables de entorno (plantilla)
```

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/yeremijesus9/flask_project.git
   cd flask_project
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copiar archivo de entorno**
   ```bash
   cp .env.example .env
   ```

5. **Ejecutar el servidor**
   ```bash
   .venv/bin/python run.py
   ```

## Configuración

El proyecto utiliza variables de entorno. Copia `.env.example` a `.env` y ajusta según necesidad:

```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_RUN_PORT=7070
JWT_SECRET_KEY=your_jwt_secret_here
SQLALCHEMY_DATABASE_URI=sqlite:///dev.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Descripción de Variables

| Variable | Descripción | Valores posibles |
|----------|-------------|------------------|
| `FLASK_ENV` | Entorno de ejecución | `development`, `test`, `production` |
| `FLASK_RUN_PORT` | Puerto del servidor | Cualquier puerto disponible |
| `JWT_SECRET_KEY` | Clave para tokens JWT | Cadena segura |
| `SQLALCHEMY_DATABASE_URI` | URL de la base de datos | URI de SQLAlchemy |
| `CORS_ORIGINS` | Orígenes permitidos | Lista separada por comas |

## Endpoints Principales

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/register` | Registrar nuevo usuario |
| POST | `/api/auth/login` | Iniciar sesión |
| POST | `/api/auth/logout` | Cerrar sesión (requiere JWT) |
| POST | `/api/auth/keep-alive` | Renovar token (requiere JWT) |

### Ejemplos

| Endpoint | Descripción |
|----------|-------------|
| `/api/examples-yeremi/routes` | Rutas básicas, parámetros y query strings |
| `/api/examples-yeremi/crud` | Operaciones CRUD en memoria |
| `/api/examples-yeremi/sqlite` | Persistencia con SQLite |
| `/api/examples-yeremi/modularization` | Estructura modular |
| `/api/basics` | Ejemplos básicos de Flask |

## Testing

Los tests se ejecutan dentro del entorno virtual. Primero activa el entorno y luego ejecuta pytest:

```bash
# Activar el entorno virtual (Linux/Mac)
source .venv/bin/activate

# Activar el entorno virtual (Windows)
.venv\Scripts\activate
```

Ejecutar todos los tests:
```bash
python -m pytest
```

Ejecutar tests específicos:
```bash
# Tests de autenticación
python -m pytest tests/test_auth.py

# Tests de JWT
python -m pytest tests/test_jwt/

# Tests de CORS
python -m pytest tests/cors/
```

## Estado del Proyecto

**Estado:** En Desarrollo

Este proyecto se encuentra en fase activa de desarrollo. Los ejemplos y funcionalidades están siendo implementados y probados.

---

⭐️ Si te fue útil este proyecto, no olvides una estrella!