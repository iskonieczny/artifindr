import React from 'react'
import {Link, Router} from "react-router-dom"
import { useEffect, useState } from 'react';
import { kratos } from '../kratos/kratos';
import { useRouter } from '../hooks/useRouter';
import { config } from '../kratos/config';
import { useSelector, useDispatch } from 'react-redux'
import { setFlow, setImg, setSingleValue } from "../ducks/actions"
import { useLogout } from '../hooks/useLogout';
import Navbar from './Navbar';
import axios from "axios";
import Swiper from './Swiper';

function Dashboard() {

  const router = useRouter()
  const logout = useLogout()
  const flow = useSelector((state) => state.flow)
  const img = useSelector((state) => state.img)
  const [style, setStyle] = useState({})
  
  const swiperPersonData = useSelector((state) => state.swiperPersonData)

  const dispatch = useDispatch()
  const swipers = useSelector((state) => state.swipers)


  

  const getName = () => {
    const traits=flow.identity.traits
    return traits.first_name + " " + traits.last_name
  }

  

  

  useEffect(() => {
    axios.get("https://random-data-api.com/api/v2/users?size=2&response_type=json")
    .then((res) => dispatch(setSingleValue("swiperPersonData", res.data[0])))
    dispatch(setSingleValue("swipers", [<Swiper key={Math.random()} id={Math.random()} style={style} />]))
  }, [])

  const isVerified = !flow 
  || !flow.authentication_methods
  || flow.authentication_methods[0].method === "oidc"
  || !flow.identity
  || flow.identity.verifiable_addresses[0].verified

  return (!flow) ? (<>loading...</>) : (
    <div className='wrapper'>
      <Navbar/>
      <div className="d-flex justify-content-center flex-wrap">
        <div className="m-1 p-3 rounded-5 text-center bg-secondary">
          {flow?.identity && `Hello, ${getName()}`}
          <div>
            {isVerified ? "Your account is set up and ready for love." : "Please, verify your address"}
          </div>
        </div>
        <div className="break" />
        {swipers}
      </div>
    </div>
  );
}

export default Dashboard;
