import React, { useState } from 'react';
import { useCustomModal } from 'src/components/objetos/Modal';
import alerta from 'src/utils/alerta';
import useUsuarioForm from './useUsuarioForm'; // Importa o hook para o formulário de usuário

const useUsuarioModal = (id) => {
    const { CustomModal, setShow } = useCustomModal();
    const [usuarioId, setUsuarioId] = useState(null);
    const { renderForm } = useUsuarioForm(usuarioId, false); // Chama o hook aqui

    const openModal = (id_usuario = false, view = false) => {
        if (!id_usuario) {
            alerta('ID do usuário não fornecido');
            return setShow(false);
        }

        setUsuarioId(id_usuario); // Armazena o ID do usuário
        setShow(view);
    };

    const renderFooter = () => (
        <button
            type="button"
            className="btn btn-secondary btn-sm mx-auto"
            onClick={() => setShow(false)}
        >
            Fechar
        </button>
    );

    const UsuarioModalComponent = () => (
        <CustomModal
            icon="person"
            title="Visualizar Usuário"
            children={renderForm()} // Renderiza o formulário de visualização de usuário
            footer={renderFooter()} // Botão para fechar o modal
        />
    );

    return { openModal, UsuarioModalComponent };
};

export default useUsuarioModal;
