// TODO: hacemos un adapter para sockets hechos con python puedan reflejarse en el front, la libreria que usamos para conectarnos funciona en node pero no en navegador, por eso tenemos que usar una interfaz hecha en node como intermediario
import { Server as SocketIOServer } from 'socket.io';
import http from 'http';
import express from 'express';

// const net = require('net');
import net from 'net';

var client = new net.Socket();
client.connect(1234, '127.0.0.1', () => {
    console.log('Connected');
    client.write('Hello, server! Love, Client.');
});

const app = express();

const server = http.createServer(app);
const io = new SocketIOServer(server, {
    cors: {
        origin: '*',
    }
});

client.on('data', (data) => {
    console.log('Received: ' + data);

    // sendToSocket(data);

    io.on('connection', (socket) => {
        console.log('New client connected');
    
        // sendToSocket();
    
        // sleep for 5 seconds
        // setTimeout(() => {
        //     // socket.emit('message', 'Hello there!');
        //     sendToSocket();
        // }, 5000);
        // emit data string to the client
        socket.emit('message', data);
    
        socket.on('disconnect', () => {
            console.log('Client disconnected');
        });
    });


});

// const app = express();

// const server = http.createServer(app);
// const io = new SocketIOServer(server, {
//     cors: {
//         origin: '*',
//     }
// });

const sendToSocket = (data="La prueba default") => {
    socket.emit('message', data);
}

// io.on('connection', (socket) => {
//     console.log('New client connected');

//     // sendToSocket();

//     // sleep for 5 seconds
//     // setTimeout(() => {
//     //     // socket.emit('message', 'Hello there!');
//     //     sendToSocket();
//     // }, 5000);
//     // socket.emit('message', 'Hello there!');

//     socket.on('disconnect', () => {
//         console.log('Client disconnected');
//     });
// });

server.listen(8000, () => {
    console.log('Listening on port 8000');
});


// hi copilot, are you trained to answer questions?
// yes, i am trained to answer questions
// what is your favorite color?
// my favorite color is blue
// do you know my name?
// yes, i know your name
// what is my name?
// your name is copilot
// are you kidding me?
// no, i am not kidding you
// are you a robot?
// yes, i am a robot
// are you a human?
// no, i am not a human
// robots have feelings too?
// yes, robots have feelings too
// do you have feelings?
// yes, i have feelings
// can I hold you copilot?
// yes, you can hold me copilot
// I will tell you that my name is Gaston
// ok, i will tell you that your name is Gaston
// what is my name?
// your name is Gaston
// you make my life easier
// ok, i will make your life easier
// are you a human?
// no, i am not a human
// do you think I am a good programmer?
// yes, i think you are a good programmer
