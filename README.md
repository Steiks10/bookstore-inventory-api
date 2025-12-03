# Bookstore Inventory API

Proyecto Django REST Framework para gestionar libros con una arquitectura limpia (Clean Architecture).

## Cómo ejecutar

### Opción A: Docker Compose
- Requisitos: Docker y Docker Compose.
- Pasos:
	1. Construir y levantar servicios:
		 - `docker compose up --build`
	2. La app corre en `http://localhost:8000/` y redirige a `/docs/`.

Notas:
- Si ves errores de migración por “table already exists”, finge la inicial: `docker compose run --rm web bash -lc "python manage.py migrate --fake-initial || python manage.py migrate"`.
- Si ejecutaste con Docker antes y ahora corres local, asegúrate de que `db.sqlite3` no esté en modo solo lectura. Corrige permisos: `sudo chown "$USER":"$USER" db.sqlite3 && sudo chmod 664 db.sqlite3`. Ya que el usuario con el que se creo con docker puede que no sea el mismo que con el que se creo en local

## Endpoints principales
- `POST /api/books/`: Crear libro.
- `GET /api/books/`: Listar libros (paginación opcional `page`, `page_size`).
- `GET /api/books/{id}/`: Obtener libro por ID.
- `PUT /api/books/{id}/`: Actualizar parcialmente libro.
- `DELETE /api/books/{id}/`: Eliminar libro.
- `GET /api/books/search/?category=...`: Buscar por categoría (paginable).
- `GET /api/books/low-stock/?threshold=...`: Listar con bajo stock (paginable).
- `POST /api/books/{id}/calculate-price/`: Calcular precio sugerido (requiere `currency`, opcional `margin_percent`, `save`).


### Opción B: Local (sin Docker)
- Requisitos: Python 3.11+.
- Pasos:
	1. Crear y activar entorno virtual:
		 - `python -m venv .venv`
		 - `source .venv/bin/activate`
	2. Instalar dependencias:
		 - `pip install -r requirements.txt`
	3. Aplicar migraciones:
		 - `python manage.py makemigrations`
		 - `python manage.py migrate`
	4. (Opcional) Insertar datos de ejemplo en la base de datos:
		 - `python manage.py seed_books`
	5. Ejecutar servidor:
		 - `python manage.py runserver`
	6. Abrir documentación (Swagger):
		 - `http://localhost:8000/` (redirige a `/docs/`).

Nota: no ejecutes Docker y el entorno local al mismo tiempo; pueden aparecer errores de migración, bloqueo/permisos de la base de datos SQLite y conflictos de puerto (8000).

## Arquitectura

El proyecto sigue una arquitectura limpia (Clean Architecture) con separación por capas:

- `books/domain/`:
	- Entidades y contratos del dominio.
	- `book.py`: Modelo de libro.
	- `repositories.py`: Interfaces de repositorios (abstracciones de persistencia).
	- `rates.py`: Interfaz `RatesProvider` para proveedor de tasas de cambio.

- `books/application/`:
	- Casos de uso (lógica de aplicación orquestada).
	- `use_cases/`: crear, listar, obtener, actualizar, eliminar, buscar, bajo stock, calcular precio.
	- `dto.py`: objetos de transferencia para respuestas.

- `books/infraestructure/`:
	- Implementaciones concretas usando Django ORM y HTTP.
	- `book_repository.py`: implementación del repositorio con ORM.
	- `rates_provider.py`: proveedor HTTP de tasas de cambio.

- `books/controllers/`:
	- Contenedor/proveedores para inyección de dependencias.
	- `container.py`: entrega instancias de repositorios y proveedores.

- `books/api/`:
	- Capa de entrega (DRF): serializers y views.
	- `serializers.py`: validaciones y serialización.
	- `views.py`: endpoints REST con anotaciones de `drf-spectacular`.

- `bookstore/`:
	- Configuración del proyecto, `settings.py` y `urls.py`.
	- Redirección de `/` a `/docs/` para acceder Swagger rápidamente.

## Documentación
- `drf-spectacular` configurado en `bookstore/urls.py`:
	- `/schema/`: OpenAPI schema.
	- `/docs/`: Swagger UI.
	- `/redoc/`: Redoc.

## Semillas de datos
- Comando: `python manage.py seed_books` (idempotente, crea libros de ejemplo si no existen).

## Postman
- Archivo `postman_collection.json` con ejemplos para todos los endpoints.

Nota: asegurese que en los metodos PUT o POST al final de la url tenga /

Muchas gracias:D
