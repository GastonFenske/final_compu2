# INSTALL

# Descargar el respositorio

Abrir una terminal y ejecutar el siguiente comando

```powershell
git clone https://github.com/GastonFenske/final_compu2.git
```

# Instalacion

## ⚠️ Hay que tener Docker en el sistema operativo local

1. Crear un archivo .env en base al archivo .env-example de este repositorio (recomendamos dejar los valores que trae por defecto, sobre todo porque en el front la conexion al back esta estatica). Solo agregarle una contraseña a la base de datos MySQL en el campo **DB_PASSWORD**
2. Ejecutar el archivo docker-compose.yaml con el siguiente comando (tenemos que estar situados en el path donde se encuentra este archivo, para comprobar que nos encontramos en el mismo lugar que el archivo podemos ejecutar un **ls** en la terminal): 

```powershell
docker compose up
```

Se comenzara a instalar el sistema completo (puede tardar unos minutos)

Una vez los 6 contenedores esten arriba ya se podra utilizar el sistema

Por defecto en la direccion para acceder a la interfaz del sistema es: [http://localhost:5173](http://localhost:5173)