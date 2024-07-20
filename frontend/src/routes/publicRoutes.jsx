// src/routes/publicRoutes.js
import Home from 'src/components/containers/default/home';
import Contato from 'src/components/containers/default/contato';
import Login from 'src/components/containers/default/login';
import Cadastro from 'src/components/containers/default/cadastro';
import Erro from 'src/components/erro';
import React from 'react';

const publicRoutes = [
  {
    path: '/',
    exact: true,
    component: Home,
  },
  {
    path: '/Sobre',
    exact: true,
    component: Contato,
  },
  {
    path: '/login',
    exact: true,
    component: Login,
  },
  {
    path: '/cadastro',
    exact: true,
    component: Cadastro,
  },
  // Rota para erros internos do servidor
  {
    path: '/erro-interno',
    exact: true,
    component: () => <Erro title="Erro Interno" descricao="Ocorreu um erro interno no servidor. Tente novamente mais tarde." />,
  },
  // Rota para página não encontrada
  {
    path: '*',
    exact: true,
    component: () => <Erro title="Página Não Encontrada" descricao="A página que você está procurando não existe." />,
  },
];

export default publicRoutes;
