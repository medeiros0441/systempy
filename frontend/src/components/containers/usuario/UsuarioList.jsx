import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Table from 'src/components/objetos/Table';
import useUsuarioModal from './useUsuarioModal';
import useConfirmationModal from 'src/components/objetos/useConfirmationModal';
import UsuarioService from 'src/services/UsuarioService';
import UsuarioInterface from 'src/interface/UsuarioInterface';
import Alerta from 'src/utils/alerta';

const UsuarioList = () => {
    const [usuarios, setUsuarios] = useState([]);
    const navigate = useNavigate(); // Usando useNavigate para navegação

    const { openModal: openUsuarioModal, UsuarioModalComponent } = useUsuarioModal();
    const { openModal: openConfirmationModal, ConfirmationModalComponent } = useConfirmationModal();

    const fetchUsuarios = useCallback(async () => {
        try {
            const response = await UsuarioService.getUsuariosByEmpresa(); // Chama o serviço sem passar id_empresa
            if (response.sucesso) {
                const usuarios = response.data.map(usuarioData =>
                    UsuarioInterface.fromApiResponse(usuarioData)
                );
                setUsuarios(usuarios);
            } else {
                Alerta(response.message, 2);
            }
        } catch (error) {
            Alerta('Erro ao buscar usuários: ' + error, 2);
        }
    }, []);

    useEffect(() => {
        fetchUsuarios();
    }, [fetchUsuarios]);

    const handleDelete = async (id_usuario) => {
        openConfirmationModal(
            'Confirmar Exclusão',
            'Você tem certeza que deseja excluir este usuário?',
            async () => {
                try {
                    const response = await UsuarioService.deleteUsuario(id_usuario);
                    if (response.sucesso) {
                        setUsuarios(prevUsuarios => prevUsuarios.filter(usuario => usuario.id_usuario !== id_usuario));
                        Alerta(response.message);
                    } else {
                        Alerta(response.message, 2, 'id_msg');
                    }
                } catch (error) {
                    Alerta('Erro ao excluir usuário', error, 2, 'id_msg');
                }
            }
        );
    };

    const columns = ['Nome', 'Email', 'Ações'];
    const rows = usuarios.map(usuario => {
        const actions = [
            {
                name: 'Editar',
                icon: 'bi-pencil',
                type: 'primary',
                onClick: () => navigate(`/usuarios/editar/${usuario.id_usuario}`)
            },
            {
                name: 'Visualizar',
                icon: 'bi-eye',
                type: 'success',
                onClick: () => openUsuarioModal(usuario.id_usuario, true)
            }
        ];

        // Adiciona a ação de exclusão apenas se o nível do usuário for maior que 1
        if (usuario.nivel_usuario > 1) {
            actions.push({
                name: 'Excluir',
                icon: 'bi-trash',
                type: 'danger',
                onClick: () => handleDelete(usuario.id_usuario)
            });
        }

        return {
            data: [
                usuario.nome_completo,
                usuario.email
            ],
            actions
        };
    });


    const dataHeader = {
        icon: 'people',
        title: 'Lista de Usuários',
        iconBtn: 'plus',
        buttonText: 'Criar Novo Usuário',
        onClickBtn: () => navigate('/usuarios/cadastrar')
    };

    return (
        <div id='id_msg'>
            <Table
                dataHeader={dataHeader}
                columns={columns}
                rows={rows}
            />
            <UsuarioModalComponent />
            <ConfirmationModalComponent />
        </div>
    );
};

export default UsuarioList;
