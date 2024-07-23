
import {request} from './api';
// Verifica se o usuário está autenticado verificando a presença de email e senha nos cookies
export const isAuthenticated  = async () => { 
 const retorno = await request("authentication","GET");
  if(retorno.sucess){
    console.log(retorno.menssag);
   return retorno.authenticated;
  }
  else{
    console.log(retorno.menssag);
  return false
  }
};
  