import axios from 'axios';
import { getToken } from './token';
import Cookies from 'js-cookie';

const token = Cookies.get('csrftoken'); // Obtém o token CSRF do cookie
console.log('CSRF Token:', token); // Verifica se o token CSRF está sendo obtido corretamente

// Configurações padrão do Axios
const axiosInstance = axios.create({
  baseURL: '/api/', // Substitua pela URL base da sua API
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
  },
});

console.log('Axios Configuração:', axiosInstance.defaults); // Verifica a configuração do Axios

/**
 * Função genérica para fazer requisições HTTP
 * @param {string} url - URL da requisição
 * @param {string} method - Método HTTP (GET, POST, PUT, DELETE)
 * @param {object} [data] - Dados a serem enviados no corpo da requisição (para POST e PUT)
 * @param {object} [config] - Configurações adicionais do Axios
 * @returns {Promise<object>} - Retorna uma Promise com um objeto contendo sucesso, dados e mensagem
 */
export const request = (url, method, data = null, config = {}) => {
  // Adiciona o token de autenticação ao cabeçalho
  const retorn = getToken("token_user");
  console.log('Token de Autenticação:', retorn); // Verifica o token de autenticação obtido

  const headers = {
    ...config.headers,
    ...(retorn.success ? { Authorization: `Bearer ${retorn.token}` } : {}),
  };

  console.log('Headers da Requisição:', headers); // Verifica os cabeçalhos da requisição

  return axiosInstance({
    url,
    method,
    data,
    headers,
    ...config,
  })
    .then(response => {
      console.log('Resposta da Requisição:', response); // Verifica a resposta da requisição

      let result = {
        success: true,
        data: null,
        message: 'Requisição bem-sucedida',
      };

      switch (response.status) {
        case 200:
        case 201:
          result.data = response.data;
          break;
        case 204:
          result.message = 'Recurso deletado com sucesso';
          break;
        default:
          result.message = 'Resposta recebida';
          result.data = response.data;
          break;
      }

      return result;
    })
    .catch(error => {
      console.log('Erro na Requisição:', error); // Verifica o erro da requisição

      let result = {
        success: false,
        data: null,
        message: 'Erro na requisição',
      };

      if (error.response) {
        result.message = `Erro ${error.response.status}: ${error.response.data.message || 'Erro desconhecido'}`;
      } else if (error.request) {
        result.message = 'Erro na requisição: Não foi possível receber resposta da API';
      } else {
        result.message = `Erro ao configurar a requisição: ${error.message}`;
      }

      return result;
    });
};
