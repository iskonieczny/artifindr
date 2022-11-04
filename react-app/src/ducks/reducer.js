import * as types from "./types"

const loading = 'loading'
const error = 'error'

const defaultState = {
  flow: undefined
} 

export const reducer = (state = defaultState, action) => {
  switch (action.type) {
    case types.FLOW_SET:
      return {...state, flow: action.payload}
    default:
      return state;
  }
}

