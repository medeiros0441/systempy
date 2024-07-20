// src/routes/privateRoutes.js
import Dashboard from 'src/components/containers/assinante/dashboard';

//import ListarUsuarios from 'src/components/containers/listar_usuarios';
//import ListaLojas from 'src/components/containers/lista_lojas';
//import PDV from 'src/components/containers/pdv';
//import ListaProdutos from 'src/components/containers/lista_produtos';
//import ListaVendas from 'src/components/containers/lista_vendas';
//import ListaClientes from 'src/components/containers/lista_clientes';
//import Configuracao from 'src/components/container/assinante/configuracao';
const privateRoutes = [
  {
    path: '/dashboard',
    exact: true,
    component: Dashboard,
  },
  {
    path: '/listar_usuarios',
    exact: true,
 //   component: ListarUsuarios,
  },
  {
    path: '/lista_lojas',
    exact: true,
//    component: ListaLojas,
  },
  {
    path: '/pdv',
    exact: true,
  //  component: PDV,
  },
  {
    path: '/lista_produtos',
    exact: true,
  //  component: ListaProdutos,
  },
  {
    path: '/lista_vendas',
    exact: true,
  //  component: ListaVendas,
  },
  {
    path: '/lista_clientes',
    exact: true,
   // component: ListaClientes,
  },
  {
    path: '/configuracao',
    exact: true,
   // component: Configuracao,
  },
];

export default privateRoutes;
