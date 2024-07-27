import {getCookie,setCookie} from './storage';
import { request } from './api';

export const useAuthentication = () => {

    const checkAuthentication = async () => {
      try {
        const retorno = await request("authentication", "GET");
        setCookie('authentication',retorno.authenticated);
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
      }  
    };
    const cookieValue = getCookie('authentication');
    if (cookieValue == null) {
      checkAuthentication();
    } 

  return cookieValue;
};
