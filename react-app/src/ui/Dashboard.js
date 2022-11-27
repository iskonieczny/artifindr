import {Link, Router} from "react-router-dom"
import { useEffect, useState } from 'react';
import { kratos } from '../kratos/kratos';
import { useRouter } from '../hooks/useRouter';
import { config } from '../kratos/config';
import { useSelector, useDispatch } from 'react-redux'
import { setFlow, setImg } from "../ducks/actions"
import { useLogout } from '../hooks/useLogout';
import Navbar from './Navbar';
import axios from "axios";

function Dashboard() {

  const router = useRouter()
  const logout = useLogout()
  const flow = useSelector((state) => state.flow)
  const img = useSelector((state) => state.img)
  const dispatch = useDispatch()


  useEffect(() => {
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

  console.log(process.env.REACT_APP_GAN_API_ADDR)

  return !flow ? (<>loading...</>) : (
    <>
      <div className="d-flex justify-content-center">
        {flow?.identity && `Hello, ${getName()}`}
      </div>
      {isVerified || <div>Please, verify your address</div>}
      {flow?.identity && <button onClick={logout}>Logout</button>}
      <img src={process.env.REACT_APP_GAN_API_ADDR+"/genapi"} max/>
    </>
  );
}

export default Dashboard;
