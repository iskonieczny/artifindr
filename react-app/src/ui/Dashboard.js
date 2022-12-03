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
  const flow = useSelector((state) => state.flow)

  const dispatch = useDispatch()
  const swipers = useSelector((state) => state.swipers)
  const swiperPersonData = useSelector((state) => state.swiperPersonData)

  const getName = () => {
    const traits=flow.identity.traits
    return traits.first_name + " " + traits.last_name
  }

  useEffect(() => {
    dispatch(setSingleValue("swiperStyles", [{}, {position: "absolute", visibility:"hidden"}]))
    swiperPersonData
    || axios.get("https://random-data-api.com/api/v2/users?size=2&response_type=json")
    .then((res) => dispatch(setSingleValue("swiperPersonData", res.data[0])))
    //fixing same images problem when adding at once
    const swiper = <Swiper key={Math.random()} id={Math.random()} queue={0} />
    dispatch(setSingleValue("swipers", [swiper]))
    setTimeout(() => {
      dispatch(setSingleValue("swipers", [swiper, <Swiper key={Math.random()} id={Math.random()} queue={1} />]))
    }, 200)
  }, [])

  const isVerified = !flow 
  || !flow.authentication_methods
  || flow.authentication_methods[0].method === "oidc"
  || !flow.identity
  || flow.identity.verifiable_addresses[0].verified

  return (!flow || !swipers) ? (<>loading...</>) : (
    <div className='wrapper'>
      <Navbar/>
      <div className="d-flex justify-content-center flex-wrap">
        <div className="break" />
        {swipers.slice(0,2)}
      </div>
    </div>
  );
}

export default Dashboard;

/*

        <div className="m-1 p-3 rounded-5 text-center bg-secondary">
          {flow?.identity && `Hello, ${getName()}`}
          <div>
            {isVerified ? "Your account is set up and ready for love." : "Please, verify your address"}
          </div>
        </div>
*/