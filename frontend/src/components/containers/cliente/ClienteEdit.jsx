import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom'; // Importa useParams e useNavigate
import ClienteService from 'src/services/ClienteService';
import ClienteInterface from 'src/interface/ClienteInterface';
import loading from 'src/utils/loading';
import alerta from 'src/utils/alerta';
import Input from 'src/components/objetos/Input';
import Select from 'src/components/objetos/Select';
import Formulario from 'src/components/objetos/Formulario';

const ClienteEdit = () => {
    const [formValues, setFormValues] = useState({
        nome: '',
        telefone: '',
        tipo_cliente: '',
        descricao: '',
    });

    const navigate = useNavigate(); // Inicializa o hook useNavigate
    const { id } = useParams(); // Obtém o id da URL

    const setLoadingState = (isLoading) => loading(isLoading, 'formulario');
    const showMessage = (message) => alerta(message);

    useEffect(() => {
        const fetchCliente = async () => {
            console.log(id)
            if (!id) return;

            setLoadingState(true);
            try {
                const response = await ClienteService.getCliente(id);
                if (response.sucesso) {
                    const clienteData = ClienteInterface.fromApiResponse(response.data);
                    setFormValues(clienteData.toApiPayload());
                } else {
                    showMessage('Cliente não encontrado.');
                    navigate('/clientes'); // Redireciona para a página de clientes
                }
            } catch {
                showMessage('Erro ao buscar cliente');
                navigate('/clientes');
            } finally {
                setLoadingState(false);
            }
        };

        fetchCliente();
    }, [id, navigate]);

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
            showMessage(`Erro:\n${errors.join('\n')}`);
            return;
        }

        try {
            setLoadingState(true);
            const response = await ClienteService.updateCliente(id, formValues);

            if (response.sucesso) {
                showMessage('Cliente atualizado com sucesso!');
                navigate('/clientes'); // Redireciona para a lista de clientes após sucesso
            } else {
                showMessage(response.message);
            }
        } catch {
            showMessage('Erro ao atualizar cliente');
        } finally {
            setLoadingState(false);
        }
    };

    const handleClear = () => {
        navigate('/clientes'); // Redireciona para a página de clientes
    };

    const headerIcon = 'pencil'; // Ícone do header
    const headerTitle = 'Editar Cliente'; // Título do header

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
                options={ClienteInterface.getTipoClienteOptions()}
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
            footerLeftButtonText="Cancelar"
            footerLeftButtonAction={handleClear}
            footerRightButtonText="Atualizar"
            footerRightButtonAction={handleSubmit}
        />
    );
};

export default ClienteEdit;
