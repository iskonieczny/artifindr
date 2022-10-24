import './App.css';
import {Link, Router} from "react-router-dom"
import { useEffect, useState } from 'react';
import { kratos } from './kratos/kratos';
import { useRouter } from './hooks/useRouter';
import { config } from './kratos/config';

function App() {

  const router = useRouter()
  const [session, setSession] = useState()
  const [hasSession, setHasSession] = useState(false)

  useEffect(() => {
    kratos
      .toSession()
      .then(({ data }) => {
        setSession(data)
        setHasSession(true)
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
    const identity=session.identity.traits
    return identity.first_name + " " + identity.last_name
  }

  return (
    <div>
      <div>
        {session?.identity && `Witaj, ${getName()}`}
      </div>
      <nav>
        <ul>
          <li>
            <Link to="/auth/login">login</Link>xd
            <Link to="/auth/registration">register</Link>xd
            <Link to="/auth/login">Home</Link>xd
          </li>
        </ul>
      </nav>
      xddxd
      {/* A <Switch> looks through its children <Route>s and
          renders the first one that matches the current URL. */}
      
    </div>
  );
}

export default App;
