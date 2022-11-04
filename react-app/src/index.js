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

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/auth/login",
    element: <Login />,
  },
  {
    path: "/auth/register",
    element: <Register />,
  },
  {
    path: "/auth/verify",
    element: <Verify />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>
);

