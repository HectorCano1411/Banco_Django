# # Banco en Línea - README
![Screenshot 2023-09-09 133206](https://github.com/HectorCano1411/Banco_Django/assets/123791914/f67472d4-5e06-46cc-a0e5-8302c019a88f)

# Banco en Línea

# Insignias
# Estado del Proyecto
# Licencia

# Índice
# Descripción del Proyecto
# Estado del Proyecto
# Características de la Aplicación y Demostración
# Acceso al Proyecto
# Tecnologías Utilizadas
# Personas Contribuyentes
# Personas Desarrolladoras del Proyecto
# Licencia
# Conclusión

# Descripción del Proyecto
# El proyecto "Banco en Línea" es una aplicación web desarrollada en Django que permite a los usuarios acceder a sus cuentas bancarias en línea. Ofrece funciones de inicio de sesión personalizado, visualización de detalles de la cuenta, desbloqueo de cuentas (para administradores), y muestra la fecha y hora actual.

# Estado del Proyecto
# El proyecto se encuentra en estado activo y está en constante desarrollo y mejora. Se están implementando nuevas características y se abordan problemas reportados por los usuarios.

# Características de la Aplicación y Demostración
# Inicio de Sesión Personalizado: Los usuarios pueden iniciar sesión utilizando su RUT y contraseña. La aplicación verifica la autenticación y gestiona el bloqueo de cuentas después de varios intentos fallidos.
![Screenshot 2023-09-09 150953](https://github.com/HectorCano1411/Banco_Django/assets/123791914/ae97f9d9-0597-4bf0-a6e3-636fedee3f61)

# Visualización de Detalles de la Cuenta: Los usuarios pueden ver los detalles de su cuenta, incluyendo saldo disponible, saldo contable, retenciones, total de cargos y total de abonos.
![Screenshot 2023-09-09 180317](https://github.com/HectorCano1411/Banco_Django/assets/123791914/53c56e81-d17d-4521-81dc-177b555accd3)

# Desbloqueo de Cuentas (Para Administradores): Los administradores pueden desbloquear cuentas de usuario bloqueadas a través de una función dedicada.
![Screenshot 2023-09-09 151027](https://github.com/HectorCano1411/Banco_Django/assets/123791914/8daafac2-3b86-41e3-b8e7-d8c7f4c229ce)

# Seguimiento y control de inicio de sesion
![Screenshot 2023-09-09 151050](https://github.com/HectorCano1411/Banco_Django/assets/123791914/8b663a5b-d7ef-4187-a9a3-c4619b3f08be)

# Demostración: Enlace a la Demo

# Acceso al Proyecto
# Para acceder al proyecto y probarlo en tu entorno local, sigue estos pasos:
# si no tienes instalado Git En Ubuntu lo puedes hacer con el siguiente comando
# Abre una terminal en tu sistema Ubuntu.
# sudo apt update 
# sudo apt install git
# git version (verificar la versión que fue instalada)
# configura tu nombre de usuario y correo electrónico para utilizar Git a nivel global
# git config --global user.name "Tu Nombre" 
# git config --global user.email "tu@email.com"

# Abre una terminal en tu sistema Ubuntu.
# Asegúrate de tener pip instalado. Si no lo tienes, puedes instalarlo con el siguiente comando:
# sudo apt-get install python3-pip
# Para instalar Django en Ubuntu, puedes utilizar el administrador de paquetes pip, que es una herramienta de Python utilizada para instalar paquetes y bibliotecas. Aquí tienes la sintaxis para instalar Django en Ubuntu:
# Abre una terminal en tu sistema Ubuntu.
# Asegúrate de tener pip instalado. Si no lo tienes, puedes instalarlo con el siguiente comando:
# pip3 install Django

# Luego, puedes instalar Django utilizando pip. Para instalar la última versión estable de Django, simplemente ejecuta:

# Para activar un entorno virtual llamado venv en Ubuntu, debes usar el comando source o simplemente el punto (.). Asumiendo que tienes un entorno virtual llamado venv, puedes activarlo de la siguiente manera:
# Abre una terminal en Ubuntu.
# Navega hasta la ubicación donde se encuentra tu entorno virtual. Por ejemplo, si tu entorno virtual venv se encuentra en el directorio /ruta/a/venv, puedes navegar allí utilizando el comando cd
# cd /ruta/a/venv
# Una vez que estés en el directorio que contiene tu entorno virtual, puedes activarlo utilizando el comando source o el punto (.) seguido del script activate dentro del directorio bin del entorno virtual:
# Usando source
# source   venv/bin/activate
# Después de activar el entorno virtual, verás el nombre del entorno virtual en el indicador de tu terminal, lo que indica que el entorno virtual está activo. Esto significa que cualquier paquete o herramienta que instales ahora se instalará en el entorno virtual en lugar de en el sistema global.

# Clona el repositorio desde Ubuntu: sudo git clone https://github.com/HectorCano1411/Banco_en_Linea_Django_Python
# Para levantar un proyecto de Django en Ubuntu, primero debes asegurarte de que estás en el directorio raíz de tu proyecto Django (donde se encuentra el archivo manage.py). Luego, puedes usar el siguiente comando para iniciar el servidor de desarrollo de Django:
# python manage.py runserver
# Asegúrate de tener activado tu entorno virtual (si estás utilizando uno) antes de ejecutar este comando. Esto iniciará el servidor de desarrollo de Django en el puerto predeterminado 8000. Si deseas especificar un puerto diferente, puedes hacerlo de la siguiente manera:
# python manage.py runserver 8080
# Esto iniciará el servidor en el puerto 8080. Una vez que el servidor esté en funcionamiento, podrás acceder a tu aplicación Django en un navegador web visitando http://localhost:8000 (o el puerto que hayas especificado) en tu máquina Ubuntu.
# Recuerda que el servidor de desarrollo de Django es adecuado para el desarrollo y pruebas locales, pero no se debe utilizar en producción. Para implementar una aplicación Django en producción, se recomienda utilizar un servidor web como Nginx o Apache junto con Gunicorn o uWSGI.
# Para instalar los paquetes especificados en un archivo requirements.txt en Ubuntu, puedes utilizar el siguiente comando en el directorio donde se encuentra el archivo requirements.txt:
# pip install -r requirements.txt
# Asegúrate de que tu entorno virtual (si estás utilizando uno) esté activado antes de ejecutar este comando para que las bibliotecas se instalen en el entorno virtual en lugar de globalmente en tu sistema. Si no tienes un entorno virtual configurado, es una buena práctica crear uno antes de instalar las dependencias de tu proyecto Django.
# Para desactivar el entorno virtual cuando hayas terminado de trabajar en él, simplemente ejecuta el comando deactivate en la misma terminal:

# Credenciales para entrar al administrador
# RUT 12345678
# CLAVE 12345678

# Tecnologías Utilizadas
# Django
# Python
# HTML/CSS
# Bootstrap
# Base de Datos (Configuración según elección)

# Personas Contribuyentes https://github.com/HectorCano1411
# Nombre del Contribuyente linkedin.com/in/héctorcanoleal
# Nombre del Contribuyente hectorcanolealestudios@gmail.com

# ¡Agradecemos a todos los que han contribuido al proyecto!

# Personas Desarrolladoras del Proyecto
# Hector Cano Leal- Desarrollador Principal

# Licencia
# Este proyecto está bajo la Licencia MIT.

# Conclusión
# "Banco en Línea" es una aplicación web robusta que ofrece a los usuarios la capacidad de acceder y gestionar sus cuentas bancarias en línea de manera segura. Siéntase libre de contribuir al proyecto o utilizarlo para sus propios fines. ¡Gracias por su interés en nuestro proyecto!
