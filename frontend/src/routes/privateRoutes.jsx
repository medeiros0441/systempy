// src/routes/privateRoutes.js
import React from 'react';
import Dashboard from '@containers/assinante/dashboard';
import ClienteCreate from '@containers/cliente/ClienteCreate';
import ClienteEdit from '@containers/cliente/ClienteEdit';
import ClienteList from '@containers/cliente/ClienteList';
import ClienteView from '@containers/cliente/ClienteView';

import UsuarioEdit from '@containers/usuario/UsuarioEdit';
import UsuarioList from '@containers/usuario/UsuarioList';
import UsuarioView from '@containers/usuario/UsuarioView';
import UsuarioCreate from '@containers/usuario/UsuarioCreate';

const Placeholder = ({ title }) => (
  <div className="d-flex justify-content-center align-items-center vh-100">
    <div className="text-center">
      <h1>{title}</h1>
      <p>Este recurso ainda está em desenvolvimento.</p>
    </div>
  </div>
);

const privateRoutes = [
  {
    path: '/dashboard',
    component: Dashboard,
  },
  {
    path: '/usuarios',
    component: UsuarioList, // Rota para listar usuários
  },
  {
    path: '/usuarios/cadastrar', // Rota para cadastro de usuário
    component: UsuarioCreate, // Componente que lida com o cadastro de usuários
  },
  {
    path: '/usuarios/editar/:id', // Rota para editar usuário, usando o ID do usuário
    component: UsuarioEdit, // Componente para editar usuário
  },
  {
    path: '/usuarios/visualizar/:id', // Rota para visualizar usuário
    component: UsuarioView, // Componente para visualizar usuário
  },

  {
    path: '/lojas',
    component: () => <Placeholder title="Lojas" />, // Placeholder para lojas
  },
  {
    path: '/pdvs',
    component: () => <Placeholder title="PDVs" />, // Placeholder para PDVs
  },
  {
    path: '/produtos',
    component: () => <Placeholder title="Produtos" />, // Placeholder para produtos
  },
  {
    path: '/vendas',
    component: () => <Placeholder title="Vendas" />, // Placeholder para vendas
  },
  {
    path: '/clientes',
    component: ClienteList, // Rota para listar clientes
  },
  {
    path: '/clientes/cadastrar', // Rota para cadastro de cliente
    component: ClienteCreate, // Componente que lida com o cadastro de clientes
  },
  {
    path: '/clientes/editar/:id', // Rota para editar cliente, usando o ID do cliente
    component: ClienteEdit, // Componente para editar cliente
  },
  {
    path: '/clientes/visualizar/:id', // Rota para visualizar cliente
    component: ClienteView, // Componente para visualizar cliente
  },
  {
    path: '/configuracao',
    component: () => <Placeholder title="Configuração" />, // Placeholder para configuração
  },
];

export default privateRoutes;
