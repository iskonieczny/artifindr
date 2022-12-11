import * as types from "./types"

const loading = 'loading'
const error = 'error'

const defaultState = {
  flow: undefined,
  chats: {}
} 

export const reducer = (state = defaultState, action) => {
  switch (action.type) {
    case types.FLOW_SET:
      return {...state, flow: action.payload}
    case types.IMG_SET:
      return {...state, img: action.payload}
    case types.DEFAULT:
      return {...state, [action.key]: action.payload}
    case types.CHAT_ADD:
      return {...state, chats: {...state.chats, [action.payload.id]: {...action.payload}}}
    case types.MESSAGE_ADD:
      return {...state, chats: {
        ...state.chats, 
        [action.payload.chat]: {...state.chats[action.payload.chat], messages: [
          ...state.chats[action.payload.chat].messages, action.payload.message
        ]}}
      }
    default:
      return state;
  }
}

