import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Formulario from '@objetos/Formulario';
import useUsuarioForm from './useUsuarioForm'; // Usa o hook para o formulário de usuário

const UsuarioView = () => {
    const navigate = useNavigate();
    const { id } = useParams(); // Pega o id do usuário a ser visualizado

    const { renderForm } = useUsuarioForm(id, false); // `false` indica que é apenas visualização

    const headerIcon = 'person';
    const headerTitle = 'Visualizar Usuário';

    const handleBack = () => {
        navigate('/usuarios'); // Redireciona para a lista de usuários
    };

    return (
        <Formulario
            headerIcon={headerIcon}
            headerTitle={headerTitle}
            formBody={renderForm()} // Certifique-se de que renderForm() retorna um JSX válido
            footerLeftButtonText="Voltar"
            footerLeftButtonAction={handleBack}
            footerRightButtonText="Salvar"
            footerRightButtonAction={null} // Não há ação de salvar neste caso, pois é apenas visualização
            isDark={true}
        />
    );
};

export default UsuarioView;
