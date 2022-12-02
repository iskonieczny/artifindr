import * as types from "./types"

export const setFlow = (payload) => ({
  type: types.FLOW_SET,
  payload: payload
})

export const setImg = (payload) => ({
  type: types.IMG_SET,
  payload: payload
})

export const setSingleValue = (key, payload) => ({
  type: types.DEFAULT,
  key: key,
  payload: payload
})