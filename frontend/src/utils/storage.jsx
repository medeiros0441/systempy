/**
 * Método para obter um item do localStorage.
 * @param {string} key - A chave do item que deseja obter.
 * @returns {any|null} O valor do item do localStorage, ou null se não encontrado.
 */
export const getLocalStorageItem = (key) => {
  // Obtém o item do localStorage pela chave
  const item = localStorage.getItem(key);
  // Se o item for encontrado, retorna seu valor como objeto JavaScript, caso contrário, retorna null
  return item ? JSON.parse(item) : null;
};

/**
 * Método para definir um item no localStorage.
 * @param {string} key - A chave do item que deseja definir.
 * @param {any} value - O valor do item que deseja armazenar.
 */
export const setLocalStorageItem = (key, value) => {
  // Converte o valor em uma string JSON e armazena no localStorage com a chave fornecida
  localStorage.setItem(key, JSON.stringify(value));
};

/**
 * Função para obter o valor de um cookie pelo nome.
 * @param {string} name - O nome do cookie que deseja obter.
 * @returns {string|null} O valor do cookie ou null se o cookie não for encontrado.
 */
export const getCookie = (name) => {
  // Divide todos os cookies da string document.cookie em um array
  const cookies = document.cookie.split(';');
  
  // Itera por cada cookie no array
  for (let cookie of cookies) {
    // Divide cada cookie em nome e valor e remove espaços em branco
    const [cookieName, cookieValue] = cookie.split('=').map(c => c.trim());
    
    // Verifica se o nome do cookie corresponde ao nome solicitado
    if (cookieName === name) {
      // Retorna o valor do cookie se encontrado
      return cookieValue;
    }
  }
  
  // Retorna null se o cookie não for encontrado
  return null;
};
export const setCookie = (name, value, timeInMinutes = 60, options = {}) => {
  // Define o caminho padrão como '/' e mescla com as opções fornecidas
  options = {
    path: '/',
    ...options
  };

  // Calcula a data de expiração com base no tempo em minutos
  const expires = new Date();
  expires.setTime(expires.getTime() + (timeInMinutes * 60 * 1000));
  options.expires = expires.toUTCString();

  // Converte a data de expiração para UTCString se for uma instância de Date
  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  // Constrói a string do cookie com nome e valor codificados
  let updatedCookie = encodeURIComponent(name) + '=' + encodeURIComponent(value);

  // Adiciona as opções à string do cookie
  for (let optionKey in options) {
    updatedCookie += '; ' + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += '=' + optionValue;
    }
  }

  // Define o cookie no documento
  document.cookie = updatedCookie;
};
