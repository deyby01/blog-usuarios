# Blog con Django y PostgreSQL 🐘

Este es un proyecto de blog funcional construido con Django, diseñado para demostrar las características fundamentales y las mejores prácticas del framework. La aplicación permite a los usuarios gestionar posts, organizarlos por categorías y cuenta con un sistema de autenticación, todo corriendo en un entorno dockerizado con PostgreSQL.

---

## ✨ Características Principales

* **Gestión Completa de Posts (CRUD):** Los usuarios autenticados pueden Crear, Leer, Actualizar y Eliminar sus propios posts.
* **Sistema de Categorías:** Los posts se pueden organizar en múltiples categorías a través de una relación Muchos-a-Muchos.
* **URLs Amigables (Slugs):** URLs limpias y legibles para cada post (ej: `/mi-primer-post/`).
* **Panel de Administración Personalizado:** Interfaz de administración de Django optimizada para gestionar Posts y Categorías de forma eficiente, con autocompletado de slugs.
* **Autenticación y Autorización:** Sistema completo de inicio de sesión, cierre de sesión. Las acciones de edición y eliminación están restringidas solo al autor del post.
* **Sistema de Comentarios:** Los usuarios autenticados pueden dejar comentarios en los posts.
* **Paginación:** La lista de posts está paginada para manejar un gran número de artículos de forma eficiente.
* **Funcionalidad de Búsqueda:** Un formulario de búsqueda que permite encontrar posts por título o contenido.
* **Entorno Dockerizado:** La aplicación y la base de datos PostgreSQL se gestionan con Docker y Docker Compose para un entorno de desarrollo consistente y portátil.
* **Pruebas Unitarias:** Pruebas automáticas para verificar la funcionalidad de los modelos y las vistas.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django
* **Base de Datos:** PostgreSQL
* **Contenerización:** Docker, Docker Compose
* **Frontend:** HTML5, CSS3 (sin frameworks)
* **Pruebas:** `unittest` (Framework de pruebas de Django)

---

## 🚀 Instalación y Ejecución (Recomendado con Docker)

La forma más fácil y recomendada de ejecutar este proyecto es usando Docker y Docker Compose.

### Prerrequisitos
* [Git](https://git-scm.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Pasos

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/deyby01/blog-usuarios
    cd tu-repositorio
    ```

2.  **Configura las Variables de Entorno:**
    En el archivo `docker-compose.yml`, las credenciales de la base de datos se toman de variables de entorno. Crea un archivo llamado `.env` en la raíz del proyecto para definirlas.
    
    Crea un archivo `.env` y añade lo siguiente (puedes cambiar los valores si quieres):
    ```env
    POSTGRES_DB=blog_db
    POSTGRES_USER=blog_user
    POSTGRES_PASSWORD=blog_password
    ```
    *Este archivo `.env` ya está incluido en el `.gitignore` para no subir secretos al repositorio.*

3.  **Construye y levanta los contenedores:**
    Este comando construirá la imagen de Django y levantará los servicios de la aplicación web y la base de datos.
    ```bash
    docker-compose up --build
    ```
    *La primera vez puede tardar unos minutos mientras se descarga la imagen de PostgreSQL y se instalan las dependencias.*

4.  **Prepara la Base de Datos (en otra terminal):**
    Mientras los contenedores están corriendo, abre una **nueva ventana de terminal**, navega a la carpeta del proyecto y ejecuta los siguientes comandos para preparar la base de datos que vive dentro del contenedor:

    * **Aplica las migraciones:**
        ```bash
        docker-compose exec web python manage.py migrate
        ```
    * **Crea un superusuario** para acceder al panel de administración:
        ```bash
        docker-compose exec web python manage.py createsuperuser
        ```
        *(Sigue las instrucciones para crear tu usuario y contraseña).*

5.  **¡Listo!**
    * Tu aplicación de blog está corriendo. Puedes acceder a ella en [http://localhost:8000](http://localhost:8000).
    * El panel de administración está en [http://localhost:8000/admin/](http://localhost:8000/admin/).

---

## 🧪 Ejecutar las Pruebas

Para ejecutar el conjunto de pruebas automáticas, usa el siguiente comando mientras los contenedores están corriendo:

```bash
docker-compose exec web python manage.py test blog