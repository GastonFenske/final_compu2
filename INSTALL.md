# INSTALACIÓN (SOLO SISTEMAS UNIX)

## Docker

Tener instalado docker de no ser así siga los pasos a continuación

Visitar la página oficial de docker 

https://docs.docker.com/desktop/install/linux-install/

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
docker compose up
```

## Celery
En la carpeta 'service' ejecutamos el siguiente comando
```bash
bash worker.sh
```

## Servidor backend
En la carpeta principal (final_compu2)
```bash 
bash boot.sh
```

## React
En la carpeta 'front' 
```bash 
bash boot.sh
```

## Node
En la carpeta 'utils'
```bash 
bash boot.sh
```
