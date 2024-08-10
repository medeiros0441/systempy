import axios from 'axios';
import Cookies from 'js-cookie';

// Função para obter o token CSRF do backend
async function fetchCsrfToken() {
  try {
    const response = await axios.get('/api/csrf-token/');
    const token = response.data.csrfToken;
    Cookies.set('csrftoken', token);  // Armazena o token nos cookies
    return token;
  } catch (error) {
    console.error('Erro ao obter o token CSRF:', error);
    throw error;
  }
}

// Configura Axios para suportar cookies e definir o token CSRF globalmente
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';  // Nome do cookie CSRF
axios.defaults.xsrfHeaderName = 'X-CSRFToken'; // Nome do cabeçalho CSRF

// Configura um interceptador de requisição para atualizar o token CSRF dinamicamente
axios.interceptors.request.use(async config => {
  let csrfToken = Cookies.get('csrftoken');  // Obtém o token CSRF dos cookies

  if (!csrfToken) {
    csrfToken = await fetchCsrfToken();
  }

  const userToken = Cookies.get('user_token');
  if (userToken) {
    // Inclui o token usuário no cabeçalho Authorization
    config.headers['Authorization'] = `Bearer ${userToken}`;
  }


  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;  // Inclui o token CSRF no cabeçalho
  }

  return config;
}, error => Promise.reject(error));

// Função genérica para fazer requisições API
export default async function request(url, method = 'GET', data = null) {
  try {
    // Adiciona a barra no final da URL se não estiver presente
    const formattedUrl = url.endsWith('/') ? url : `${url}/`;
    const apiUrl = `/api/${formattedUrl}`;  // Corrige a variável para a URL

    const response = await axios({
      url: apiUrl,              // URL da API
      method,                   // Método HTTP
      headers: {
        'Content-Type': 'application/json',  // Tipo de conteúdo JSON
      },
      data,                     // Dados para o método POST ou PUT
    });

    // Retorna sucesso com os dados da resposta dentro do objeto data
    return { success: true, ...response.data };
  } catch (error) {
    // Lida com diferentes tipos de erro e exibe mensagens apropriadas
    const errorMessage = getErrorMessage(error);
    console.error('Erro na requisição:', errorMessage);
    // Retorna o erro dentro do objeto data com sucesso como false
    return { success: false, message: errorMessage };
  }
}

// Função para gerar a mensagem de erro
function getErrorMessage(error) {
  if (error.response) {
    // A resposta da API contém informações sobre o erro
    switch (error.response.status) {
      case 400:
        return error.response.data.message || 'Solicitação inválida.';
      case 401:
        return error.response.data.message || 'Não autorizado.';
      case 403:
        return error.response.data.message || 'Acesso negado.';
      case 404:
        return error.response.data.message || 'Recurso não encontrado.';
      case 500:
        return error.response.data.message || 'Erro interno do servidor.';
      default:
        return error.response.data.message || 'Erro na requisição.';
    }
  } else if (error.request) {
    // A requisição foi feita, mas não houve resposta
    return 'Nenhuma resposta recebida do servidor.';
  } else {
    // Outro erro ocorreu ao configurar a requisição
    return error.message || 'Erro ao configurar a requisição.';
  }
}