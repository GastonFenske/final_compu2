import React, { useEffect, useState } from 'react'
import axios from 'axios';
import { getMarkets } from '../helpers/getMarkets';
import { operateMarket } from '../helpers/operateMarket';
import { LoadingComponent } from './LoadingComponent';

export const MarketsComponent = () => {

  const [markets, setMarkets] = useState([])
  const [activeMarket, setActiveMarket] = useState('')
  const [money, setMoney] = useState(0)

  const getOpenMarkets = async () => {
    const openMarkets = await getMarkets()
    const markets = orderOpenMarkets(openMarkets)
    setMarkets(markets)
  }

  const orderOpenMarkets = (markets) => {
    // console.log(markets, 'markets')
    markets.sort((a, b) => {
      if (a.name > b.name) {
        return 1;
      }
      if (a.name < b.name) {
        return -1;
      }
      // a must be equal to b
      return 0;
    })
    // console.log(markets, 'markets')
    return markets
  }

  const startTrading = (market_name, money) => {
    operateMarket(market_name, money)

    if (activeMarket === market_name) {
      // console.log('Se desactiva el mercado')
      setActiveMarket('')
    }
    else {
      setActiveMarket(market_name)
    }

  }


  useEffect(() => {

    getOpenMarkets()
  
    // return () => {
    //   second
    // }
  }, [ activeMarket ])


  return (
    <>

      {/* if open_markets is empty return LoadingComponent */}

      {
        markets.length === 0 && <LoadingComponent />
      }

      {/* create an input to set the moeny */}
      <div className='input-group mt-6'>
        <span className='input-group-text' id='basic-addon1'>$</span>
        <input
          type='number'
          className='form-control'
          placeholder='Cantidad de dinero'
          aria-label='Username'
          aria-describedby='basic-addon1'
          onChange={ (e) => setMoney(e.target.value) }
        />
      </div>

      <h3 className='my-4 mt-3 text-light'>
        Mercados abiertos
      </h3>

      <ol className='list-group mb-4 bg-dark'>
        {
          markets.map(market => (
            <li key={market.id} className='list-group-item d-flex justify-content-between align-items-center text-light bg-pro'>
  
              {market.name}
              {/* create a button to operate this market */}
              {
                (market.operating == true)
                ?
                <button
                  className='btn btn-success'
                  onClick={ () => startTrading(market.name, money) }
                >
                  Stop Trade
                </button>
                :
                <button 

                    className="btn btn-iq text-light"
                    onClick={ () => startTrading(market.name, money) }
                  >
                    Operar
                </button>
              }


            </li>
          ))
        }
      </ol>

    </>
  )
}
