import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import io from 'socket.io-client'
import { MarketsComponent } from './components/markets'
import { Navbar } from './components/navbar'
import { AppRouter } from './router/AppRouter'
// import { client } from './common';

// const net = require('net').default;
// import net from 'net'

// const socket = io('http://127.0.0.1:8000')


function App() {


  const [msj, setMsj] = useState('')
  const [messages, setMessages] = useState([])

  // const [markets, setMarkets] = useState([])

  // useEffect(() => {

  //   console.log('useEffect')
    
  //   socket.on('message', (message) => {
  //     console.log(message, 'message')
  //     setMessages([...messages, message])
  //     setMsj(message)
  //   })

  //     return () => {
  //       socket.off()
  //     }

  // }, [])

  // const handleMarkets = (markets) => {

  // }

    // const getMarkets = async () => {

    //   console.log('Entro')

    //   const url = 'http://127.0.0.1:1234/api/open-markets'
    //   const resp = await fetch(
    //     url
    //   )
    //   const data = await resp.json();

    //   console.log(data, 'data')

    // }

    // getMarkets()
    
    return (
      // Hola {msj} 
      // <>
      //   <Navbar />
      //   <div className='container'>
      //   {
      //     <MarketsComponent />
      //   } 
      //   </div>
      // </>

      <>
        <AppRouter />
      </>
     

  )
}

export default App
