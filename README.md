# Operation Patch Request

Este proyecto busca regularizar notificaciones de cambios de estado de ASD que, al enviar requests con combinaciones desconocidas por la DB, no se procesaron correctamente.

## Requerimientos técnicos

- Python3
- Pip
- libpq-dev
- psycopg2
- requests
- sshtunnel
- python-dotenv 
- pytz

## Variables de entorno

1. En el .env se debe indicar segun corresponda al entorno

- Linux: Corresponde si tu ambiente local de desarrollo es alguna distribución de Linux
- Windows: Corresponde si tu ambiente local de desarrollo es Windows
- AWS: Corresponde si ejecutarás en la nube de AWS

```
ENVIRONMENT= [LINUX | WINDOWS | AWS]
```

## Ejecucion del programa

1. Se debe ejecutar el script run.sh

```
$ sh ./run.sh {INDICA-EL-ENVIRONMENT-DE-EJECUCION}
```
Por ejemplo, es estás ejecutando localmente en WINDOWS:

```
$ sh ./run.sh WINDOWS
```

## Despliegue

Para el despliegue se envían todos los archivos del proyecto al servidor EC2.

Se utiliza el hook post-receive de Git Bare.

Cuando se está con una versión estable del proyecto, se debe consolidar en el branch de nombre *main* y hacer push hacia el remoto *server*.  
El funcionamiento de lo anterior se explicará en los siguientes puntos.

### Git bare
Es un repositorio Git creado sin un working tree, a diferencia de los repositorios Git como Gitlab o Github, y se utiliza para configurar un servidor como si fuera un remoto de nuestro proyecto local. Esto no reemplaza el uso de plataformas como Gitlab.

Esto nos permite subir cambios a nuestro servidor e incluso desplegar la ejecución solamente haciendo push hacia el remoto Git Bare.

#### Setup de Git Bare en Operation Patch Request

*Estos pasos ya fueron realizados, por lo que no es necesario repetirlos en el ambiente de desarrollo. Se exponen para que conozcas el proceso y lo implementes en otros proyectos similares.*

1. Debes ingrear al servidor donde desplegarás este proyecto.
2. En el root del servidor debes crear un directorio para hacer los hooks del repositorio remoto. Se debe ejecutar estos comandos:

```
# creamos directorio
$ mkdir operation-patch-request.git

# nos movemos al directorio
$ cd operation-patch-request.git

# inicializamos el repositorio como git bare
$ git init --bare
```

3. Luego, en tu repositorio local (operation-patch-request), debes añadir el servidor y la ruta hacia el directorio creado, de la misma forma en la que añadirías un remoto de Gitlab. 

```
$ git remote add server {server-user}@ec2-xx-xx-xx-xx.compute-1.amazonaws.com:/home/{server-user}/operation-patch-request.git
```

4. Ahora debes volver al servidor e ingresar a la carpeta .git creada y entrar al directorio /hooks

```
$ cd operation-patch-request.git/hooks
```

Debes buscar el archivo post-receive.sample y eliminarlo

```
$ rm -rf post-receive.sample
```
Y ahora debes crear un nuevo archivo
```
$ sudo touch post-receive
```
Abres el archivo con
```
$ sudo nano post-receive
```

Dentro de post-receive pegas este script:

```
#!/bin/bash
echo "post receive desde servidor con operation-patch-request.git"
deployDir="../deploy"
TEMP="/home/admin/operation-patch-request"
GIT_DIR="/home/admin/operation-patch-request.git"
echo "ejecutando comando ls"
ls
echo "-------------------------"
while read oldrev newrev ref
do
    branch="main"
    if [ "$ref" == "refs/heads/main" ]; then
        mkdir $TEMP
        git --work-tree=$TEMP --git-dir=$GIT_DIR checkout -f main
        cd $TEMP
    fi
done

```

5. Ahora vuelves a tu máquina local y creas una rama de nombre *main*.  Haces commit, y antes de hacer push, debes fijarte de hacerlo así: 
   
```
$ git push -u server main
```

Si todo está OK verás cómo el servidor recibe tus cambios exitosamente, de la misma manera en la que ocurriría con un remoto de Gitlab.  Además verás el mensaje *post receive desde servidor con operation-patch-request.git*

6. Para corroborar lo anterior, debes volver al servidor remoto y en el *root* hacer el comando *ls* y encontrar el directorio operation-patch-request y operation-patch-request.git


## Estructura del repositorio

Aquí se describe los directorios y archivos principales.  Los archivos que no se mencionan no son relevantes (todavía) para el proyecto.

### /root

Directorio principal.

#### main.py

Script principal.  Toma de la DB original de misuper todos los requests, responses, ms_entry_id de todos los requests de ASD erróneos.

Luego los inserta en una nueva tabla intermedia llamada api_patches_logs.

Posteriormente, se toma todos los registros de la tabla intermedia y se reenvía a la api los requests mal procesados.

Finalmente, en la tabla notificaciones, se reemplaza la fecha con la que quedó el nuevo cambio de estado, con la fecha original e inicial, correspondiente a la fecha de los requests erróneos.

#### load_sp.py

Este script ejecuta un procedimiento almacenado en la DB que permite automatizar el ingreso de cambios de estado.  Se requiere generar un CSV como se indica en el CSV de ejemplo para un resultado óptimo.

### /credentials

Este directorio contiene un archivo .env con variables de entorno que se deben setear previo a la ejecución de main.py

### /db

Directorio con los scripts necesarios para conectarse al tunel de la DB, a la DB, scripts SQL y funciones en Python que operan en la DB.

### /service

#### api.py
Contiene las funciones que realizan llamados a la API.

### /utils

#### env.py

Archivo Python que lee y exporta las variables de entorno para disponibilizarla a los demás módulos.

#### utils.py

Archivo que contiene funciones auxiliares para el proceso.

### /settings

Directorio que controla cómo debe ser la ejecución del script según el ambiente de operación: si es el local del desarrollador, el ambiente de desarrollo o el ambiente productivo.
