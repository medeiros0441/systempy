// src/routes/publicRoutes.js
import Home from '@containers/default/Home';
import Contato from '@containers/default/Contato';
import Login from '@containers/default/Login';
import Cadastro from '@containers/default/Cadastro';
import Erro from '@components/erro';
import React from 'react';

const publicRoutes = [
  {
    path: '/',
    component: Home,
  },
  {
    path: '/Sobre',
    component: Contato,
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/cadastro',
    component: Cadastro,
  },
  // Rota para erros internos do servidor
  {
    path: '/erro-interno',
    component: () => <Erro title="Erro Interno" descricao="Ocorreu um erro interno no servidor. Tente novamente mais tarde." />,
  },
  // Rota para página não encontrada
  {
    path: '*',
    component: () => <Erro title="Página Não Encontrada" descricao="A página que você está procurando não existe." />,
  },
];

export default publicRoutes;
