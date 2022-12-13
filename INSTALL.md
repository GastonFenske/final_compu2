# INSTALACIÓN (SOLO SISTEMAS UNIX)

## Docker

Tener instalado docker de no ser así siga los pasos a continuación

- Abrir la terminal

```bash
sudo apt update
sudo apt install docker.io
```
Verificar si se instaló correctamente

```bash 
docker
```
o tambien verificando la version
```bash 
docker --version
```
luego de confirmar que tenemos docker en nuestra máquina ejecutar el contenedor docker del proyecto

```bash 
docker run tradingbot
```
