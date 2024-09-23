import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Formulario from '@objetos/Formulario';
import useUsuarioForm from './useUsuarioForm';

const UsuarioEdit = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const { handleSubmit, renderForm } = useUsuarioForm(id, true); // Obtém renderForm e handleSubmit

    const headerIcon = 'pencil';
    const headerTitle = 'Editar Usuário';

    return (
        <Formulario
            headerIcon={headerIcon}
            headerTitle={headerTitle}
            formBody={renderForm()} // Renderiza o formulário de edição de usuário
            footerLeftButtonText="Cancelar"
            footerLeftButtonAction={() => navigate('/usuarios')} // Redireciona para a lista de usuários ao cancelar
            footerRightButtonText="Atualizar"
            footerRightButtonAction={handleSubmit} // Ação para atualizar o usuário
        />
    );
};

export default UsuarioEdit;
