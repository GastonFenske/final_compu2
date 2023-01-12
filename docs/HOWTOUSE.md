# How to use

# Guia rapida para usar el sistema:

### [http://localhost:5173](http://localhost:5173) → Interfaz principal (por defecto)

### Una vez nos encontramos en la interfaz principal, nos logueamos con nuestras credenciales de IQ OPTION

El boton de **markets** nos permite comenzar a operar un mercado y setear cuando dinero queremos operar, tambien permite detener el mercado que se esta operando (es un switch)

El boton **real time** nos permite ver que esta haciendo el bot en tiempo real y si hay operaciones abiertas (tambien podemos ver las operaciones abiertas directamente en la app de iqoption en la web, smartphone o desktop)

El boton **operations log** nos permite acceder a todos los datos que hay guardados en la base de datos de nuestra operaciones ya concluidas

PD: si queremos ver las operaciones guardas y se queda cargando sin mostrarnos nada, lo mas probable es que haya una operacion abierta, cuando el socket de la api de iqoption se queda verificando el resultado de la operacion hasta que no se cierra no libera al hilo que esta usando nuestro sistema, apenas cierre la operacion se cargara aquello que estemos esperando (comprobar el resultado de una operacion abierta consume todo el hilo que esta usando nuestro sistema y hasta que no termina la operacion no queda libre).