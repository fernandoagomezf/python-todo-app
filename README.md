# Aplicación TO-DO en Python

Una aplicación escrita en python para gestionar una lista de tareas pendientes por realizar. Es parte de mi ruta de aprendizaje de este lenguaje.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## Características

La aplicación utiliza una línea de comandos para recibir instrucciones. En general, la aplicación permite realizar las siguientes acciones: 
* Añadir, editar y eliminar una tarea.
* Ver las tareas existentes en una vista de tabla.
* Rastrear el progreso de una tarea (desde 0% hasta 100%).
* Promover o degradar la importancia de una tarea.
* Gestión automática del estado: 
    - 0% - _Pending_ (pendiente)
    - 100% - _Completed_ (completado)
    - Cualquier punto intermedio - _In Progress_ (en progreso).
* Indicadores gráficos colorizados por el indicador de la tarea.

### Comandos disponibles

| Comando       | Descripción |
|------------   |------------|
| **add**       | Crear una nueva tarea, ingresando el asunto, la fecha de vencimiento y las notas. |
| **show**      | Muestra todas las tareas en una vista de tabla, incluyendo un ícono que indica si una tarea está retrasada o no. |
| **detail**    | Consultar información adicional y detallada sobre una tarea específica. |
| **edit**      | Modificar una tarea existente, cambiando el asunto, la fecha de vencimiento o las notas. |
| **delete**    | Elimina una tarea completamente, no puede ser recuperada posteriormente. |
| **progress**  | Permite reportar cambios en el progreso de una tarea; usa 0 para marcarla como pendiente y 100 para marcarla como completada. |
| **promote**   | Incrementa la prioridad de una tarea: si está en baja, la cambia a normal, y de normal la cambia a alta. |
| **demote**    | Decrementa la prioridad de una tarea: si está en alta la cambia a normal, y si está en normal la cambia a baja.|
| **clear**     | Limpia la pantalla de contenido. |
| **help**      | Muestra los comandos disponibles junto con una breve descripción de qué hacen. |
| **exit**      | Termina la aplicación. |


## Especificaciones técnicas

### Dependencias

La aplicación está constuída y probada con Python 3.13. Utiliza los siguientes paquetes:
* sqlite3 - persiste los datos en una base de datos contenida en un archivo local llamado "todo.db". 
* pandas - se utiliza el componente DataFrame, que contiene los datos de las tareas y facilita su manipulación; asimismo permite cargar y guardar desde y hacia el disco duro. 
* tabulate - permite darle formato de tabla a la vista principal.
* colorama - se utiliza para codificar el color de los caracteres mostrados en la vista de tabla. 

**Instalar dependencias**:

    pip install pandas sqlite3 tabulate colorama

**Ejecutar la aplicación**:
    
    python main.py

### Base de atos

La aplicación almacena todos los datos en una base de datos local de SQLite 3, la cual se guarda como un archivo llamado "todo.db". Los datos son cargados y guardados utilizando los métodos de DataFrame, y son sobreescritos cada vez que se guarda. Debido a que es un proyecto pequeño, se puede tolerar esta pequeña ineficiencia. 

La base de datos utiliza el siguiente esquema:

    CREATE TABLE tasks (
        id TEXT PRIMARY KEY,
        code TEXT,
        subject TEXT,
        due_date TEXT,
        status INTEGER,
        priority INTEGER,
        progress REAL,
        notes TEXT
    )

Si la base de datos no existe, la aplicación la recreará automáticamente. 

### Arquitectura

La aplicación utiliza línea de comandos, y no se le añadirá una interfaz de usuario adicional a la terminal. 

![alt text](./architecture.svg)

Los datos son persistidos en una base de datos local en SQLite 3. Los datos son cargados cuando la aplicación inicia, y se mantienen en un DataFrame de Pandas. Cuando se hace una modificación, el DataFrame se salva completamente. 

## Versiones

v0.1 Primera versión, toda la aplicación está en un archivo utilizando solo funciones. Quizás en el futuro refactorizar hacia clases y añadir un enfoque estructurado.  