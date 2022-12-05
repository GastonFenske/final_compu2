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
client.connect(1234, '127.0.0.1', () => {
    console.log('Connected');
    client.write('Hello, server! Love, Client.');
});

// client.on('data', (data) => {
//     console.log('Received: ' + data);

//     // func()
//     // socket.emit('message', " que hace perro");


// });

const func = () => {
    io.on('connection', (socket) => {
        console.log('New client connected');

        client.on('data', (data) => {
            console.log('Received: ' + data);
        
            // func()
            socket.emit('message', data.toString());
        
        
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
    console.log('Listening on port 3000');
});

