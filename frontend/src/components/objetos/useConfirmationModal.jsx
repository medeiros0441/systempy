import React, { useState } from 'react';
import { useCustomModal } from 'src/components/objetos/Modal';

const useConfirmationModal = () => {
    const { CustomModal, setShow } = useCustomModal();
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [onConfirm, setOnConfirm] = useState(() => () => { });

    const openModal = (title, description, onConfirmCallback) => {
        setTitle(title);
        setDescription(description);
        setOnConfirm(() => onConfirmCallback);
        setShow(true); // Abre o modal
    };

    const closeModal = () => {
        setShow(false); // Fecha o modal
    };

    const handleConfirm = () => {
        onConfirm(); // Executa a função de confirmação
        closeModal(); // Fecha o modal
    };

    const renderFooter = () => (
        <>
            <button
                type="button"
                className="btn btn-secondary btn-sm me-auto"
                onClick={closeModal}>
                Cancelar
            </button>
            <button
                type="button"
                className="btn btn-primary btn-sm"
                onClick={handleConfirm}>
                Confirmar
            </button>
        </>
    );

    const ConfirmationModalComponent = () => (
        <CustomModal
            icon="exclamation-triangle"
            title={title}
            children={<p>{description}</p>}
            footer={renderFooter()}
        />
    );

    return { openModal, ConfirmationModalComponent };
};

export default useConfirmationModal;
