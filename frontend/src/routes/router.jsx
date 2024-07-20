// src/routes/Router.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import publicRoutes from './publicRoutes';
import privateRoutes from './privateRoutes';
import { isAuthenticated } from '../utils/auth';

const Router = () => (
  <Routes>
    {publicRoutes.map((route, index) => (
      <Route
        key={index}
        path={route.path}
        element={<route.component />}
        exact={route.exact}
      />
    ))}
    {privateRoutes.map((route, index) => (
      <Route
        key={index}
        path={route.path}
        element={isAuthenticated() ? <route.component /> : <Navigate to="/login" />}
        exact={route.exact}
      />
    ))}
  </Routes>
);

export default Router;
