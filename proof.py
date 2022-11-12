from iqoptionapi.stable_api import IQ_Option
import logging
import time
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
print("Accediendo...")
Iq=IQ_Option("s.fenske@alumno.um.edu.ar","perrito2")
Iq.connect()#connect to iqoption
goal="AUDCAD-OTC"
size="all"#size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
maxdict=10
print("Empezar stream...")
Iq.start_candles_stream(goal,size,maxdict)
#DO something
print("Hacer algo...")
time.sleep(10)

print("imprimir velas")
cc=Iq.get_realtime_candles(goal,size)
for k in cc:
    print(goal,"size",k,cc[k])
print("parar velas")
Iq.stop_candles_stream(goal,size)