import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/style.scss';
import 'bootstrap'
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
import Messages from './ui/Messages';

const wrapRoute = (route) => {
  return (<div className='wrapper'><Navbar/>{route}</div>)
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/auth/login",
    element: wrapRoute(<Login />),
  },
  {
    path: "/auth/register",
    element: wrapRoute(<Register />),
  },
  {
    path: "/messages",
    element: wrapRoute(<Messages />),
  },
  {
    path: "/messages/:id",
    element: wrapRoute(<Messages />),
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <Provider store={store}>
      <RouterProvider router={router}/>
    </Provider>
);

