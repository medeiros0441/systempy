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
    }  static validateInputs(inputIDs) {
        var allInputsValid = true; // Inicializa como true
    
        function showError(input, message) {
            var feedbackElement = input.nextElementSibling;
            if (feedbackElement.classList.contains('invalid-feedback')) {
                feedbackElement.innerText = message;
            } else {
                feedbackElement = document.createElement('div');
                feedbackElement.className = 'invalid-feedback';
                feedbackElement.innerText = message;
                input.parentNode.appendChild(feedbackElement);
            }
            feedbackElement.style.fontSize = '0.5rem'; // Defina o tamanho de fonte desejado
            input.classList.add('is-invalid');
        }
    
        function removeError(input) {
            var feedbackElements = input.parentNode.querySelectorAll('.invalid-feedback');
            feedbackElements.forEach(function(element) {
                if (element.innerText === 'Preencha este campo.') {
                    element.remove();
                }
            });
            input.classList.remove('is-invalid');
        }
    
        function isEmpty(input) {
            return input.value.trim() === '';
        }
    
        function validateInput(input) {
            var errorShown = input.getAttribute('data-error-shown');
            if (isEmpty(input)) {
                if (!errorShown) {
                    showError(input, 'Preencha este campo.');
                    input.setAttribute('data-error-shown', 'true');
                }
                allInputsValid = false; // Define como false se um input estiver vazio
            } else {
                if (errorShown) {
                    removeError(input);
                    input.removeAttribute('data-error-shown');
                }
            }
        }
    
        inputIDs.forEach(function(id) {
            var input = document.getElementById(id);
            if (!input) {
                console.error('Elemento de input não encontrado com o ID: ' + id);
                return; // Se o elemento de input não for encontrado, saia da iteração atual
            }
    
            // Adiciona um ouvinte de evento de entrada para monitorar as alterações nos inputs
            input.addEventListener('input', function() {
                validateInput(input);
            });
    
            // Executa a validação inicialmente
            validateInput(input);
        });
    
        // Retorna allInputsValid ao final da função
        return allInputsValid;
    }
    static converterStringParaData(dataString) {
        try {
            const partes = dataString.split(/[\s\/:]/); // Divide a string em partes usando espaço, barra ou dois pontos como delimitadores
            if (partes.length !== 5) {
                throw new Error('Formato de data inválido. Deve ser "dia/mês/ano hora:minuto".');
            }
    
            const dia = parseInt(partes[0], 10);
            const mes = parseInt(partes[1], 10) - 1; // Mês é base zero
            const ano = parseInt(partes[2], 10);
            const hora = parseInt(partes[3], 10);
            const minuto = parseInt(partes[4], 10);
    
            if (isNaN(dia) || isNaN(mes) || isNaN(ano) || isNaN(hora) || isNaN(minuto)) {
                throw new Error('Valores de data inválidos.');
            }
    
            return new Date(ano, mes, dia, hora, minuto);
        } catch (error) {
            console.error('Erro ao converter string para data:', error.message);
            return null;
        }
    }
    
}
    