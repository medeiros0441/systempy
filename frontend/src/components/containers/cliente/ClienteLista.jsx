import React, { useState, useEffect } from 'react';
import Table from 'src/components/objetos/Table'; // Componente DataTable
import useClienteModal from './useClienteModal'; // Hook para o modal de cliente
import useConfirmationModal from 'src/components/objetos/useConfirmationModal'; // Novo hook para o modal de confirmação
import ClienteService from 'src/services/ClienteService'; // Serviço para buscar clientes
import ClienteInterface from 'src/interface/ClienteInterface'
const ClienteList = () => {
    const [clientes, setClientes] = useState([]);
    const { openModal: openClienteModal, ClienteModalComponent } = useClienteModal();
    const { openModal: openConfirmationModal, ConfirmationModalComponent } = useConfirmationModal();


    // Função para buscar clientes da empresa
    const fetchClientes = async () => {
        try {
            const response = await ClienteService.getClientesByEmpresa(); // Exemplo com ID 1, ajuste conforme necessário
            if (response.sucesso) {
                // Mapear os dados para instâncias de ClienteInterface
                const clientes = response.data.map(clienteData => ClienteInterface.fromApiResponse(clienteData));
                setClientes(clientes);
            } else {
                console.error(response.message); // Tratar erros adequadamente
            }
        } catch (error) {
            console.error('Erro ao buscar clientes:', error);
        }
    };

    useEffect(() => {
        fetchClientes();
    }, []);

    const handleDelete = (id_cliente) => {
        openConfirmationModal(
            'Confirmar Exclusão',
            'Você tem certeza que deseja excluir este cliente?',
            async () => {
                try {
                    const response = await ClienteService.deleteCliente(id_cliente);
                    if (response.sucesso) {
                        setClientes(prevClientes => prevClientes.filter(cliente => cliente.id !== id_cliente));
                    } else {
                        console.error(response.message); // Tratar erros adequadamente
                    }
                } catch (error) {
                    console.error('Erro ao excluir cliente:', error);
                }
            }
        );
    };

    const columns = ['Nome', 'Telefone', 'Ações']; // Títulos das colunas da tabela

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
                onClick: () => openClienteModal(cliente.id, false) // Passa o ID do cliente e indica que não é visualização
            },
            {
                name: 'Visualizar',
                icon: 'bi-eye',
                type: 'info',
                onClick: () => openClienteModal(cliente.id, true) // Passa o ID do cliente e indica que é visualização
            },
            {
                name: 'Excluir',
                icon: 'bi-trash',
                type: 'danger',
                onClick: () => handleDelete(cliente.id) // Passa o ID do cliente para exclusão
            }
        ]
    }));

    const dataHeader = {
        icon: 'people', // Ícone para o título
        title: 'Lista de Clientes', // Título da tabela
        iconBtn: 'plus', // Ícone para o botão
        buttonText: 'Criar Novo Cliente', // Texto do botão
        onClickBtn: () => openClienteModal(null, false) // Função a ser executada no botão
    };

    return (
        <div>
            <Table
                dataHeader={dataHeader}
                columns={columns}
                rows={rows}
            />

            {/* Renderiza o modal de cliente */}
            <ClienteModalComponent />

            {/* Renderiza o modal de confirmação */}
            <ConfirmationModalComponent />
        </div>
    );
};

export default ClienteList;
