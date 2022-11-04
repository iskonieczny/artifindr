import './App.css';
import {Link, Router} from "react-router-dom"
import { useEffect, useState } from 'react';
import { kratos } from './kratos/kratos';
import { useRouter } from './hooks/useRouter';
import { config } from './kratos/config';
import { useSelector, useDispatch } from 'react-redux'
import { setFlow } from "./ducks/actions"
import { useLogout } from './hooks/useLogout';

function App() {

  const router = useRouter()
  const logout = useLogout()
  const flow = useSelector((state) => state.flow)
  const dispatch = useDispatch()


  useEffect(() => {
    kratos
      .toSession()
      .then(({ data }) => {
        dispatch(setFlow(data))
      })
      .catch((err) => {
        switch (err.response?.status) {
          case 403:
          // This is a legacy error code thrown. See code 422 for
          // more details.
          case 422:
            // This status code is returned when we are trying to
            // validate a session which has not yet completed
            // it's second factor
            return router.navigate(config.routes.login.selfServiceUrl)
          case 401:
            // do nothing, the user is not logged in
            return
        }

        // Something else happened!
        return
      })
  }, [])

  const getName = () => {
    const traits=flow.identity.traits
    return traits.first_name + " " + traits.last_name
  }
  const isVerified = !flow 
  || !flow.authentication_methods
  || flow.authentication_methods[0].method === "oidc"
  || !flow.identity
  || flow.identity.verifiable_addresses[0].verified

  return (
    <div className='bg-light'>
      <div>
        {flow?.identity && `Hello, ${getName()}`}
      </div>
      {isVerified || <div>Please, verify your address</div>}
      <nav>
        <ul>
          <li>
            <Link to="/auth/login">login</Link>
            <Link to="/auth/register">register</Link>
            <Link to="/auth/verify">Verify</Link>
          </li>
        </ul>
      </nav>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default App;
