import React, { useEffect, useState } from 'react'
import { Navbar } from '../components/navbar'
// import { getNewInfo } from '../helpers/getNewInfo'
import io from 'socket.io-client'
import tradingBotApi from '../api/tradingBotApi'


export const OperationsRealPage = () => {


    const [msj, setMsj] = useState({
        type: '',
        message: '',
        date: '',
        close: '',
        upper_band: '',
        lower_band: '',
        K: '',
        D: '',
        CCI: '',
        ema_growing: '',
    })
    const [messages, setMessages] = useState([])

    const [operations, setOperations] = useState([])
    const [ids, setIds] = useState([])

    const getOperations = async () => {
      // const url = 'http://127.0.0.1:1234/api/operations-pending'
      const url = `${tradingBotApi}/api/operations-pending`
      const resp = await fetch(url)
      const data = await resp.json();
      setOperations(data.operations);
      console.log(operations, 'operations')
    }

    const getInfo = () => {

        const socket = io('http://127.0.0.1:8000')

        socket.on('server:newVeil', (message) => {

          setNewInfo(message)

        })

        return socket

    }

    const setNewInfo = (data) => {

      if (data.type === 'new_veil') {

        // const message = `Fecha: ${data.date} | Mensaje: ${data.message}`

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


      }


    useEffect(() => {
      
      getOperations()
    
    }, [])
    

    useEffect(() => {
    
        const socket = getInfo()

    
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
                    [MESSAGE] <span className='text-warning'>{msj.message}</span><br/>
                    [DATE] <span className='text-warning'>{msj.date}</span><br/>
                    [CLOSE] <span className='text-warning'>{msj.close}</span><br/>
                    [UPPER_BAND] <span className='text-warning'>{msj.upper_band}</span><br/>
                    [LOWER_BAND] <span className='text-warning'>{msj.lower_band}</span><br/>
                    [K] <span className='text-warning'>{msj.K}</span><br/>
                    [D] <span className='text-warning'>{msj.D}</span><br/>
                    [CCI] <span className='text-warning'>{msj.CCI}</span><br/>
                    [EMA_GROWING] <span className='text-warning'>{msj.ema_growing}</span><br/>
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

                {/* <ul className='list-group'> */}

        </div>
    </>
  )

}
