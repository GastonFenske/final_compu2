# FINAL

![compu2dark.png](FINAL%20c529cb82acb3484cbef94c920f787d70/compu2dark.png)

La aplicacion se basa en un servidor concurrente asincronico que recibe datos de la api de IQ_OPTION, analiza los datos y segun diferentes parametros que el usuario establece compra a la baja o a la alza. Los datos de las operaciones se guardan en una base de datos MySQL

Se utiliza un pool of workers (paralelismo) para analizar difentes mercados a la vez, y operarlos en caso de que se den los patrones preestablecidos para operar, la aplicacion puede estar analizando horas hasta que los graficos muestren un patron donde la probabilidad de beneficio sea alta.

La aplicacion al analizar un mercado solicita informacion en tiempo real de las velas (graficos) a la api de IQ_OPTION, la api del broker devuelve en forma de JSON la informacion de una o mas velas. La aplicacion utilizando las librerias numpy y matplotlib grafica y analiza los datos y si los datos conciden con los parametros establecidos por el usuario la aplicacion opera.

Cuando se realiza una operacion la misma y su resultado se guardan en la base de datos

La aplicacion cuenta con el uso de sockert para la api, el uso de celery o multiprocessing para analizar los mercados, docker y alguna tecnologia para el front y trataremos de desplegarlo para que la aplicacion pueda estar activa 24/7

# Front:

- Contiene el inicio de sesion
- Tiene los botones para configurar cuando operar
- Muestra los mercados abiertos y los mercados en los que se esta operando
- Muestra la cantidad de dinero
- Las ultimas operaciones

# BD:

- Los datos de los usuarios administradores
- Los datos de las operaciones (monto, fecha, si se gano o perdio)
- Tablas:
    
    
    | id | nombre | apellido | username | password | rol | email |
    | --- | --- | --- | --- | --- | --- | --- |
    
    | id | fecha | resultado | monto operado | mercado | beneficio | abierto | cerrado | tiempo | ventaja |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

# API:

- Extraer datos de la api de iqoption, los analiza se fija si compra o vende en un x mercado, entrega los datos al front y guarda datos en la BD, se comunica con celery para calcular cuando operar

# Pool of workers:

- Analiza los diferentes mercados en tiempo real