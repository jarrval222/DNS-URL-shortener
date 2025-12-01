# DNS-URL-shortener

Este proyecto es un acortador de URLs minimalista construido con Flask que utiliza los registros TXT del DNS (Domain Name System) para almacenar la asociación entre la URL corta (un subdominio) y la URL de destino. La gestión de los registros DNS se realiza mediante la API de IONOS.

## Estructura del Proyecto

El repositorio contiene los siguientes archivos clave:

app.py  La aplicación principal en Flask que gestiona la creación de URLs y la redirección.
.env    Archivo para almacenar la clave API de IONOS (IONOS_API_KEY) y el dominio (DOMAIN).
requirements.txt    Lista de paquetes de Python necesarios (requests, python-dotenv).
index.html  Contiene el frontend básico con un título y un formulario para acortar URLs.
README.md   Este documento.

## Configuración y Despliegue Paso a Paso

Sigue estos pasos para poner en marcha la aplicación.

1. Requisitos Previos
Asegúrate de tener instalado Python 3.

2. Instalación de Dependencias
Instala todas las librerías de Python listadas en requirements.txt, además de flask y dnspython que son necesarias para el código:

```bash
pip install flask requests python-dotenv dnspython
```

3. Configuración de Credenciales
El proyecto requiere credenciales para interactuar con la API de IONOS.

a. Archivo .env

El archivo .env proporcionado contiene las siguientes variables (mi clave API)

4. Ejecución

Inicia la aplicación Flask:

```bash
python app.py
```

## Detalles de Implementación (app.py)

El archivo app.py contiene la lógica central del acortador.

1. crear_url_corta(url_larga)
Esta función genera el código corto y crea el registro DNS.

Generación de Código: Utiliza hashlib.md5(url_larga.encode()).hexdigest()[:8] para generar un código corto de 8 caracteres.

Comunicación con IONOS:

Consulta el endpoint /zones para obtener el zone_id.

Crea un registro DNS con una petición POST al endpoint /zones/{zone_id}/records.

Registro Creado: Es de tipo TXT con el siguiente contenido:

name: {codigo}.{DOMAIN}

type: TXT

content: url_larga

2. obtener_url_destino(codigo)

Esta función resuelve el registro DNS para obtener la URL original.

Consulta DNS: Utiliza dns.resolver.resolve(f"{codigo}.{DOMAIN}", 'TXT') para buscar el registro TXT del subdominio.

Recuperación: Devuelve el contenido del registro TXT, que es la URL larga, tras eliminar las comillas (.strip('"')).
