import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import publicRoutes from './publicRoutes';
import privateRoutes from './privateRoutes';
import { useAuth } from '../utils/auth';

const Router = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* Rotas públicas */}
      {publicRoutes.map((route, index) => (
        <Route
          key={index}
          path={route.path}
          element={<route.component />} // Verifique se route.component está definido
        />
      ))}

      {/* Rotas privadas */}
      {privateRoutes.map((route, index) => (
        <Route
          key={index}
          path={route.path}
          element={
            isAuthenticated ? (
              <route.component /> // Verifique se route.component está definido
            ) : (
              <Navigate to="/login" />
            )
          }
        />
      ))}
    </Routes>
  );
};

export default Router;
