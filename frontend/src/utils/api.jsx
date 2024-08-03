import axios from 'axios';
import Cookies from 'js-cookie';

// Configura Axios para incluir o token CSRF e suportar cookies
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';  // Nome do cookie CSRF
axios.defaults.xsrfHeaderName = 'X-CSRFToken'; // Nome do cabeçalho CSRF

// Função genérica para fazer requisições API
export default function request(url, method = 'GET', data = null) {
  const csrfToken = Cookies.get('csrftoken');  // Obtém o token CSRF dos cookies

  return axios({
    url,                     // URL da API
    method,                  // Método HTTP
    headers: {
      'X-CSRFToken': csrfToken,  // Inclui o token CSRF no cabeçalho
      'Content-Type': 'application/json',  // Tipo de conteúdo JSON
    },
    data,                    // Dados para o método POST ou PUT
  })
    .then(response => response.data)   // Retorna a resposta dos dados
    .catch(error => {
      console.error('Erro na requisição:', error);
      throw error;
    });
};
