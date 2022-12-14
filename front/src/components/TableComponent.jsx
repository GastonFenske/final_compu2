import React, { useEffect, useState } from 'react'

export const TableComponent = (operations) => {

    const [wins, setWins] = useState(0)
    const [losses, setLosses] = useState(0)
    const [totalAmount, setTotalAmount] = useState(0)
    const [totalProfit, setTotalProfit] = useState(0)

    const [probability, setProbability] = useState(0)

    const calcProbability = () => {
        // why it doesnt work?
        if (wins === 0 && losses === 0) {
            setProbability(0)
            return;
        }
        setProbability(wins / (wins + losses) * 100)



        // console.log(wins, 'wins')
        // setProbability(wins / (wins + losses))
    }


    const setTotals =  (operations) => {

        // console.log operations len
        // console.log(operations.length, 'operations.length')

        operations.map( operation => {
            // console.log(operation.result, 'operation.result')
            if(operation.result === 1){
                // setWins(wins + 1)

                // why it doest work?
                setWins(prevState => prevState + 1)
                // console.log(wins, 'wins')
            }else{
                setLosses(prevState => prevState + 1)
                // console.log(losses, 'losses')
            }

            setTotalAmount(prevState => prevState + operation.ammount_use)
            setTotalProfit(prevState => prevState + operation.profit)

        })

        // calcProbability();
    }


    useEffect(() => {
      
        // console.log(operations, 'operations.operations')
        setTotals(operations.operations);



    //   return () => {
    //     // second
    //   }
    }, [])

    useEffect(() => {
        calcProbability();

    }, [wins, losses])

    

  return (
    <>

        <h4 className='text-light'>
            Efectividad del bot: {probability}%
        </h4>
        <h4 className='text-light'>
            Ganacias actuales: {totalProfit} U$D
        </h4>

        <table className="table table-light table-striped my-4">
                <thead className='table-dark'>
                    <tr>
                    <th scope="col">Operation id</th>
                    <th scope="col">Date</th>
                    <th scope="col">Market</th>
                    <th scope="col">Result</th>
                    <th scope="col">Amount use</th>
                    <th scope="col">Profit</th>
                    <th scope='col'>Type</th>
                    <th scope="col">Duration in minutes</th>
                    </tr>

                </thead>
            
                <tbody>

                        <tr>
                            <th scope="row">Total</th>
                            <td></td>
                            <td></td>
                            <td> {wins} wins</td>
                            <td>{totalAmount} U$D</td>
                            <td>{totalProfit} U$D</td>
                            <td></td>
                            <td></td>
                        </tr>

                    {
                        operations.operations.map( operation => (


                            <tr key={operation.id}>
                                <th scope="row">{operation.id}</th>
                                <td>{operation.date}</td>
                                <td>{operation.market}</td>
                                <td>{
                                    operation.result === 1
                                    ?
                                    <span className='text-success'>Win</span>
                                    :
                                    <span className='text-danger'>Lost</span>
                                }
                                </td>
                                <td>{operation.ammount_use} U$D</td>
                                <td>{operation.profit} U$D</td>
                                <td>{operation.type}</td>
                                <td>{operation.duration_in_min} minutes</td>
                            </tr>

                            // create a tr for sum the values
            
                        ))
                    }

                    {/* <tr>
                    <th scope="row">1</th>
                    <td>2022-12-08 22:29:02.097866</td>
                    <td>EURUSD</td>
                    <td>Win</td>
                    <td>$10.0</td>
                    <td>$8.0</td>
                    <td>60 minutes</td>
                    </tr> */}


                </tbody>
                
            </table>
    </>
  )
}
