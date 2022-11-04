## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)

en general-info describir toda la prueba, los endpoints que se tienen, los servicios, los supuestos que se tomaron
en teconologias hablar de que tecnologias se usar y para que
en instalación es que lo más importante, hablar quee se debe clonar el repo - colocar link al repo,
decir en general infor los prerequisitos como tener instalado GIT, DOCKER.
una vez clonado ejecutar el comando de docker, antes de eso pararse en la direcci;on donde esta el archivo de docker file
cd ..carpeta hasta llegar al directorio donde se encuentra el docker file, aqui colocar el cd/home y la direccion que queda al descargarlo/clonarlo.

por si se desea trabajar con una BD precargada

borrar el contenido del archivo .dockerignore  si no obviar este apartado


comando de docker para crear la imagen docker build --tag test-order .
comando de docker para crear el contenedor docker run -d  --name "test-order-container" -p 8000:8000 test-order


por si trabaja una nueva BD 
docker exec -it test-order-container /bin/sh comando para entrar dentro del contenedor
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser aqui decir que le solicitara nombre de usuario que es con el que iniciara sesión
seguido del correo electronico y una contraseá de igual manera para iniciar sesion
python manage.py loaddata vehicles.json comando para cargar los vehiculos
python manage.py loaddata driver.json comando para cargar los driver / conductores
python manage.py test applications por si se requieren cargar los unit test


en ejecucion colocar que si haya trabajado con una nueva BD o la precargada
al ir al localhost:8000
le pedira iniicar sesión, una vez inicie sesión copiar la key que le da y guardarla
mostrar un ejemplo de key 
ir a localhost:8000/swagger/  donde encontrara toda la documentación del api, puede trabajar desde ahí o utilizar la coleccion de postman que le cargare 
donde dice Authorization colocar la palabra Token seguido de un espacio en blanco seguido de la KEY que se le asigno al iniciar sesión
ejemplo Token Key