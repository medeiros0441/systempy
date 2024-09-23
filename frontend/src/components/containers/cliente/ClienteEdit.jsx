import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Formulario from '@objetos/Formulario';
import useClienteForm from './useClienteForm';

const ClienteEdit = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const { handleSubmit, renderForm } = useClienteForm(id, true); // Obtém renderBody que contém renderForm e handleSubmit

    const headerIcon = 'pencil';
    const headerTitle = 'Editar Cliente';

    return (
        <Formulario
            headerIcon={headerIcon}
            headerTitle={headerTitle}
            formBody={renderForm()} // Renderiza o formulário
            footerLeftButtonText="Cancelar"
            footerLeftButtonAction={() => navigate('/clientes')}
            footerRightButtonText="Atualizar"
            footerRightButtonAction={handleSubmit} // Ação para atualizar cliente
        />
    );
};

export default ClienteEdit;
