import { Server as SocketIOServer } from 'socket.io';
import http from 'http';
import express from 'express';
import net from 'net';

const app = express();

const server = http.createServer(app);
const io = new SocketIOServer(server, {
    cors: {
        origin: '*',
    }
});

const client = new net.Socket();

// try to connect to python server until it is up
const connectToPythonServer = () => {
    client.connect(1234, 'python', () => {
        console.log('Connected al back de python, es decir al sv asincronico');
        client.write('Hello, server! Love, Client.');
    });
}

// try to connect to python server until it is up
client.on('error', (error) => {
    console.log('Error al conectar con el back de python, es decir al sv asincronico');
    console.log(error);
    setTimeout(connectToPythonServer, 1000);
});

connectToPythonServer();


// client.connect(1234, '127.0.0.1', () => {
//     console.log('Connected al back de python, es decir al sv asincronico');
//     client.write('Hello, server! Love, Client.');
// });

// client.on('data', (data) => {
//     console.log('Received: ' + data);

//     // func()
//     // socket.emit('message', " que hace perro");


// });

const func = () => {

    // TODO: en teoria se conecta nada mas con el back y se queda ahi, hasta que el front no se conecta no hace nada 
    io.on('connection', (socket) => {
        console.log('New client connected, se conecto uno desde el front');

        client.on('data', (data) => {

            // convert data to JSON
            data = JSON.parse(data);
            console.log(data.date, 'DATE')

            console.log('Received: ' + data + 'ahora se enviara esta data al front');
        
            // func()
            // socket.emit('message', data.toString());
            console.log('Emitido')
            // socket.emit('server:newVeil', data.toString());

            // send in json fomat
            socket.emit('server:newVeil', data);
        
        
        });


    
        // socket.emit('message', 'Que mande algo aunquesea no me importa la data');
        // console.log('Emitido');
    
        // socket.emit('message', " que hace perro");
    
        // write a global func to send message
    
    
        // sendToSocket(socket=socket);
    
        socket.on('disconnect', () => {
            console.log('Client disconnected');
        });
    });
}

func();

// const sendToSocket = (socket, data="La prueba default") => {
//     socket.emit('message', data);
// }

// io.on('connection', (socket) => {
//     console.log('New client connected');

//     // socket.emit('message', data);

//     // socket.emit('message', " que hace perro");

//     // write a global func to send message


//     sendToSocket(socket=socket);

//     socket.on('disconnect', () => {
//         console.log('Client disconnected');
//     });
// });


server.listen(8000, () => {
    console.log('Listening on port 8000');
});

