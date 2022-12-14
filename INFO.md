# Diseño del sistema

## Python

Es un lenguaje sencillo, multiparadigma y actualmente en auge, además que es el lenguaje que más conocemos. Utilizado para el backend ya que contamos con librerías y módulos que nos facilitan el flujo de trabajo como lo son; celery, redis, PyMySQL, cryptography.

Además que utilizamos la api de la plataforma iqoption que esta desarrollada en python

### Celery y Redis

Usamos redis para el envio de tareas que nos pide el front y la procese el celery, realizando un cálculo constante y dejando que el usuario no tenga que hacer uso instensivo de su procesador

## React

Adoptamos react porque su reactividad en el front nos es muy benéfico ya que trabajamos con el mercado que se actualiza constantemente