import { useSelector, useDispatch } from 'react-redux'
import { useLogout } from '../hooks/useLogout';
import Navbar from './Navbar';
import {Link} from "react-router-dom"

function Mainpage() {

  const logout = useLogout()
  const flow = useSelector((state) => state.flow)

  return (
    <div className='main'>
      <Navbar/>
        <div className='py-3 px-2 middle rounded-5'>
          <div className='h2 py-3 w-100 text-white'>Artifindr: your best bet for artificial love.</div>
          <Link to="/auth/login" className='p-2 btn btn-primary rounded-5 btn-lg'>Log in</Link>
          <span className='p-2'/>
          <Link to="/auth/register" className='p-2 btn btn-primary rounded-5 btn-lg'>Register</Link>
        </div>
      {flow?.identity && <button onClick={logout}>Logout</button>}
    </div>
  )
}

export default Mainpage