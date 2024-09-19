// src/routes/privateRoutes.js
import Dashboard from 'src/components/containers/assinante/dashboard';

//import ListarUsuarios from 'src/components/containers/listar_usuarios';
//import ListaLojas from 'src/components/containers/lojas';
//import PDV from 'src/components/containers/pdv';
//import ListaProdutos from 'src/components/containers/produtos';
//import ListaVendas from 'src/components/containers/vendas';
import ClienteCreate from 'src/components/containers/cliente/ClienteCreate';
import ClienteEdit from 'src/components/containers/cliente/ClienteEdit';
import ClienteList from 'src/components/containers/cliente/ClienteLista';
//import Configuracao from 'src/components/container/assinante/configuracao';
const privateRoutes = [
  {
    path: '/dashboard',
    exact: true,
    component: Dashboard,
  },
  {
    path: '/usuarios',
    exact: true,
    //   component: ListarUsuarios,
  },
  {
    path: '/lojas',
    exact: true,
    //    component: ListaLojas,
  },
  {
    path: '/pdvs',
    exact: true,
    //  component: PDV,
  },
  {
    path: '/produtos',
    exact: true,
    //  component: ListaProdutos,
  },
  {
    path: '/vendas',
    exact: true,
    //  component: ListaVendas,
  },
  {
    path: '/clientes',
    exact: true,
    component: ClienteList,
  },
  {
    path: '/clientes/cadastrar',   // Rota para cadastro de cliente
    exact: true,
    component: ClienteCreate,      // Componente que lida com o cadastro de clientes
  },
  {
    path: '/clientes/editar/:id',  // Rota para editar cliente, usando o ID do cliente
    exact: true,
    component: ClienteEdit,        // Componente para editar cliente
  },
  {
    path: '/configuracao',
    exact: true,
    // component: Configuracao,
  },
];

export default privateRoutes;
