<center><em><h3>Documentación del sistema como respuesta al reto</h3> <h1><bold> ¿Puedes recoger mi pedido?</bold></h1> </em></center>


## Tabla de Contenido
- [Tabla de Contenido](#tabla-de-contenido)
- [Descripción.](#descripción)
- [Tecnologias](#tecnologias)
- [Pre-requisitos.](#pre-requisitos)
- [Instalación.](#instalación)
- [Ejecución.](#ejecución)
- [Supuestos](#supuestos)
- [Funcionalidades](#funcionalidades)
- [Extras](#extras)


## Descripción.


## Tecnologias
- dj-rest-auth==2.2.5
- Django==4.1.2
- djangorestframework==3.14.0
- drf-yasg==1.21.4

## Pre-requisitos.
<p style="text-align: justify;">El software aqui mencionado se encuentra como requisito escencial para el cargue, descargue para el correcto funcionamiento de la prueba al sistema.</p>

- Git.
  - Link de descarga Linux/Windows: https://git-scm.com/
  
- Docker.
  - Link de descarga Linux/Windows : https://www.docker.com/

## Instalación.
 - Paso 1 - Clonar el Proyecto.

   <p style="text-align: justify;"> Elegir la carpeta o ruta de destino donde almacenar el codigo del repositorio correspondiente al sistema desarrollado, ejemplo. </p> 
    C:\Users\User\Desktop\your-path\

    - Abrir el CMD en windows o una TERMINAL en Linux.
    - Ejecutar el siguiente comando para acceder a la ruta donde quieres clonar el repositorio.

                    cd  + la ruta donde quieres que se clone el repositorio
                    Ejemplo : cd c:/users/user/desktop/../
    -  por ultimo clonar el proyecto.

                    git clone  https://github.com/EdwardPinzon13/test-orders.git
 - Paso 2.  - Selección de Base de Datos.
    <p style="text-align: justify;">
    En este paso se presentan dos caminos posibles,el primero es ejecutar el sistema con una Base de datos precargada en SQLite, donde se encuentran vacio los pedidos, pero cuenta con el resto de tablas tales como Brands(marcas), type-vehicle(Tipo de Vehiculo),vehicle(Vehiculo) correspondiendo a la información de los vehiculos y driver pertenecieente a la información de los conductores ya cargado.</p>

    - Opción 1 : Base de Datos pre-cargada.
      * Borrar el contenido dentro el archivo .docekerignore ubicado en la carpeta generada al clonar el repositorio.
      * Seguir al apartado A del paso 3 - Dockerización.

    - Opción 2 : Base de datos nueva.
      * Seguir al apartado B del paso 3 - Dockerización.

  - Paso 3. Dockerización.

    - <h3><strong>Apartado A - Dockerización.</strong></h3>

        Ejecutar los siguientes comandos en la terminal antes abierta ahora dentro de la carpeta creada producto de la clonación del repositorio. 
        - <strong>Construcción de la Imagen a base del Dockerfile.</strong>

               docker build --tag test-order .
        - <strong>Creación del Contenedor en donde se ejecutará la aplicación embebida con base a la Imagen creada con el comando anterior.</strong>

               docker run -d  --name "test-order-container" -p 8000:8000 test-order 

    <br>

    - <h3><strong>Apartado B - Dockerización.</strong></h3>

      Ejecutar los siguientes comandos en la terminal antes abierta ahora dentro de la carpeta creada producto de la clonación del repositorio. 
        - <strong>Construcción de la Imagen a base del Dockerfile</strong>.

               docker build --tag test-order .
        - <strong>Creación del Contenedor en donde se ejecutará la aplicación embebida con base a la Imagen creada con el comando anterior.</strong>

               docker run -d  --name "test-order-container" -p 8000:8000 test-order 
        - <strong>Entrar a la terminal propia para ejecutar los comandos a nivel de "maquina" interna en el contenedor.</strong>

               docker exec -it test-order-container /bin/sh
        - <strong>Ejecutar las migraciones internas en caso de ser necesario</strong>.

               python manage.py makemigrations
        - <strong>Ejecutar las migraciones para la creación de la Base de Datos con base a los Models de Django</strong>.

               python manage.py migrate
        - <strong> Creación de un usuario para iniciar sesión y lograr ejecutar los diferentes endpoints, ya que requieren de credenciales de Autenticación.</strong>

            Te solicitara un <strong>username</strong>/nombre de usuario con el cual iniciaras sesión , un correo electronico y una <strong>contraseña</strong>  como medida de credencial de acceso.

               python manage.py createsuperuser
        - <strong>Cargar los datos en las tablas de necesarias para la creación de vehiculos.</strong>

               python manage.py loaddata vehicles.json
        - </strong>Cargar los datos de los conductores.</strong>

               python manage.py loaddata driver.json
        - <strong>Ejecutar los Tests de las diferentes aplicaciones</strong>.

               python manage.py test applications

  - Paso 4. Servidor Local.
    Entrar a http://localhost:8000/ donde se te pedira que ingreses el username y password para iniciar sesión.
    <strong>Recordar</strong> que si creaste la base de datos, las credenciales corresponden al usuario que creaste.

    <strong>Si elegiste la opción de la Base de Datos Pre-cargada:</strong>

        - username: orderadmin
        - password: 1234
         
  - Paso 5. - Guardar KEY.
    AL iniciar sesión de forma correcta se te dara una key, dicha key guardarla, ya que con ella podremos ejecutar los servicios ofrecidos en el API.
      * Ejemplo:  key : f2361f32a188436fdb77f15292fe698698cdf72a
 
  - Paso 6. - Swagger.
    Swagger es el paquete elegido para la representación y documentación propia del API, en ella se especificaran los modelos, los endpoints ofrecidos como servicios y solución a los retos planteado, dichos retos se especifican en el apartado de funcionalidades.

      * Una vez guardada la KEY del paso anterior, dirigirnos a la siguiente url <strong> http://localhost:8000/swagger/ </strong> , en ella encontraremos todos los endpoints como funcionalidades/respuesta a los retos y algunos otros pertenecientes a los modelos que componen todo el API.

## Ejecución.
 <p style="text-align: justify;">
    Para le ejecución y prueba de las funcionalidades, se puede hacer directamente desde el link al SWAGGER presentado en el paso 6 del apartado anterior o ejecutar los endpoints desde el Cliente HTTP de su preferencia , dentro del repositorio se encuentra un archivo que corresponde a una Colección de postman con la cual podran ver los diferentes endpoints y ejemplos de como ejecutarlos de igual manera en la documentación del SWAGGER se encuentra especificado lo que se espera para cada campo y el cuerpo para realizar la solicitud al endpoint. </p>

- <strong>Autorización para acceso a los endpoints.</strong>
  - SWAGGER.
   
    Dentro del SWAGGER dirigirte al Botón  en la parte superior derech llamado <strong>Authorize</strong> , te pedira un valor, ese valor es la palabra Token con la T en mayúscula seguido de la KEY que nos dieron al iniciar sesión.

    Ejemplo.
        
        Token f2361f32a188436fdb77f15292fe698698cdf72a

  - POSTMAN - Cliente HTTP de tu elección.

   Dentro del cliente HTTP de preferencia dentro de los HEADERS  enviar la petición con el campo <strong>Authorization</strong> como clave y la palabra Token seguido de un espacio en blanco seguido de la Key como valor,

        Authorization  : Token f2361f32a188436fdb77f15292fe698698cdf72a

## Supuestos
<p style="text-align: justify;">1. Todo pedido efectuado, una vez registrado toma una hora su ejecución, ejemplo >  Hora de pedido 10:00:01 - Hora de Entrega 11:00:01 </P>
<p style="text-align: justify;">2. El sistema toma en cuenta la ultima posición registrada consultada al  servicio externo utilizado para tomar la posición del conductor. </p>



## Funcionalidades
- `Funcionalidad 1` : <strong>Agendar un pedido a un conductor en una fecha y hora, y especificar su lugar de
recogida (latitud y longitud) y destino</strong>
    - add-order
      - http://localhost:8000/add-order/
  
- `Funcionalidad 2` : 
  -  <strong>Consultar todos los pedidos asignados en un día en específico ordenados por la hora</strong>
  -  <strong>Consultar todos los pedidos de un conductor en un día en específico ordenados por la hora</strong>
     - <h3>filter-order</h3>
        Este servicio acepta la busqueda de un servicio especificando un driver/conductor, dando solución al apartado 2 de esta funcionalidad, como dato en común para las dos consultas el <strong>date</strong> como query params es obligatorio contrario al <strong>driver</strong> que es opcional. 
        
       - http://localhost:8000/filter-order/?date=&driver=

- `Funcionalidad 3` : <strong>Hacer búsquedas del conductor que esté más cerca de un punto geográfico en una
fecha y hora. (Tener en consideración los pedidos ya asignados al conductor).
</strong>
  - driver-certain
    - http://localhost:8000/driver-certain/

## Extras
- `Funcionalidad extra` : <strong>Agendar un pedido a un conductor seeleccionandolo automaticamente en una fecha y hora, y especificando su lugar de recogida (latitud y longitud) y destino.</strong>

    - add-order-dynamic
      - http://localhost:8000/add-order-dynamic/





