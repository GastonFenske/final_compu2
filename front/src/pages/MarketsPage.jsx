import React from 'react'
import { MarketsComponent } from '../components/markets'
import { Navbar } from '../components/navbar'

export const MarketsPage = () => {
  return (
    <>

        <Navbar />
        <div className='container'>

        {
          <MarketsComponent />
        } 
        
        </div>

    </>
  )
}
