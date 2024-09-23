import React, { useState } from 'react';
import Formulario from '@objetos/Formulario';
import Input from '@objetos/Input';
import Select from '@objetos/Select';
import UsuarioService from '@services/UsuarioService';
import alerta from '@utils/alerta';
import { useNavigate } from 'react-router-dom';
import { isValidEmail } from 'src/utils/validate';

const UsuarioCreate = () => {
    const [formValues, setFormValues] = useState({
        nome_completo: '',
        email: '',
        senha: '',
        senhaConfirm: '',
        nivel_usuario: '0', // Alterado para string
        status_acesso: false,
    });
    const navigate = useNavigate();

    const nivelUsuarioOptions = [
        { value: '0', label: 'Selecionar Nível' },
        { value: '1', label: 'Administrador' },
        { value: '2', label: 'Gerente' },
        { value: '3', label: 'Colaborador' },
    ];

    const handleChange = ({ target: { name, value } }) => {
        setFormValues((prevValues) => ({
            ...prevValues,
            [name]: value,
        }));
    };

    const validatePayload = ({ nome_completo, email, senha }) => {
        const errors = [];
        if (!nome_completo.trim()) errors.push('Nome completo é obrigatório.');
        if (!isValidEmail(email)) errors.push('E-mail inválido.');
        if (!senha.trim()) errors.push('Senha é obrigatória.');
        return errors;
    };

    const handleValidatePassword = () => {
        const { senha, senhaConfirm } = formValues;
        const isValidSenha =
            senha.length >= 8 &&
            /[A-Z]/.test(senha) && // Pelo menos uma letra maiúscula
            /[a-z]/.test(senha) && // Pelo menos uma letra minúscula
            /[0-9]/.test(senha);   // Pelo menos um número

        return isValidSenha && senha === senhaConfirm;
    };

    const handleSubmit = async () => {
        const errors = validatePayload(formValues);
        if (errors.length > 0) {
            alerta(`Erro:\n${errors.join('\n')}`);
            return;
        }

        if (!handleValidatePassword()) {
            alerta('Erro: Senha inválida ou não coincide.');
            return;
        }

        try {
            const response = await UsuarioService.createUsuario(formValues);
            if (response.sucesso) {
                navigate('/usuarios');
                alerta('Usuário criado com sucesso!');
            } else {
                alerta(response.message);
            }
        } catch {
            navigate('/usuarios');
            alerta('Erro ao criar usuário');
        }
    };

    const handleClear = () => {
        setFormValues({
            nome_completo: '',
            email: '',
            senha: '',
            senhaConfirm: '',
            nivel_usuario: '0', // Alterado para string
            status_acesso: false,
        });
    };

    const headerIcon = 'person'; // Ícone do header
    const headerTitle = 'Criar Novo Usuário'; // Título do header

    const formBody = (
        <>
            <Input
                id="nome_completo"
                name="nome_completo"
                value={formValues.nome_completo}
                label="Nome Completo"
                onChange={handleChange}
            />
            <Select
                id="nivel_usuario"
                name="nivel_usuario"
                value={formValues.nivel_usuario}
                label="Nível de Usuário"
                options={nivelUsuarioOptions}
                onChange={handleChange}
            />
            <Input
                id="email"
                name="email"
                value={formValues.email}
                label="E-mail"
                onChange={handleChange}
                type="email"
            />
            <Input
                id="senha"
                name="senha"
                value={formValues.senha}
                label="Senha"
                onChange={handleChange}
                type="password"
            />
            <Input
                id="senhaConfirm"
                name="senhaConfirm"
                value={formValues.senhaConfirm}
                label="Confirmação da Senha"
                onChange={handleChange}
                type="password"
            />
        </>
    );

    return (
        <Formulario
            headerIcon={headerIcon}
            headerTitle={headerTitle}
            formBody={formBody}
            footerLeftButtonText="Limpar"
            footerLeftButtonAction={handleClear}
            footerRightButtonText="Salvar"
            footerRightButtonAction={handleSubmit}
        />
    );
};

export default UsuarioCreate;
