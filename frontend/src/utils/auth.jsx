
import {getCookie} from './storage';

// Verifica se o usuário está autenticado verificando a presença de email e senha nos cookies
export const isAuthenticated = () => {
  const id_usuario = getCookie('id_usuario');
  const id_empresa = getCookie('id_empresa');
  return id_empresa !== undefined && id_usuario !== undefined;
};
  