import React from 'react'
import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { setFlow, setImg, setSingleValue } from "../ducks/actions"
import axios from "axios";

function Swiper({id, xd}) {
  const flow = useSelector((state) => state.flow)
  const swiperPersonData = useSelector((state) => state.swiperPersonData)
  const [style, setStyle] = useState({})

  const dispatch = useDispatch()

  const setNextPerson = () => {
    axios.get("https://random-data-api.com/api/v2/users?size=2&response_type=json")
    .then((res) => dispatch(setSingleValue("swiperPersonData", res.data[0])))
  }

  const handleRejectClick = () => {
    setStyle({animation: "0.5s swipe-left"})
    setTimeout(() => {
      setStyle({})
      setNextPerson()
      dispatch(setSingleValue("swipers", [<Swiper key={Math.random()} id={Math.random()} style={style} />]))
    }, 500)
    
  }

  const handleAcceptClick = () => {
    setStyle({animation: "0.5s swipe-right"})
    setTimeout(() => {
      setStyle({})
      setNextPerson()
      dispatch(setSingleValue("swipers", [<Swiper key={Math.random()} id={Math.random()} style={style} />]))
    }, 500)
  }

  return (!flow || !swiperPersonData) ? (<>loading...</>) : (
    <div className="m-1 p-3 rounded-5 d-flex flex-wrap bg-secondary swiper" style={style}>
      <img src={process.env.REACT_APP_GAN_API_ADDR+"/genapi?key="+id} />
      <h2>
        {swiperPersonData.first_name+" "+swiperPersonData.last_name+", "}
        {2022-swiperPersonData.date_of_birth.substring(0,4)}
      </h2>
      <h5>&#9893; {swiperPersonData.gender}</h5>
      <h5>{swiperPersonData.employment.title}</h5>
      <h6>I love {swiperPersonData.employment.key_skill.toLowerCase()}.</h6>
      <div className="d-flex flex-wrap justify-content-between">
        <img className="w-25" src="cross.svg" onClick={() => handleRejectClick()} />
        <img className="w-25" src="heart.svg" onClick={() => handleAcceptClick()} />
      </div>
      
    </div>
  );
}

export default Swiper;
