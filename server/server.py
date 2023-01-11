import asyncio, os, json, datetime, random, string
from server.router import route, get_fun_by_route
from asyncio import sslproto, transports
from service.trader import Trader
from service.buyer import Buyer

class Request:

    def __init__(self, method, path, protocol, body):
        self.method = method
        self.path = path
        self.protocol = protocol
        self.body = body

    def __str__(self):
        return f'{self.method} {self.path} {self.protocol} {self.body}'

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def parcear(self, dato):
        try:
            encabezado = dato.decode().splitlines()[0]
            pedido = encabezado.split()
            body = dato.decode().splitlines()[-1]
        except:
            pass
        return(pedido, body)

    async def echo_handle(self, reader, writer):

        # how each new connection is handled
        try:
            addr = writer.get_extra_info('peername')
            print(f'[NEW] Connection from {addr}')
        except:
            pass

        data = await reader.read(10000)

        request, body = self.parcear(data)
        print(request, 'REQUEEEEST')
        request = Request(request[0], request[1], request[2], body)

        print(request.protocol, 'PROTOCOL')
        if request.protocol == 'HTTP/1.1':
            print('ES POR HTTP')
            pass
        else:
            print('ENTRA A SOCKETS, ES POR SOCKETS')
            try:

                try:
                    trader = Trader()
                    trader.writer = writer
                    print(trader.writer, 'writer que se crea en el server al momento se conecta el socket')
                    # buyer = Buyer()
                    # buyer.writer = writer
                    # print('socket', buyer)
                except Exception as e:
                    print(e)
                    pass

            except Exception as e:
                print(e)
            return


        # TODO: desacoplar los helpers para los types de request como GET, POST, PUT, DELETE
        if request.method == 'GET':
            print('Entro al GET')
            try:
                fun = get_fun_by_route(request.path)
                data = fun() # lo que devuelve el metodo en este caso devia ser el html
                print(data, 'ESTO LO IMPREME DESDE EL GET DEL SERVEr')


                try:
                    body = json.dumps(data).encode()
                except:
                    body = data
                
                respuesta = '200 OK'

                header = bytearray(
                    "HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html'
                    + "\r\nContent-length:" + str(len(body)) + "\r\nAccess-Control-Allow-Origin: *" + "\r\n\r\n", 'utf8'
                )

                writer.write(header)        #Enviamos la cabecera
                writer.write(body)          #Enviamos el body
                await writer.drain()        #Esperamos que todo se haya enviado
                writer.close()
            except:
                body = json.dumps({
                    'timestamp': str(datetime.datetime.now()),
                    'status': 404,
                    'error': 'Not Found',
                    'path': str(request.path)
                }).encode()
                respuesta = '404 Not Found'

                header = bytearray(
                    "HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html'
                    + "\r\nContent-length:" + str(len(body)) + "\r\nAccess-Control-Allow-Origin: *" + "\r\n\r\n", 'utf8'
                )

                writer.write(header)        #Enviamos la cabecera
                writer.write(body)          #Enviamos el body
                await writer.drain()        #Esperamos que todo se haya enviado
                writer.close()
    
        elif request.method == 'POST':
            fun = get_fun_by_route(request.path, request.method)
            # print(request.body, 'body')
            data = fun(request.body)
            print('is a post')

            otro = json.loads(body)

            body = json.dumps(data).encode()
            respuesta = '201 OK'

            # create a header with Access-Control-Allow-Origin: * and allow cors
            header = bytearray(
                "HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html'
                + "\r\nContent-length:" + str(len(body)) + "\r\nAccess-Control-Allow-Origin: *" + "\r\n\r\n", 'utf8'
            )

            writer.write(header)        #Enviamos la cabecera
            writer.write(body)          #Enviamos el body
            await writer.drain()        #Esperamos que todo se haya enviado
            writer.close()

    async def main(self):

        server = await asyncio.start_server(              
            self.echo_handle,
            self.host,
            self.port
        )

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:                              
            await server.serve_forever()

    def start(self):
        route()
        asyncio.run(self.main())
