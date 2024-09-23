import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Table from 'src/components/objetos/Table';
import useClienteModal from './useClienteModal';
import useConfirmationModal from 'src/components/objetos/useConfirmationModal';
import ClienteService from 'src/services/ClienteService';
import ClienteInterface from 'src/interface/ClienteInterface';
import Alerta from 'src/utils/alerta';

const ClienteList = () => {
    const [clientes, setClientes] = useState([]);
    const navigate = useNavigate(); // Usando useNavigate para navegação

    const { openModal: openClienteModal, ClienteModalComponent } = useClienteModal();
    const { openModal: openConfirmationModal, ConfirmationModalComponent } = useConfirmationModal();

    const fetchClientes = useCallback(async () => {
        try {
            const response = await ClienteService.getClientesByEmpresa();
            if (response.sucesso) {
                const clientes = response.data.map(clienteData => ClienteInterface.fromApiResponse(clienteData));
                setClientes(clientes);
            } else {
                Alerta(response.message);
            }
        } catch (error) {
            Alerta('Erro ao buscar clientes', error);
        }
    }, []);

    useEffect(() => {
        fetchClientes();
    }, [fetchClientes]);

    const handleDelete = async (id_cliente) => {
        openConfirmationModal(
            'Confirmar Exclusão',
            'Você tem certeza que deseja excluir este cliente?',
            async () => {
                try {
                    const response = await ClienteService.deleteCliente(id_cliente);
                    if (response.sucesso) {
                        setClientes(prevClientes => prevClientes.filter(cliente => cliente.id_cliente !== id_cliente));
                        Alerta(response.message);
                    } else {
                        Alerta(response.message, 2, 'id_msg');
                    }
                } catch (error) {
                    Alerta('Erro ao excluir cliente', error, 2, 'id_msg');
                }
            }
        );
    };

    const columns = ['Nome', 'Telefone', 'Ações'];

    const rows = clientes.map(cliente => ({
        data: [
            cliente.nome,
            cliente.telefone
        ],
        actions: [
            {
                name: 'Editar',
                icon: 'bi-pencil',
                type: 'primary',
                onClick: () => navigate(`/clientes/editar/${cliente.id_cliente}`)
            },
            {
                name: 'Visualizar',
                icon: 'bi-eye',
                type: 'success',
                onClick: () => openClienteModal(cliente.id_cliente, true)
            },
            {
                name: 'Excluir',
                icon: 'bi-trash',
                type: 'danger',
                onClick: () => handleDelete(cliente.id_cliente)
            }
        ]
    }));

    const dataHeader = {
        icon: 'people',
        title: 'Lista de Clientes',
        iconBtn: 'plus',
        buttonText: 'Criar Novo Cliente',
        onClickBtn: () => navigate('/clientes/cadastrar')
    };

    return (
        <div id='id_msg'>
            <Table
                dataHeader={dataHeader}
                columns={columns}
                rows={rows}
            />
            <ClienteModalComponent />
            <ConfirmationModalComponent />
        </div>
    );
};

export default ClienteList;
