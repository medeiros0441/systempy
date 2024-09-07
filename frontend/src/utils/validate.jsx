// Função para validar CPF
const isValidCPF = (cpf) => {
    cpf = cpf.replace(/[^\d]+/g, ''); // Remove caracteres não numéricos

    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false; // Verifica se todos os dígitos são iguais

    let sum = 0;
    let remainder;

    // Valida o primeiro dígito
    for (let i = 1; i <= 9; i++) sum += parseInt(cpf.charAt(i - 1)) * (11 - i);
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.charAt(9))) return false;

    sum = 0;
    // Valida o segundo dígito
    for (let i = 1; i <= 10; i++) sum += parseInt(cpf.charAt(i - 1)) * (12 - i);
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.charAt(10))) return false;

    return true;
};

// Função para validar CNPJ
const isValidCNPJ = (cnpj) => {
    cnpj = cnpj.replace(/[^\d]+/g, ''); // Remove caracteres não numéricos

    if (cnpj.length !== 14 || /^(\d)\1{13}$/.test(cnpj)) return false; // Verifica se todos os dígitos são iguais

    let sum = 0;
    let remainder;

    // Valida o primeiro dígito
    const firstWeights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    for (let i = 0; i < 12; i++) sum += parseInt(cnpj.charAt(i)) * firstWeights[i];
    remainder = sum % 11;
    if (remainder < 2) remainder = 0;
    else remainder = 11 - remainder;
    if (remainder !== parseInt(cnpj.charAt(12))) return false;

    sum = 0;
    // Valida o segundo dígito
    const secondWeights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    for (let i = 0; i < 13; i++) sum += parseInt(cnpj.charAt(i)) * secondWeights[i];
    remainder = sum % 11;
    if (remainder < 2) remainder = 0;
    else remainder = 11 - remainder;
    if (remainder !== parseInt(cnpj.charAt(13))) return false;

    return true;
};

// Função para validar CEP
const isValidCEP = (cep) => {
    const cepRegex = /^\d{5}-\d{3}$/;
    return cepRegex.test(cep);
};
// Função para validar data no formato dd/mm/yyyy
const isValidDate = (date) => {
    const dateRegex = /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/;
    if (!dateRegex.test(date)) return false;

    const [day, month, year] = date.split('/').map(Number);
    const isLeapYear = (year) => (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);

    if (month === 2) {
        if (isLeapYear(year)) return day <= 29;
        return day <= 28;
    }

    if ([4, 6, 9, 11].includes(month)) return day <= 30;

    return day <= 31;
};
// Função para validar telefone
const isValidPhone = (phone) => {
    const phoneRegex = /^(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}$/;
    return phoneRegex.test(phone);
};

// Função para validar e-mail
const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

export { isValidEmail, isValidCNPJ, isValidCPF, isValidPhone, isValidDate, isValidCEP };
