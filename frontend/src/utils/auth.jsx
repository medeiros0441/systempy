import { getCookie, setCookie } from './storage';
import request from './api';
import { useState, useEffect } from 'react';


export const useAuthentication = () => {
  const [cookieValue, setCookieValue] = useState(() => getCookie('authentication'));

  useEffect(() => {
    // Função assíncrona dentro do useEffect
    const checkAuthentication = async () => {
      try {
        const response = await request("public/check-auth/", "GET");
        if (response.success) { // Verifica se a resposta foi bem-sucedida
          setCookie('authentication', response.data.authenticated);
          setCookieValue(response.data.authenticated);
        } else {
          console.error('Autenticação falhou:', response.message);
        }
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
      }
    };

    // Só faz a verificação se o cookie ainda não estiver definido
    if (cookieValue == null) {
      checkAuthentication();
    }
  }, [cookieValue]);

  return cookieValue;
};
