import React from 'react';
import Home from '../components/containers/default/home';
import Contato from '../components/containers/default/contato';
import Login from '../components/containers/default/login';
import Cadastro from '../components/containers/default/cadastro';
import NotFound from '../components/notfound';

const routes = [
  {
    path: '/',
    exact: true,
    component: Home,
    private: false // Rota pública
  },
  {
    path: '/contato',
    exact: true,
    component: Contato,
    private: false // Rota pública
  },
  {
    path: '/login',
    exact: true,
    component: Login,
    private: false // Rota pública
  },
  {
    path: '/cadastro',
    exact: true,
    component: Cadastro,
    private: false // Rota pública
  },
  {
    path: '/dashboard',
    exact: true,
    component: Home,
    private: true // Rota privada
  },
  {
    path: '*',
    component: NotFound
  }
];

export default routes;
