import React from 'react'
import { Link, NavLink } from 'react-router-dom'

export const Navbar = () => {
  return (
    <>

    <nav className="navbar navbar-expand-lg navbar-dark bg-dark-nav fixed-top">
    <div className="container">

        {/* <a className="navbar-brand" href="#">Navbar</a> */}
        <Link
            className="navbar-brand"
            to="/"
        >
            <span className='text-iq'>Trading Bot IQ</span>
        </Link>

        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
        {/* <ul className="navbar-nav me-auto mb-2 mb-lg-0"> */}
        <ul className="navbar-nav mb-2 mb-lg-0 ms-auto">

            {/* <li className="nav-item">
            <a className="nav-link active" aria-current="page" href="#">Home</a>
            </li> */}
            <NavLink
                className={({isActive}) => `nav-item nav-link me-2 ${isActive ? 'active' : ''}}`}
                to="/markets"
            >
                Markets
            </NavLink>

            {/* <li className="nav-item">
            <a className="nav-link" href="#">Operaciones en proceso</a>
            </li>  */}

            <NavLink
                className={({isActive}) => `nav-item nav-link me-2 ${isActive ? 'active' : ''}}`}
                to="/operations"
            >
                Real Time
            </NavLink>

            <NavLink
                className={({isActive}) => `nav-item nav-link me-2 ${isActive ? 'active' : ''}}`}
                to="/operations-data"
            >
                Operations Log
            </NavLink>



            <NavLink
                className={({isActive}) => `nav-item nav-link btn btn-iq ${isActive ? 'active' : ''}}`}
                to="/iq"
            >
                {
                    // verify if the user is logged in
                    // if so, log out
                    // if not, log in
                    // localStorage.getItem(localStorage.getItem("authenticated"))
                    localStorage.getItem("authenticated") === 'true'
                    ?
                    'Log Out'
                    :
                    'Log In'
                }
            </NavLink>




            {/* <li className="nav-item">
            <a className="nav-link" href="#" tabIndex="-1" aria-disabled="true">IQ Log In</a>
            </li> */}

        </ul>
        </div>
    </div>
    </nav>

    </>
  )
}
