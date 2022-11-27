import { Link } from "react-router-dom"
import { useRouter } from "../hooks/useRouter"

const Navbar = () => {

  const router = useRouter()

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

  return (
    <>
      <div className="px-2 navbar sticky-top">
        <div>
          {getBackLink()}
          {getLink('/', 'artiFindr')}
        </div>
        <div>
          ...
        </div>
      </div>
      <div className="curve"/>
    </>
  )
}

export default Navbar