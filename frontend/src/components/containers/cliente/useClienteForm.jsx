// useClienteForm.js
import React, { useState, useEffect, useRef } from 'react';
import ClienteInterface from 'src/interface/ClienteInterface';
import ClienteService from 'src/services/ClienteService';
import alerta from 'src/utils/alerta';
import loading from 'src/utils/loading';

const useClienteForm = (id_cliente = '', isView = false) => {
    const [cliente, setCliente] = useState(new ClienteInterface({}));
    const formRef = useRef(null);

    const setLoadingState = (valor) => loading(valor, "formulario");
    const setSuccessMessage = (message) => alerta(message, 1, 'formulario');
    const setErrorMessage = (message) => alerta(message, 2, 'formulario');

    useEffect(() => {
        const fetchCliente = async () => {
            if (!id_cliente) {
                setCliente(new ClienteInterface({}));
                return;
            }
            setLoadingState(true);
            try {
                const response = await ClienteService.getCliente(id_cliente);
                if (response.sucesso) {
                    setCliente(ClienteInterface.fromApiResponse(response.data));
                } else {
                    setErrorMessage(response.message);
                }
            } catch (error) {
                setErrorMessage('Erro ao buscar cliente');
            } finally {
                setLoadingState(false);
            }
        };

        fetchCliente();
    }, [id_cliente]);

    const handleSubmit = async () => {
        setLoadingState(true);

        const payload = cliente.toApiPayload();

        try {
            const response = id_cliente
                ? await ClienteService.updateCliente(id_cliente, payload)
                : await ClienteService.createCliente(payload);

            if (response.sucesso) {
                setSuccessMessage('Cliente salvo com sucesso!');
                setCliente(new ClienteInterface({}));
            } else {
                setErrorMessage(response.message);
            }
        } catch (error) {
            setErrorMessage('Erro ao salvar cliente');
        } finally {
            setLoadingState(false);
        }
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setCliente(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const renderForm = () => {
        return isView
            ? cliente.generateLabels()
            : cliente.generateInputs({ handleChange });
    };

    const ClienteForm = () => (
        <div id="formulario" ref={formRef}>
            {renderForm()}
        </div>
    );

    return isView ? { ClienteForm } : { ClienteForm, handleSubmit };
};

export default useClienteForm;
