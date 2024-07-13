import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import routes from './routes/default';
import Base from './components/Base';
import { isAuthenticated } from './utils/auth';

const App = () => {
  return (
    <Router>
      <Base>
        <Routes>
          {routes.map((route, index) => {
            if (route.private) {
              return (
                <Route 
                  key={index}
                  path={route.path}
                  element={isAuthenticated() ? <route.component /> : <Navigate to="/login" />}
                />
              );
            } else {
              return (
                <Route 
                  key={index}
                  path={route.path}
                  element={<route.component />}
                />
              );
            }
          })}
        </Routes>
      </Base>
    </Router>
  );
};

export default App;
