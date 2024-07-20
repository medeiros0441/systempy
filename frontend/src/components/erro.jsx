// src/components/erro.js
import React from 'react';
import { useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';

const Erro = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);

  const title = queryParams.get('title') || 'Ocorreu um erro!';
  const descricao = queryParams.get('descricao') || 'Desculpe-nos pelo inconveniente.';
  const urlRedirect = queryParams.get('urlRedirect') || '';

  return (
    <div className="container-erro container  mx-2 my-5 text-center">
      <h1 className="h1-erro">{title}</h1>
      <p className="p-erro">{descricao}</p>
      {urlRedirect && (
        <a href={urlRedirect} className="btn btn-primary">Voltar</a>
      )}
      <p>Por favor, tente novamente mais tarde ou entre em contato conosco para obter assistência.</p>
    </div>
  );
};

Erro.propTypes = {
  title: PropTypes.string,
  descricao: PropTypes.string,
  urlRedirect: PropTypes.string,
};

export default Erro;
