import { applyMiddleware, createStore } from 'redux';
import { reducer } from './reducer';
 
// Logger with default options
import logger from 'redux-logger'
export const store = createStore(
  reducer,
  applyMiddleware(logger)
)
 
// Note passing middleware as the third argument requires redux@>=3.1.0