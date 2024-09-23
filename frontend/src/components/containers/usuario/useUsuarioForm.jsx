import React, { useState, useEffect, useCallback } from 'react';
import Input from '@objetos/Input';
import Select from '@objetos/Select';
import Label from '@objetos/Label';
import UsuarioService from '@services/UsuarioService';
import UsuarioInterface from '@interface/UsuarioInterface';
import alerta from '@utils/alerta';

const useUsuarioForm = (id, isEditable) => {
    const [formValues, setFormValues] = useState({
        nome_completo: '',
        nome_usuario: '',
        senha: '',
        nivel_usuario: 0,
        status_acesso: false,
        email: '',
        ultimo_login: null,
        empresa: '',
    });
    const [usuario, setUsuario] = useState({});

    const showMessage = (message) => alerta(message);

    const fetchUsuario = useCallback(async () => {
        if (!id) {
            showMessage('ID do usuário não fornecido');
            return;
        }

        try {
            const response = await UsuarioService.getUsuario(id);
            if (response.sucesso) {
                const usuarioData = UsuarioInterface.fromApiResponse(response.data);
                setFormValues(usuarioData);
                setUsuario(usuarioData);
            } else {
                showMessage(response.message);
            }
        } catch {
            showMessage('Erro ao buscar usuário');
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            fetchUsuario();
        }
    }, [id, fetchUsuario]);

    const handleChange = (event) => {
        const { name, value, type, checked } = event.target;
        const newValue = type === 'checkbox' ? checked : value;
        setFormValues((prevValues) => ({
            ...prevValues,
            [name]: newValue,
        }));
    };

    const validatePayload = ({ nome_completo, nome_usuario, email }) => {
        const errors = [];
        if (!nome_completo.trim()) errors.push('Nome completo é obrigatório.');
        if (!nome_usuario.trim()) errors.push('Nome de usuário é obrigatório.');
        if (!email.trim()) errors.push('Email é obrigatório.');
        return errors;
    };

    const handleSubmit = async () => {
        const errors = validatePayload(formValues);
        if (errors.length > 0) {
            showMessage(`Erro:\n${errors.join('\n')}`);
            return;
        }

        try {
            const response = await UsuarioService.updateUsuario(id, formValues);
            if (response.sucesso) {
                showMessage('Usuário atualizado com sucesso!');
            } else {
                showMessage(response.message);
            }
        } catch {
            showMessage('Erro ao atualizar usuário');
        }
    };

    const renderForm = () => (
        <div>
            <Input id="nome_completo" name="nome_completo" value={formValues.nome_completo} label="Nome Completo" onChange={handleChange} />
            <Input id="nome_usuario" name="nome_usuario" value={formValues.nome_usuario} label="Nome de Usuário" onChange={handleChange} />
            <Input id="senha" name="senha" value={formValues.senha} label="Senha" onChange={handleChange} type="password" />
            <Select
                id="nivel_usuario"
                name="nivel_usuario"
                value={formValues.nivel_usuario}
                label="Nível de Usuário"
                options={[
                    { value: 0, label: 'Usuário Comum' },
                    { value: 1, label: 'Administrador' },
                ]}
                onChange={handleChange}
            />
            <Input
                id="status_acesso"
                name="status_acesso"
                value={formValues.status_acesso}
                label="Status de Acesso"
                type="checkbox"
                checked={formValues.status_acesso}
                onChange={handleChange}
            />
            <Input id="email" name="email" value={formValues.email} label="Email" onChange={handleChange} />
            <Input id="empresa" name="empresa" value={formValues.empresa} label="Empresa" onChange={handleChange} />
        </div>
    );

    const renderLabels = () => (
        <div>
            <Label htmlFor="nome_completo" title="Nome Completo:" value={usuario.nome_completo || ''} iconClass="person" />
            <Label htmlFor="nome_usuario" title="Nome de Usuário:" value={usuario.nome_usuario || ''} iconClass="person" />
            <Label htmlFor="email" title="Email:" value={usuario.email || ''} iconClass="envelope" />
            <Label htmlFor="nivel_usuario" title="Nível de Usuário:" value={usuario.nivel_usuario === 0 ? 'Usuário Comum' : 'Administrador'} iconClass="shield" />
            <Label htmlFor="status_acesso" title="Status de Acesso:" value={usuario.status_acesso ? 'Ativo' : 'Inativo'} iconClass="check-circle" />
            <Label htmlFor="ultimo_login" title="Último Login:" value={usuario.ultimo_login || 'Nunca'} iconClass="clock" />
            <Label htmlFor="empresa" title="Empresa:" value={usuario.empresa || ''} iconClass="building" />
        </div>
    );

    return isEditable ? { handleSubmit, renderForm } : { renderForm: renderLabels };
};

export default useUsuarioForm;
