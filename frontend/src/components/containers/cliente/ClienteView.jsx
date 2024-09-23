import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Formulario from '@objetos/Formulario';
import useClienteForm from './useClienteForm';

const ClienteView = () => {
    const navigate = useNavigate();
    const { id } = useParams();

    const { renderForm } = useClienteForm(id, false);

    const headerIcon = 'person';
    const headerTitle = 'Visualizar Cliente';

    const handleBack = () => {
        navigate('/clientes'); // Redireciona para a lista de clientes
    };

    return (
        <Formulario
            headerIcon={headerIcon}
            headerTitle={headerTitle}
            formBody={renderForm()} // Certifique-se de que renderForm() retorna um JSX válido
            footerLeftButtonText="Voltar"
            footerLeftButtonAction={handleBack}
            footerRightButtonText="Salvar"
            footerRightButtonAction={null}
            isDark={true}
        />
    );
};

export default ClienteView;
