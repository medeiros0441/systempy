import axios from 'axios';

// Função para obter o token de acesso
export const getAccessToken = () => localStorage.getItem('jwt_token');

// Função para obter o token de atualização
export const getRefreshToken = () => localStorage.getItem('refresh_token');

// Função para atualizar o token de acesso
export const refreshAccessToken = () => {
  return new Promise((resolve, reject) => {
    axios.post('/api/token/refresh/', {
      refresh: getRefreshToken(),
    })
    .then((response) => {
      const newAccessToken = response.data.access;
      localStorage.setItem('jwt_token', newAccessToken);
      resolve(newAccessToken);
    })
    .catch((error) => {
      console.error('Erro ao atualizar o token de acesso:', error);
      reject(error);
    });
  });
};

// Função para obter o token
export const getToken = async (username, password) => {
  try {
    const response = await axios.post('/api/token/', { username, password });
    if (response.status === 200) {
      // Armazenar os tokens no localStorage
      localStorage.setItem('jwt_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      return { success: true, token: response.data.access };
    }
  } catch (error) {
    console.error('Erro ao obter o token:', error);
    return { success: false, error: error.message };
  }
};
