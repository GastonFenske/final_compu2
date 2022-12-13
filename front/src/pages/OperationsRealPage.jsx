import React, { useEffect, useState } from 'react'
import { Navbar } from '../components/navbar'
// import { getNewInfo } from '../helpers/getNewInfo'
import io from 'socket.io-client'


// const socket = io('http://127.0.0.1:8000')

export const OperationsRealPage = () => {


    const [msj, setMsj] = useState('nada')
    const [messages, setMessages] = useState([])
    // const [operationInfo, setOperationInfo] = useState({})

    const [operations, setOperations] = useState([])
    const [ids, setIds] = useState([])
    const [newOperations, setNewOperations] = useState([])

    const getOperations = async () => {
      // setLoading(true);
      const url = 'http://127.0.0.1:1234/api/operations-pending'
      const resp = await fetch(url)
      const data = await resp.json();
      setOperations(data.operations);
      // setLoading(false);
      console.log(operations, 'operations')
    }

    const getInfo = () => {
        // console.log('Entra al get info')
        // const msj = await getNewInfo()

        const socket = io('http://127.0.0.1:8000')



        // socket.on('message', (message) => {
        //     console.log(message, 'message que llega desde el server asyncio')
        //     setMessages([...messages, message])
        //     setMsj(message)
        //     // disconnect socket
        //     // socket.disconnect()
        // })

        socket.on('server:newVeil', (message) => {
          // conver message str to json

          // console.log(message, 'message que llega desde el server asyncio')
          // const este = JSON.parse(message)
          // console.log(este, 'este')

          setNewInfo(message)

          // convert message to str
          // message = JSON.stringify(message)



          // message = '"' + message + '"'

          // const otro = JSON.parse(message)
          // console.log(otro, 'otro')
          // ver el tipo de dato que es otro
          // console.log(typeof otro, 'tipo de dato')
          // const otro2 = JSON.stringify(otro)
          // console.log(otro2, 'otro strignify')

          // console.log(message, 'vela nueva json nuevo')
          // console.log(message, ' json nuevo')
          // setMessages([...messages, message])
          // setMsj(message)
        })

        return socket

        // console.log(msj, 'El mensaje que llega')
        // setMessages([...messages, msj])
        // setMsj(msj)
    }

    // const handleNewOperation = (data) => {

    //   const newOperations = operations.map((operation) => {

    //     if (operation.id === data.id) {
    //       return {
    //         ...operation,
    //         state: data.state,
    //         profit: data.profit,
    //         message: data.message
    //       }
    //     }
    //     return operation
    //   })

    //   setOperations(newOperations)

    // } 

    const setNewInfo = (data) => {

      if (data.type === 'new_veil') {
        data = JSON.stringify(data)
        setMessages([...messages, data])
        setMsj(data)

      } else {

        if (ids.includes(data.id)) {
          console.log('Llega una operacion que ya existe')

          const newOperations = operations.map((operation) => {

            if (operation.id === data.id) {

              return {
                ...operation,
                state: data.state,
                profit: data.profit,
                message: data.message
              }
            }
            return operation
          })

          setOperations(newOperations)

          return
        }
  
        setOperations([...operations, data])
        setIds([...ids, data.id])

 


      }

        // setOperations(operations)
  
        // if (ids.includes(data.id)) {
        //   console.log('Llega una operacion que ya existe')
        //   return
        // }  


        // console.log('Llega una operacion nueva')
        // setOperations([...operations, data])
        

        


        // setOperations([...operations, data])
        // setOperationInfo(data)
        // console.log(data, 'operation')
        // console.log(operations)


      }



    // update operations in DOM
    // useEffect(() => {
    //   // console.log(operations, 'operations')
    // }, [operations])


    // const disconnectSocket = () => {
    //   socket.disconnect()
    // }

    useEffect(() => {
      
      getOperations()
    
    }, [])
    

    useEffect(() => {
    
        const socket = getInfo()

        // const socket = io('http://127.0.0.1:8000')

    //     socket.on('message', (message) => {
    //         console.log(message, 'message')
    //         setMessages([...messages, message])
    //         setMsj(message)
    //     })
    
      return () => {
        socket.disconnect()
      }

    }, [ operations ])
    

  return (
    <>
        <Navbar />
        <div className='container mt-6 text-light'>
             <h1 className='my-4'>Log in real time</h1>
             {/* <p>
                Recibido: {msj}
             </p> */}

              {/* aling vertical the children of the next div */}
              <div className="alert alert-dark my-4 d-flex align-items-center" role="alert">
                  <i className="fas fa-terminal me-2 text-iq log-effect"></i>
                  <p className=''>
                    [STATUS] <span className='text-warning'>{msj}</span>
                  </p>
              </div>
                {/* Lista completa: {messages} */}
                <h2>Operations open</h2>

                {
                  operations.map((operation) => (
                    <div className="card bg-dark mb-4" key={operation.id}>
                      <div className="card-header my-1">
                        Operation #{operation.id}
                      </div>
                      <div className="card-body">
                        <h5 className="card-title">Market: {operation.market}</h5>
                        <p className="card-text my-2">Message: {operation.message}</p>
                        <p className="card-text my-2">Date: {operation.date}</p>
                        <p className="card-text my-2">Amount: {operation.ammount_use}</p>
                        <p className="card-text my-2">Profit: {operation.profit}</p>
                        <p className="btn btn-iq my-2">State: {operation.state}</p>
                        {/* <p href="#" className="btn btn-iq">Time remaining: {operation.duration_in_min}</p> */}
                      </div>
                    </div>
                  ))
                }

                {/* <div className="card bg-dark">
                <div className="card-header my-1">
                  Operation #bnjdsjabd
                </div>
                <div className="card-body">
                  <h5 className="card-title">EURUSD</h5>
                  <p className="card-text my-2">Call option placed</p>
                  <p className="card-text my-2">Date</p>
                  <p className="card-text my-2">Amount</p>
                  <p className="card-text my-2">State</p>
                  <p href="#" className="btn btn-iq">Time: 4:00</p>
                </div>
              </div> */}


                {/* <ul className='list-group'> */}

        </div>
    </>
  )

}
