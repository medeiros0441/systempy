import React, { useState, useEffect, useCallback } from 'react';
import Input from 'src/components/objetos/Input';
import Select from 'src/components/objetos/Select';
import Label from 'src/components/objetos/Label';
import ClienteService from 'src/services/ClienteService';
import ClienteInterface from 'src/interface/ClienteInterface';
import alerta from 'src/utils/alerta';

const useClienteForm = (id, isEditable) => {
    const [formValues, setFormValues] = useState({
        nome: '',
        telefone: '',
        tipo_cliente: '',
        descricao: '',
        endereco: '',
    });
    const [cliente, setCliente] = useState({});

    const showMessage = (message) => alerta(message);


    const fetchCliente = useCallback(async () => {
        if (!id) {
            showMessage('ID do cliente não fornecido');
            return;
        }

        try {
            const response = await ClienteService.getCliente(id);
            if (response.sucesso) {
                const clienteData = ClienteInterface.fromApiResponse(response.data);
                setFormValues(clienteData);
                setCliente(clienteData);
            } else {
                showMessage(response.message);
            }
        } catch {
            showMessage('Erro ao buscar cliente');
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            fetchCliente();
        }
    }, [id, fetchCliente]);

    const handleChange = (event) => {
        const { name, value } = event.target;
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
            const response = await ClienteService.updateCliente(id, formValues);
            if (response.sucesso) {
                showMessage('Cliente atualizado com sucesso!');
            } else {
                showMessage(response.message);
            }
        } catch {
            showMessage('Erro ao atualizar cliente');
        }
    };

    const renderForm = () => (
        <div >
            <Input id="nome" name="nome" value={formValues.nome} label="Nome do Cliente" onChange={handleChange} />
            <Input id="telefone" name="telefone" value={formValues.telefone} label="Telefone" onChange={handleChange} type="tel" />
            <Select
                id="tipo_cliente"
                name="tipo_cliente"
                value={formValues.tipo_cliente}
                label="Tipo de Cliente"
                options={[
                    { value: 'Pessoa Física', label: 'Pessoa Física' },
                    { value: 'Pessoa Jurídica', label: 'Pessoa Jurídica' },
                ]}
                onChange={handleChange}
            />
            <Input id="descricao" name="descricao" value={formValues.descricao} label="Descrição" onChange={handleChange} />
        </div>
    );

    const renderLabels = () => (
        <div >
            <Label htmlFor="nome" title="Nome do Cliente:" value={cliente.nome || ''} iconClass="person" />
            <Label htmlFor="telefone" title="Telefone:" value={cliente.telefone || ''} iconClass="telephone" />
            <Label htmlFor="tipo_cliente" title="Tipo de Cliente:" value={cliente.tipo_cliente || ''} iconClass="tag" />
            <Label htmlFor="descricao" title="Descrição:" value={cliente.descricao || ''} iconClass="info-circle" />
            <Label htmlFor="endereco" title="Endereço:" value={cliente.endereco || ''} iconClass="house" />
        </div>
    );

    return isEditable ? { handleSubmit, renderForm } : { renderForm: renderLabels };
};

export default useClienteForm;
