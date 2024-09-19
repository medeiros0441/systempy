import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie'; // Importa a biblioteca para manipular cookies
import loading from 'src/utils/loading';

const Erro = () => {
  const [title, setTitle] = useState('Ocorreu um erro!');
  const [descricao, setDescricao] = useState('Desculpe-nos pelo inconveniente.');
  const [errorDetails, setErrorDetails] = useState({});

  useEffect(() => {
    setLoadingState(true); // Ativa o loading ao montar o componente

    // Lê os valores dos cookies
    const cookieTitle = Cookies.get('errorTitle');
    const cookieDescricao = Cookies.get('errorDescricao');
    const cookieDetails = Cookies.get('errorDetails');

    if (cookieTitle) setTitle(cookieTitle);
    if (cookieDescricao) setDescricao(cookieDescricao);

    if (cookieDetails) {
      try {
        const decodedDetails = JSON.parse(cookieDetails);
        setErrorDetails(decodedDetails);
      } catch (e) {
        console.error('Erro ao decodificar os detalhes do erro:', e);
      }
    }

    // Simula o fim do carregamento após um pequeno atraso
    const timer = setTimeout(() => {
      setLoadingState(false);
    }, 1000);

    return () => clearTimeout(timer); // Limpa o timeout ao desmontar o componente
  }, []);

  const setLoadingState = (isLoading) => loading(isLoading, 'formulario');

  return (
    <div className="px-3" id="formulario">
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
