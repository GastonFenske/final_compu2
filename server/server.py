import asyncio, os, json, datetime
from server.router import route, get_fun_by_route

def parcear(dato):
    try:
        encabezado = dato.decode().splitlines()[0]
        pedido = encabezado.split()
        body = dato.decode().splitlines()[-1]
    except:
        pass
    return(pedido, body)

class Request:

    def __init__(self, method, path, protocol, body):
        self.method = method
        self.path = path
        self.protocol = protocol
        self.body = body

    def __str__(self):
        return f'{self.method} {self.path} {self.protocol} {self.body}'


async def echo_handle(reader, writer):

    data = await reader.read(10000)
    request, body = parcear(data)
    request = Request(request[0], request[1], request[2], body)

    # TODO: desacoplar los helpers para los types de request como GET, POST, PUT, DELETE
    if request.method == 'GET':
        print('Entro al GET')
        try:
            fun = get_fun_by_route(request.path)
            data = fun()
            print(data)
            body = json.dumps(data).encode()
            respuesta = '200 OK'
            header = bytearray(
                "HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html'
                + "\r\nContent-length:" + str(len(body)) + "\r\n\r\n", 'utf8'
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
                + "\r\nContent-length:" + str(len(body)) + "\r\n\r\n", 'utf8'
            )
            writer.write(header)        #Enviamos la cabecera
            writer.write(body)          #Enviamos el body
            await writer.drain()        #Esperamos que todo se haya enviado
            writer.close()


    # if consulta[0] == 'GET' and consulta[1] == '/alumnos':
    #     print('is a get')


    #     alumnos = [
    #         {
    #             'nombre': 'Juan',
    #             'apellido': 'Perez',
    #             'edad': 20
    #         },
    #         {
    #             'nombre': 'Maria',
    #             'apellido': 'Gomez',
    #             'edad': 21
    #         },
    #         {
    #             'nombre': 'Pedro',
    #             'apellido': 'Gonzalez',
    #             'edad': 22
    #         }
    #     ]
        
    #     # body = b'Hello, world!'
    #     body = json.dumps(alumnos).encode()
    #     respuesta = '200 OK'
    #     header = bytearray(
    #         "HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html'
    #         + "\r\nContent-length:" + str(len(body)) + "\r\n\r\n", 'utf8'
    #     )

    #     writer.write(header)        #Enviamos la cabecera
    #     writer.write(body)          #Enviamos el body
    #     await writer.drain()        #Esperamos que todo se haya enviado
    #     writer.close()

    elif request[0] == 'POST':
        print('is a post')
        print(body, 'el body que llega')
        print(type(body), 'el tipo de body')
        otro = json.loads(body)
        print(otro, 'el body convertido a diccionario')
        print(type(otro), 'el tipo de body convertido a diccionario')
        body = b''
        respuesta = '201 OK'
        header = bytearray(
            "HTTP/1.1 " + respuesta + "\r\nContent-type:" + 'text/html'
            + "\r\nContent-length:" + str(len(body)) + "\r\n\r\n", 'utf8'
        )
        writer.write(header)        #Enviamos la cabecera
        writer.write(body)          #Enviamos el body
        await writer.drain()        #Esperamos que todo se haya enviado
        writer.close()

host = '127.0.0.1'
port = 1234


async def main():

    server = await asyncio.start_server(              
        echo_handle,
        host,
        port
    )

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:                              
        await server.serve_forever()


def server():
    route()
    asyncio.run(main())

# if __name__ == '__main__':
#     route()
#     asyncio.run(main()) 