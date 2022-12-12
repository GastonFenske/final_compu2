import React from 'react'

export const LoadingButtonComponent = () => {
  return (
    <>

        <button className="btn btn-iq" type="button" disabled>
            <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Loading...
        </button>

    </>
  )
}
