import { useState, useEffect } from 'react';
import request from './api';
import { getCookie, setCookie } from './storage';

// Função para tentar fazer login com os dados armazenados
const autoLogin = async (email, senha) => {
  try {
    const response = await request('public/login/', 'POST', { email, senha });
    return response.sucesso;
  } catch (error) {
    console.error('Erro ao autenticar:', error);
    return false;
  }
};
export const useAuthentication = () => {
  const [cookieValue, setCookieValue] = useState(() => getCookie('authentication'));

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await request('public/check-auth/');
        const isAuthenticated = response.sucesso && response.authenticated;
        console.log(isAuthenticated)
        setCookie('authentication', isAuthenticated);
        setCookieValue(isAuthenticated);

        if (!isAuthenticated) {
          const storedEmail = getCookie('email_LembrarMe');
          const storedSenha = getCookie('senha_LembrarMe');

          if (storedEmail && storedSenha) {
            const autoLoginSuccess = await autoLogin(storedEmail, storedSenha);
            setCookie('authentication', autoLoginSuccess);
            setCookieValue(autoLoginSuccess);
          }
        }
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        setCookie('authentication', false);
        setCookieValue(false);
      }
    };

    if (cookieValue === null) {
      checkAuthentication();
    }
  }, [cookieValue]);

  // Retorne o valor booleano diretamente
  return !!cookieValue; // Garante que o retorno é sempre booleano
};
