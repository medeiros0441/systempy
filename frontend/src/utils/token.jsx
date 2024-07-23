import { getCookie } from './storage';

/**
 * Função para obter o token do cookie.
 * @returns {Object} Objeto contendo o status de sucesso e o token ou a mensagem de erro.
 */
export const getToken = (name_token) => {
  try {
    // Obtém o token do cookie 'token_user'
    const token_user = getCookie(name_token);

    // Verifica se o token é válido (não nulo, não indefinido e não vazio)
    if (token_user) {
      // Retorna um objeto indicando sucesso e o token obtido
      return { success: true, token: token_user };
    } else {
      // Caso o token seja inválido, retorna um objeto indicando falha
      return { success: false, error: 'Token não encontrado ou inválido' };
    }
  } catch (error) {
    // Em caso de erro, exibe a mensagem de erro no console e retorna um objeto indicando falha
    console.error('Erro ao obter o token:', error);
    return { success: false, error: error.message };
  }
};
