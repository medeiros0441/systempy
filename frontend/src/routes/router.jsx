import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import publicRoutes from './publicRoutes';
import privateRoutes from './privateRoutes';
import { useAuthentication } from '../utils/auth';

const Router = () => {
  const isAuthenticated = useAuthentication(); // Use o hook no nível superior

  return (
    <Routes>
      {/* Rotas públicas */}
      {publicRoutes.map((route, index) => (
        <Route
          key={index}
          path={route.path}
          element={<route.component />}
          exact={route.exact}
        />
      ))}

      {/* Rotas privadas */}
      {privateRoutes.map((route, index) => (
        <Route
          key={index}
          path={route.path}
          element={
            isAuthenticated ? (
              <route.component />
            ) : (
              <Navigate to="/login" />
            )
          }
          exact={route.exact}
        />
      ))}
    </Routes>
  );
};

export default Router;
