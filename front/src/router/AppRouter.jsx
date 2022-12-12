import React from 'react'
import { Route, Routes } from 'react-router-dom'
import { IqPage } from '../pages/IqPage'
import { MarketsPage } from '../pages/MarketsPage'
import { OperationsPage } from '../pages/OperationsPage'
import { OperationsRealPage } from '../pages/OperationsRealPage'

export const AppRouter = () => {
  return (
    <>
        <Routes>
            <Route path='*' element={ <IqPage /> } />
            <Route path='/operations' element={ <OperationsRealPage /> } />
            <Route path='/iq' element={ <IqPage />} />
            <Route path='/markets' element={ <MarketsPage /> } />
            <Route path='/operations-data' element={ <OperationsPage /> } />
        </Routes>
    </>
  )
}
