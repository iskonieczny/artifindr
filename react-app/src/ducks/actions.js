import * as types from "./types"

export const setFlow = (payload) => ({
  type: types.FLOW_SET,
  payload: payload
})

export const setImg = (payload) => ({
  type: types.IMG_SET,
  payload: payload
})

export const addChat = (payload) => ({
  type: types.CHAT_ADD,
  payload: payload
})

export const addMessage = (chat, message) => ({
  type: types.MESSAGE_ADD,
  payload: {chat, message}
})

export const setSingleValue = (key, payload) => ({
  type: types.DEFAULT,
  key: key,
  payload: payload
})