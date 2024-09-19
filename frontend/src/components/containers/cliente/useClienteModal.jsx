import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useCustomModal } from 'src/components/objetos/Modal';
import ClienteInterface from 'src/interface/ClienteInterface';
import ClienteService from 'src/services/ClienteService';
import alerta from 'src/utils/alerta';
import Label from 'src/components/objetos/Label';
import loading from 'src/utils/loading';

const useClienteModal = (id) => {
    const { CustomModal, setShow } = useCustomModal();
    const [cliente, setCliente] = useState({});
    const refForm = useRef(null);

    const setLoadingState = (valor) => {
        loading(valor, refForm.current?.id);
    };

    const fetchCliente = useCallback(async () => {
        if (!id) {
            alerta('ID do cliente não fornecido');
            setShow(false); // Fechar modal se o ID não for fornecido
            return;
        }

        try {
            setLoadingState(true);
            const response = await ClienteService.getCliente(id);
            if (response.sucesso) {
                const clienteData = ClienteInterface.fromApiResponse(response.data);
                setCliente(clienteData);
            } else {
                alerta(response.message);
                setShow(false); // Fechar modal se o cliente não for encontrado
            }
        } catch (error) {
            alerta('Erro ao buscar cliente');
            setShow(false); // Fechar modal em caso de erro
        } finally {
            setLoadingState(false);
        }
    }, [id, setShow]);

    useEffect(() => {
        if (id) {
            fetchCliente();
        }
    }, [id, fetchCliente]);

    const openModal = (view = false) => {
        setShow(view);
        if (view) {
            fetchCliente();
        }
    };

    const renderChild = () => (
        <div ref={refForm}>
            <Label htmlFor="nome" title="Nome do Cliente:" value={cliente.nome || 'N/A'} iconClass="person" />
            <Label htmlFor="telefone" title="Telefone:" value={cliente.telefone || 'N/A'} iconClass="telephone" />
            <Label htmlFor="tipo_cliente" title="Tipo de Cliente:" value={cliente.tipo_cliente || 'N/A'} iconClass="tag" />
            <Label htmlFor="descricao" title="Descrição:" value={cliente.descricao || 'N/A'} iconClass="info-circle" />
            <Label htmlFor="endereco" title="Endereço:" value={cliente.endereco || 'N/A'} iconClass="house" />
        </div>
    );

    const renderFooter = () => (
        <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => {
                setShow(false); // Fechar modal ao clicar no botão
            }}>
            Fechar
        </button>
    );

    const ClienteModalComponent = () => (
        <CustomModal
            icon="person"
            title="Visualizar Cliente"
            children={renderChild()}
            footer={renderFooter()}
        />
    );

    return { openModal, ClienteModalComponent };
};

export default useClienteModal;
