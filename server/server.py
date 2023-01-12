import asyncio, json, datetime
from server.router import route, get_fun_by_route
from service.trader import Trader

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

        addr = writer.get_extra_info('peername')
        print(f'[NEW] Connection from {addr}')

        data = await reader.read(10000)

        request, body = self.parcear(data)

        request = Request(request[0], request[1], request[2], body)

        print(request.protocol, 'PROTOCOL')
        
        if request.protocol == 'HTTP/1.1':

            print('ES POR HTTP')
            methods = {
                'GET': self.get_handle,
                'POST': self.post_handle
            }
            fun_to_ex = methods[request.method]
            await fun_to_ex(request, writer)

        else:
            self.socket_handle(writer)

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

    def socket_handle(self, writer) -> None:
        print('ENTRA A SOCKETS, ES POR SOCKETS')
        try:
            trader = Trader()
            trader.writer = writer
            print(trader.writer, 'writer que se crea en el server al momento se conecta el socket')
        except Exception as e:
            print(e)
            pass

    async def post_handle(self, request, writer) -> None:

        print('Entro al POST')
        fun = get_fun_by_route(request.path, request.method)
        data = fun(request.body)
        body = json.dumps(data).encode()
        respuesta = '201 OK'

        header = bytearray(
            "HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html'
            + "\r\nContent-length:" + str(len(body)) + "\r\nAccess-Control-Allow-Origin: *" + "\r\n\r\n", 'utf8'
        )

        writer.write(header)        #Enviamos la cabecera
        writer.write(body)          #Enviamos el body
        await writer.drain()        #Esperamos que todo se haya enviado
        writer.close()

    async def get_handle(self, request, writer) -> None:

        print('Entro al GET')
        try:

            fun = get_fun_by_route(request.path)
            data = fun()

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

        except Exception as e:
            print(e)
            await self.not_found_handle(request, writer)


    async def not_found_handle(self, request, writer) -> None:

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


