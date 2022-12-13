import React, { useEffect, useState } from 'react'
import { LoadingComponent } from '../components/LoadingComponent'
import { Navbar } from '../components/navbar'
import { TableComponent } from '../components/TableComponent'

export const OperationsPage = () => {

    const [operations, setOperations] = useState([])

    const [loading, setLoading] = useState(false)

    const getOperations = async () => {
        setLoading(true);
        const url = 'http://127.0.0.1:1234/api/operations'
        const resp = await fetch(url)
        const data = await resp.json();
        setOperations(data.operations);
        setLoading(false);
        console.log(operations, 'operations')
    }

    useEffect(() => {
      
        getOperations();
    
    //   return () => {
    //     second
    //   }
    }, [])
    

  return (
    <>
        <Navbar />
        <div className='container'>

            <h1 className='text-light mt-6'>Operations</h1>

            {
                loading
                ?
                 <LoadingComponent />
                :
                <TableComponent operations={operations}/>
            }
            {/* <TableComponent operations={operations}/> */}

        </div>
    </>
  )
}
