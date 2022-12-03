import React from 'react'
import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { setFlow, setImg, setSingleValue, addChat } from "../ducks/actions"
import axios from "axios";

function Swiper({queue, id}) {
  const flow = useSelector((state) => state.flow)
  const swiperPersonData = useSelector((state) => state.swiperPersonData)
  const swipers = useSelector((state) => state.swipers)
  const swiperStyles = useSelector((state) => state.swiperStyles)

  const dispatch = useDispatch()


  const setNextPerson = (accepted) => {
    axios.get("https://random-data-api.com/api/v2/users?size=2&response_type=json")
    .then((res) => {
      if (accepted) {
        const name = swiperPersonData.first_name+" "+swiperPersonData.last_name
        dispatch(addChat({
          name: name,
          id: Math.random(),
          messages: [{message: `This is the start of your conversation with ${name}.`}]
        }))
        dispatch(setSingleValue("swiperStyles", [
          {animation: "0.5s swipe-right", position: "absolute"}, 
          {animation: "0.5s rev-swipe-left", position: "absolute"}
        ]))
      } else {
        dispatch(setSingleValue("swiperStyles", [
          {animation: "0.5s swipe-left", position: "absolute"}, 
          {animation: "0.5s rev-swipe-right", position: "absolute"}
        ]))
      }
      dispatch(setSingleValue("swiperPersonData", res.data[0]))
      setTimeout(() => {
        dispatch(setSingleValue("swiperStyles", [
          {}, 
          {position: "absolute", visibility:"hidden"}
        ]))
        dispatch(setSingleValue("swipers", [{...swipers[1], props: {...swipers[1].props, queue: 0}}, <Swiper key={Math.random()} id={Math.random()} queue={1} />]))
      }, 500)
      
    })
  }

  const handleSwipe = (accepted) => {
    setNextPerson(accepted)
  }

  return (!flow || !swiperPersonData) ? (<>loading...</>) : (
    <div className="m-1 p-3 rounded-5 d-flex flex-wrap bg-secondary swiper" style={swiperStyles[queue]}>
      <img src={process.env.REACT_APP_GAN_API_ADDR+"/genapi?key="+id} />
      <h2>
        {swiperPersonData.first_name+" "+swiperPersonData.last_name+", "}
        {2022-swiperPersonData.date_of_birth.substring(0,4)}
      </h2>
      <h5>&#9893; {swiperPersonData.gender}</h5>
      <div className='break' />
      <h5>{swiperPersonData.employment.title}</h5>
      <div className='break' />
      <h6>I love {swiperPersonData.employment.key_skill.toLowerCase()}.</h6>
      <div className="d-flex flex-wrap justify-content-between">
        <img className="w-25" src="cross.svg" onClick={() => handleSwipe(false)} />
        <img className="w-25" src="heart.svg" onClick={() => handleSwipe(true)} />
      </div>
      
    </div>
  );
}

export default Swiper;
