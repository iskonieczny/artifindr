import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/style.scss';
import App from './App';
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  Link
} from "react-router-dom";
import Login from './auth/Login';
import Register from './auth/Register';
import Verify from './auth/Verify';
import { Provider } from 'react-redux'
import { store } from './ducks/store';
import Navbar from './ui/Navbar';

const wrapRoute = (route) => {
  return (<div className='wrapper'><Navbar/>{route}</div>)
}

const router = createBrowserRouter([
  {
    path: "/",
    element: wrapRoute(<App />),
  },
  {
    path: "/auth/login",
    element: wrapRoute(<Login />),
  },
  {
    path: "/auth/register",
    element: wrapRoute(<Register />),
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router}/>
    </Provider>
  </React.StrictMode>
);

