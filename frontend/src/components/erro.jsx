// src/components/erro.js
import React from 'react';
import { useLocation } from 'react-router-dom';

const Erro = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);

  const title = queryParams.get('title') || 'Ocorreu um erro!';
  const descricao = queryParams.get('descricao') || 'Desculpe-nos pelo inconveniente.';
  const details = queryParams.get('details');

  let errorDetails = {};
  if (details) {
    try {
      errorDetails = JSON.parse(decodeURIComponent(details));
    } catch (e) {
      console.error("Erro ao decodificar os detalhes do erro:", e);
    }
  }

  return (
    <div className="px-3">
      <div className="container-erro my-4 container justify-content-between align-items-center text-center mx-0 mx-sm-auto">
        <h1 className="h1-erro">{title}</h1>
        <p className="p-erro">{descricao}</p>

        {errorDetails.message && (
          <div>
            <h3>Detalhes do erro:</h3>
            <p><strong>Mensagem:</strong> {errorDetails.message}</p>
            <pre style={{ textAlign: 'left', margin: '0 auto', maxWidth: '600px' }}>
              {errorDetails.stack}
            </pre>
          </div>
        )}

        <p>Por favor, tente novamente mais tarde ou entre em contato conosco para obter assistência.</p>
      </div>
    </div>
  );
};

export default Erro;
