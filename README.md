# LolWithMongo

**LolWithMongo** es una trabajo para la asignatura Complementos de Bases de Datos del grado de Ingeniería del Software de la Universidad de Sevilla. Consiste en un esfuerzo de investigación y experimentación centrado en la integración de la base de datos MongoDB con Django usando datos sobre League Of Legends competitivo.

## Instalación

Con el repositorio descargado en el equipo, es necesario crear un entorno virtual (requiere la instalación de Python) para poder ejecutarlo. Los pasos, en un equipo Windows, son los siguientes:
- Abrir la consola de comandos, navegar a un directorio donde se desee alojar el entorno virtual y ejecutar `python3 -m venv nombre-directorio`.
- Esto crea un carpeta *nombre-directorio*. Para activarlo, usar el comando `nombre-directorio\Scripts\activate.bat`.
- Una vez finalice todo el proceso (continua con las próximas líneas), se puede cerrar el entorno ejecutando `deactivate`.

El entorno virtual permitirá instalar todas las dependencias, que están disponibles en el archivo *requirements.txt* del directorio raíz del proyecto. Estando en ese directorio principal se debe:
- Lanzar el comando `pip install -r requirements.txt`.
- Una vez esté completado este paso, activar la base de datos de MongoDB y ejecutar `.\lolpedia\manage.py migrate` para realizar las migraciones.
- Por último, el comando `.\lolpedia\manage.py runserver` posibilitará interactuar con el sistema.

Tras todo ello, es posible acceder al mismo visitando [http://localhost:8000](localhost:8000). 

