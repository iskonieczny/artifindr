import { Link } from "react-router-dom"
import { useRouter } from "../hooks/useRouter"
import { useSelector, useDispatch } from 'react-redux'
import { useLogout } from '../hooks/useLogout';
import { useState } from "react";


const Navbar = () => {

  const router = useRouter()
  const flow = useSelector((state) => state.flow)
  const [dropdown, setDropdown] = useState(false)
  const logout = useLogout()

  const getLink = (path, text) => {
    return router.location.pathname === path ? 
    (<Link to={path} className="active">{text}</Link>) :
    (<Link to={path}>{text}</Link>)
  }

  const getBackLink = () => {
    return router.location.pathname.includes('/', 2) ? 
    (<span className="back-link" onClick={() => router.navigate(-1)}>&larr;</span>) :
    (<></>)
  }

  const getOptions = () => (
    <div class="btn-group">
      <button type="button" className="btn btn-sm dropdown-toggle text-white caret-off" data-bs-toggle="dropdown">
        &#8226;&#8226;&#8226;
      </button>
        <ul className="dropdown-menu dropdown-menu-end bg-primary">
          <li><button className="dropdown-item text-white" >Your account</button></li>
          <li><button className="dropdown-item text-white" >Premium content</button></li>
          <li><hr className="dropdown-divider border border-secondary" /></li>
          <li><button className="dropdown-item text-danger" onClick={logout}>Log out</button></li>
        </ul>
    </div>
  )

  return (
    <>
      <div className="px-2 navbar sticky-top">
        <div className="navbar-left">
          {getBackLink()}
          {getLink('/', 'artiFindr')}
        </div>
        <div>
          {flow?.identity && getOptions()}
        </div>
      </div>
      <div className="curve"/>
    </>
  )
}

export default Navbar