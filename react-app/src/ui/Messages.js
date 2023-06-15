import { Link } from "react-router-dom"
import { useRouter } from "../hooks/useRouter"
import { useSelector, useDispatch } from 'react-redux'
import { useLogout } from '../hooks/useLogout';
import { useFormik } from 'formik';
import { useEffect, useState, useRef } from "react";
import Navbar from "./Navbar";
import { addMessage, setSingleValue, addChat } from "../ducks/actions";
import axios from "axios";
import ScrollableFeed from 'react-scrollable-feed'
import useWindowWidth from "../hooks/useWindowWidth";


const Messages = () => {

  const dispatch = useDispatch()
  const width = useWindowWidth();
  const router = useRouter()
  const user_id = useSelector((state) => state.flow.identity.id)
  const chats = useSelector((state) => state.chats)
  const activeChat = useSelector((state) => state.activeChat)
  const last_tag_used = useSelector((state) => state.last_tag_used)
  const formik = useFormik({
    initialValues: {
      message: '',
    },
    onSubmit: (values, { resetForm }) => {
      resetForm()
      dispatch(addMessage(activeChat, {message: values.message, fromUser: true}))
      values.message && axios.get(process.env.REACT_APP_CHAT_API_ADDR+"/get_new_msg", {
        params: {
          "user_id": user_id,
          "bot_id": activeChat,
          "message": values.message,
          "last_tag_used": "None" //last_tag_used || "None"
        }
      }).then(res => {
        dispatch(addMessage(activeChat, {message: res.data.response}))
        dispatch(setSingleValue("last_tag_used", res.data.tag_used))
      }).catch(err => console.log(err))

    },
  });

  useEffect(() => {
    if (Object.keys(chats).length === 0) {
      axios.get(process.env.REACT_APP_CHAT_API_ADDR+"/get_all_user_bots", {
        params: {
          "user_id": user_id
        }
      }).then(res => {
        res.data.forEach(bot => dispatch(addChat({
          id: bot.bot_id,
          img_path: bot.img_path,
          name: bot.name,
          messages: [{message: `This is the start of your conversation with ${bot.name}.`}]
        })))
        res.data.length > 0 && handleChatChange(res.data[0].bot_id, true)
      }).catch(err => console.log(err))
    }
    
  }, [])

  const handleChatChange = (id, isInit=false) => {
    (!Object.keys(chats).includes(JSON.stringify(id)) || chats[id].messages.length < 2)
    && axios.get(process.env.REACT_APP_CHAT_API_ADDR+"/get_all_user_msg", {
      params: {
        "user_id": user_id,
        "bot_id": id
      }
    }).then(res => {
      res.data.forEach(msg => 
      dispatch(addMessage(id, {
        message: msg.content, 
        fromUser: !msg.from_bot
      })))
    }).catch(err => console.log(err))
    dispatch(setSingleValue("activeChat", id))
    dispatch(setSingleValue("last_tag_used", null))
    
    !isInit && router.navigate(`/messages/${id}`)
  }

  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView()
  }

  useEffect(() => {
    scrollToBottom()
  }, [chats, router.query.id]);

  const listStyle = width < 561 && router.query.id ? {
    display: "none", visibility: "hidden", position: "absolute"
  } : {}

  return (Object.keys(chats).length === 0 || !activeChat) ? (<>No chats yet!</>) : (
    <div className="d-flex messages ">
      <div style={listStyle} className="chat-list">
        {Object.values(chats).map((el, idx) => 
          <div key={el.id} className={"d-flex p-2 rounded-5 chat-list-elem " + (activeChat===el.id ? "bg-secondary" : "")} onClick={() => handleChatChange(el.id)}>
            <img src={process.env.REACT_APP_GAN_API_ADDR+"/face?bot_id="+el.id} width="50" height="50" className="rounded-circle m-1" />
            <div className="d-flex flex-wrap py-1">
              <span style={{fontWeight: "550", width: "100%"}}>{el.name}</span>
              <span>{el.messages[el.messages.length-1].message}</span>
            </div>
          </div>
        )}
      </div>
      <div className={"d-flex flex-column flex-wrap w-100 me-3"+ (!listStyle.display ? " chat-window" : "")}>
        <div className="w-100 d-flex justify-content-end border-bottom ms-auto pe-3">
          <h4 className="align-self-center">{chats[activeChat].name}</h4>
          <img src={process.env.REACT_APP_GAN_API_ADDR+"/face?bot_id="+activeChat} width="50" height="50" className="rounded-circle m-1" />
        </div>
        <div className="flex-grow-1 message-box ms-2 my-2">
          
          {chats[activeChat].messages.map(el => 
            <div className="d-flex m-2">
              {el.fromUser && <div className="flex-grow-1" />}
              {el.fromUser || <img src={process.env.REACT_APP_GAN_API_ADDR+"/face?bot_id="+activeChat} width="40" height="40" className="rounded-circle m-1" />}
              <div className={"p-2 ms-auto rounded-4 mx-1"+ (el.fromUser ? " bg-secondary text-end" : " bg-semi-light-chat")}>
                {el.message}
              </div>
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