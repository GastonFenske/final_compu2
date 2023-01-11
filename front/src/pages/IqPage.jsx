import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import tradingBotApi from '../api/tradingBotApi';
import { LoadingButtonComponent } from '../components/LoadingButtonComponent';
import { LoadingComponent } from '../components/LoadingComponent';
import { Navbar } from '../components/navbar'

export const IqPage = () => {

    localStorage.setItem("authenticated", false);

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const [loading, setLoading] = useState(false)

    const [success, setSuccess] = useState('loading')

    const [authenticated, setauthenticated] = useState(
        localStorage.getItem(localStorage.getItem("authenticated") || false)
    );

    const navigate = useNavigate();

    const onEmailChange = ({ target }) => {
        setEmail( target.value );
    }

    const onPasswordChange = ({ target }) => {
        setPassword( target.value );
    }

    const onSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);
        
        // const url = 'http://127.0.0.1:1234/api/login'
        const url = `${tradingBotApi}/api/login`
        const resp = await fetch(
            url,
            {
                method: 'POST',
                body: JSON.stringify({
                    email,
                    password
                }),
            }
        )
        const data = await resp.json();

        if ( data.status === 'ok' ) {
            // go to MarketsPage
            setauthenticated(true);
            localStorage.setItem("authenticated", true);
            navigate('/markets');

        }
        else {  

            console.log('error login')
            setSuccess('error');
            setLoading(false);

        }

    }

    useEffect(() => {
      
        localStorage.setItem("authenticated", false);
    
    //   return () => {
    //     second
    //   }
    }, [
        // every time I change the value of authenticated, this useEffect will be executed
        authenticated
    ])
    

  return (
    <>

        <Navbar />

        <div className="container">

        <div className="row d-flex justify-content-center my-6">
            <div className="bg-forms p-5 rounded col-md-4 col-10">
                <div className="d-flex justify-content-center">
                    <h3>Log In IQ Option</h3>
                </div>

                {
                    // show alert when the user submit wrong credentials
                    success === 'error'
                    &&
                    <div className="alert alert-dark my-2" role="alert">
                        <strong>Oh no!</strong> Email or password incorrect.
                    </div>
                }

                <form className="pt-3"
                onSubmit={ onSubmit }
                >
                    <div className="mb-3">
                    <label htmlFor="exampleInputEmail1" className="form-label">Email</label>
                    <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Ingresa tu email" 
                    value={ email }
                    onChange={ onEmailChange }
                    />
                    </div>
                    <div className="mb-3">
                    <label htmlFor="exampleInputPassword1" className="form-label">Password</label>
                    <input type="password" className="form-control" id="exampleInputPassword1" placeholder="Ingresa tu password" 
                    value={ password }
                    onChange={ onPasswordChange }
                    />
                    </div>
                    <div className="d-grid pt-3">


                        {
                            // when the user submit show loading button component
                            loading 
                            ?
                             <LoadingButtonComponent />
                            :
                            <button type="submit" className="btn btn-iq"
                                onClick={ onSubmit }
                            >
                                Log In
                            </button>

                        }


                    </div>
                </form>
            </div>
        </div>

        </div>

        {/* <LoadingComponent /> */}

    </>
  )
}
