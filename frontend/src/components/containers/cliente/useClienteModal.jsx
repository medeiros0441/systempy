import React, { useState } from 'react';
import { useCustomModal } from 'src/components/objetos/Modal';
import alerta from 'src/utils/alerta';
import useClienteForm from './useClienteForm';

const useUsuarioModal = (id) => {
    const { CustomModal, setShow } = useCustomModal();
    const [clienteId, setClienteId] = useState(null);
    const { renderForm } = useClienteForm(clienteId, false); // Chama o hook aqui

    const openModal = (id_cliente = false, view = false) => {
        if (!id_cliente) {
            alerta('ID do cliente não fornecido');
            return setShow(false);
        }

        setClienteId(id_cliente); // Armazena o ID do cliente
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

    const ClienteModalComponent = () => (
        <CustomModal
            icon="person"
            title="Visualizar Cliente"
            children={renderForm()}
            footer={renderFooter()}
        />
    );

    return { openModal, ClienteModalComponent };
};

export default useUsuarioModal;
