import React, { useState } from 'react';
import Formulario from '@objetos/Formulario';
import Input from '@objetos/Input';
import Select from '@objetos/Select';
import ClienteService from '@services/ClienteService';
import alerta from '@utils/alerta';
import { useNavigate } from 'react-router-dom'; // Importa useParams e useNavigate

const ClienteCreate = () => {
    const [formValues, setFormValues] = useState({
        nome: '',
        telefone: '',
        tipo_cliente: '',
        descricao: '',
    });
    const navigate = useNavigate(); // Inicializa o hook useNavigate

    const tipoClienteOptions = [
        { value: '', label: 'Selecionar' },
        { value: 'fisica', label: 'Pessoa Física' },
        { value: 'juridica', label: 'Pessoa Jurídica' },
    ];

    const handleChange = ({ target: { name, value } }) => {
        setFormValues((prevValues) => ({
            ...prevValues,
            [name]: value,
        }));
    };

    const validatePayload = ({ nome, telefone, tipo_cliente }) => {
        const errors = [];
        if (!nome.trim()) errors.push('Nome do cliente é obrigatório.');
        if (!telefone.trim()) errors.push('Telefone é obrigatório.');
        if (!tipo_cliente.trim()) errors.push('Tipo de cliente é obrigatório.');
        return errors;
    };

    const handleSubmit = async () => {
        const errors = validatePayload(formValues);
        if (errors.length > 0) {
            alerta(`Erro:\n${errors.join('\n')}`);
            return;
        }

        try {
            const response = await ClienteService.createCliente(formValues);
            if (response.sucesso) {
                navigate('/clientes');
                alerta('Cliente criado com sucesso!');
            } else {
                alerta(response.message);
            }
        } catch {
            navigate('/clientes');
            alerta('Erro ao criar cliente');
        }
    };

    const handleClear = () => {
        setFormValues({
            nome: '',
            telefone: '',
            tipo_cliente: '',
            descricao: '',
        });
    };

    const headerIcon = 'person'; // Ícone do header
    const headerTitle = 'Criar Novo Cliente'; // Título do header

    const formBody = (
        <>
            <Input
                id="nome"
                name="nome"
                value={formValues.nome}
                label="Nome do Cliente"
                onChange={handleChange}
            />
            <Input
                id="telefone"
                name="telefone"
                value={formValues.telefone}
                label="Telefone"
                onChange={handleChange}
                type="tel"
            />
            <Select
                id="tipo_cliente"
                name="tipo_cliente"
                value={formValues.tipo_cliente}
                label="Tipo de Cliente"
                options={tipoClienteOptions}
                onChange={handleChange}
            />
            <Input
                id="descricao"
                name="descricao"
                value={formValues.descricao}
                label="Descrição"
                onChange={handleChange}
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

export default ClienteCreate;
