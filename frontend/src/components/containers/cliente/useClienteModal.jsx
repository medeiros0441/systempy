import React, { useState } from 'react';
import { useCustomModal } from 'src/components/objetos/Modal';
import useClienteForm from './useClienteForm';

const useClienteModal = () => {
    const { CustomModal, setShow } = useCustomModal();
    const [isModalVisible, setModalVisible] = useState(false);
    const [clienteId, setClienteId] = useState(null);  // Para gerenciar o ID do cliente
    const [isView, setIsView] = useState(false); // Para gerenciar o modo de visualização/edição
    const { ClienteForm, handleSubmit } = useClienteForm(clienteId, isView);

    const openModal = (id = null, view = false) => {
        setClienteId(id);        // se Definir o ID do cliente é para editar
        setIsView(view);         // se Definir true é para visualizar 
        setModalVisible(true);   // Abrir o modal
    };

    const renderFooter = () => {
        if (!isView) {
            return (
                <>
                    <button
                        type="button"
                        className="btn btn-secondary btn-sm me-auto"
                        onClick={() => setShow(false)}>
                        Cancelar
                    </button>
                    <button
                        type="button"
                        className="btn btn-primary btn-sm me-auto"
                        onClick={handleSubmit}>
                        Salvar
                    </button>
                </>
            );
        } else {
            return (
                <button
                    type="button"
                    className="btn btn-secondary btn-sm me-auto"
                    onClick={() => setShow(false)}>
                    Fechar
                </button>
            );
        }
    };

    const getModalTitle = () => {
        if (clienteId && isView) {
            return "Visualizar Cliente";
        }
        if (clienteId) {
            return "Editar Cliente";
        }
        return "Criar Cliente";
    };

    const ClienteModalComponent = () => (
        isModalVisible && (
            <CustomModal
                icon="person"
                title={getModalTitle()}
                children={ClienteForm}
                footer={renderFooter()}
            />
        )
    );

    return { openModal, ClienteModalComponent };
};

export default useClienteModal;
