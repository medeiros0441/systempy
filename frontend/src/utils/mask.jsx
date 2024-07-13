import Cleave from 'cleave.js';

// Função para inicializar máscaras
function initializeMasks() {
    new Cleave('.cnpj-mask', {
        delimiters: ['.', '.', '/', '-'],
        blocks: [2, 3, 3, 4, 2],
        numericOnly: true
    });

    new Cleave('.cpf-mask', {
        delimiters: ['.', '.', '-'],
        blocks: [3, 3, 3, 2],
        numericOnly: true
    });

    new Cleave('.telefone-mask', {
        delimiters: ['+', ' ', '(', ') ', '-'],
        blocks: [2, 2, 4, 5],
        numericOnly: true
    });

    new Cleave('.codigo-mask', {
        delimiters: ['-'],
        blocks: [3, 3],
        numericOnly: true
    });

    new Cleave('.cep-mask', {
        delimiters: ['-'],
        blocks: [5, 3],
        numericOnly: true
    });

    new Cleave('.data-mask', {
        delimiters: ['/'],
        blocks: [2, 2, 4],
        numericOnly: true
    });

    new Cleave('.data-mes-ano-mask', {
        delimiters: ['/'],
        blocks: [2, 4],
        numericOnly: true
    });

    new Cleave('.quantidade-mask', {
        blocks: [8],
        numericOnly: true
    });

    new Cleave('.money-mask', {
        delimiters: ['.', '.', ','],
        blocks: [3, 3, 3, 2],
        numericOnly: true,
        reverse: true
    });
}

// Inicializar máscaras ao carregar a página
document.addEventListener('DOMContentLoaded', initializeMasks);
