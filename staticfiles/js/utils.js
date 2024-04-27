class Utils {
   // Método para obter um item do local storage
   static getLocalStorageItem(key) {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
}

// Método para definir um item no local storage
static setLocalStorageItem(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}
// Método para recuperar o valor de um cookie pelo nome
    static getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [cookieName, cookieValue] = cookie.split('=').map(c => c.trim());
            if (cookieName === name) {
                return cookieValue;
            }
        }
        return null;
    }

    // Método para definir um cookie com um nome, valor e opções (opcional)
    static setCookie(name, value, options = {}) {
        options = {
            path: '/',
            ...options
        };

        if (options.expires instanceof Date) {
            options.expires = options.expires.toUTCString();
        }

        let updatedCookie = encodeURIComponent(name) + '=' + encodeURIComponent(value);

        for (let optionKey in options) {
            updatedCookie += '; ' + optionKey;
            let optionValue = options[optionKey];
            if (optionValue !== true) {
                updatedCookie += '=' + optionValue;
            }
        }

        document.cookie = updatedCookie;
    }
    // Método estático para formatar data e hora no formato brasileiro
    static formatarDataHoraBR(dataUTC, tipoRetorno = 0) {
        try {
            // Converte a string de data para um objeto Date
            const data = new Date(dataUTC);

            // Extrai os componentes de data e hora
            const dia = data.getDate().toString().padStart(2, '0');
            const mes = (data.getMonth() + 1).toString().padStart(2, '0');
            const ano = data.getFullYear();
            const hora = data.getHours().toString().padStart(2, '0');
            const minuto = data.getMinutes().toString().padStart(2, '0');

            let retorno = '';

            // Verifica o tipo de retorno desejado
            switch (tipoRetorno) {
                case 1: // Apenas a data
                    retorno = `${dia}/${mes}/${ano}`;
                    break;
                case 2: // Apenas o horário (hora e minutos)
                    retorno = `${hora}:${minuto}`;
                    break;
                default: // Data e hora com minutos
                    retorno = `${dia}/${mes}/${ano} ${hora}:${minuto}`;
            }

            // Retorna o valor formatado
            return retorno;
        } catch (error) {
            // Em caso de erro, retorna uma string vazia
            console.error("Erro ao formatar data/hora:", error);
            return '';
        }
        // Outros métodos...
    }
}