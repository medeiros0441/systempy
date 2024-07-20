// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Base from './components/Base'; // Importe seu componente Base aqui
import RouterConfig from './routes/router'; // Importe o componente Router aqui

const App = ({ isCliente = false }) => (
  <Router>
    <Base isCliente={isCliente}>
      <RouterConfig />
    </Base>
  </Router>
);

export default App;
