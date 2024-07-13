
import Cookies from 'js-cookie';

// Verifica se o usuário está autenticado verificando a presença de email e senha nos cookies
export const isAuthenticated = () => {
  const email = Cookies.get('email');
  const senha = Cookies.get('senha');
  return email !== undefined && senha !== undefined;
};

// Função de login que armazena email e senha nos cookies
export const login = (email, senha) => {
  Cookies.set('email', email, { expires: 7 }); // Expira em 7 dias
  Cookies.set('senha', senha, { expires: 7 }); // Expira em 7 dias
};

// Função de logout que remove email e senha dos cookies
export const logout = () => {
  Cookies.remove('email');
  Cookies.remove('senha');
};