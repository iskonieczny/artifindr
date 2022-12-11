import { Link } from "react-router-dom"
import { useRouter } from "../hooks/useRouter"
import { useSelector, useDispatch } from 'react-redux'
import { useLogout } from '../hooks/useLogout';
import { useFormik } from 'formik';
import { useEffect, useState, useRef } from "react";
import Navbar from "./Navbar";
import { addMessage, setSingleValue } from "../ducks/actions";
import axios from "axios";
import ScrollableFeed from 'react-scrollable-feed'


const Messages = () => {

  const dispatch = useDispatch()
  //const user = useSelector((state) => state.flow.identity.id)
  const chats = useSelector((state) => state.chats)
  const activeChat = useSelector((state) => state.activeChat)
  const formik = useFormik({
    initialValues: {
      message: '',
    },
    onSubmit: (values, { resetForm }) => {
      resetForm()
      values.message && axios.post(process.env.REACT_APP_CHAT_API_ADDR+"/chatapi", {
        "message": values.message,
        "chatbot_character": "not_formal",
        "last_tag_used": "None"
      }).then(res => {
        dispatch(addMessage(activeChat, {message: values.message, fromUser: true}))
        dispatch(addMessage(activeChat, {message: res.data.response}))
      }).catch(err => console.log(err))

    },
  });

  useEffect(() => {
    if (!activeChat) {
      dispatch(setSingleValue("activeChat", Object.values(chats)[0].id))
    }
  }, [])

  const handleChatChange = (id) => {
    dispatch(setSingleValue("activeChat", id))
  }

  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView()
  }

  useEffect(() => {
    scrollToBottom()
  }, [chats]);


  return (!chats || !activeChat) ? (<>No chats yet!</>) : (
    <div className="d-flex messages ">
      <div className="chat-list">
        {Object.values(chats).map((el, idx) => 
          <div key={el.id} className="d-flex p-2 rounded-5 chat-list-elem" onClick={() => handleChatChange(el.id)}>
            <img src="/gracjan.jpg" width="50" height="50" className="rounded-circle m-1" />
            <div className="d-flex flex-wrap py-1">
              <span style={{fontWeight: "550"}}>{el.name}</span>
              <span>{el.messages[el.messages.length-1].message}</span>
            </div>
          </div>
        )}
      </div>
      <div className="d-flex flex-column flex-wrap w-100 me-3">
        <div className="w-100 d-flex justify-content-end border-bottom ms-auto pe-3">
          <h4 className="align-self-center">{chats[activeChat].name}</h4>
          <img src="/gracjan.jpg" width="50" height="50" className="rounded-circle m-1" />
        </div>
        <div className="flex-grow-1 message-box ms-2 my-2">
          
          {chats[activeChat].messages.map(el => 
            <div className="d-flex">
              {el.fromUser && <div className="flex-grow-1" />}
              {el.fromUser || <img src="/gracjan.jpg" width="40" height="40" className="rounded-circle m-1" />}
              <div className="p-2 ms-auto text-end rounded-5 bg-semi-light mx-2">{el.message}</div>
              {el.fromUser || <div className="flex-grow-1" />}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <form autocomplete="off" className="d-flex w-100 m-1 mt-auto pe-3" onSubmit={formik.handleSubmit}>
          <input
            type="text"
            name="message"
            value={formik.values.message}
            className="flex-grow-1 mx-2 form-control rounded-2"
            onChange={formik.handleChange}
            placeholder="Type message..."
          />
          <button type="submit" className="btn btn-primary">
            Send
          </button>
        </form>
      </div>
    </div>
  )
}

export default Messages