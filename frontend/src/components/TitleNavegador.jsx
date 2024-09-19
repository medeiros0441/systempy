import React from 'react';
import { Helmet } from 'react-helmet';

const CPS = "{ CPS } ";

const Title = ({ text = null }) => {
    return (
        <Helmet>
            {/* Configuração do título da aba */}
            <title>{CPS} {text ? `+ ${text}` : ''}</title>

            {/* Meta descrição da página */}
            <meta name="description" content={text || 'Descrição padrão'} />

            {/* Link para o favicon */}
            <link rel="icon" href="/assets/img/logo/2.png" type="image/png" />

            {/* Alternativamente, para diferentes tamanhos e formatos */}
            {/* <link rel="icon" href="/favicon.png" sizes="32x32" type="image/png" /> */}
            {/* <link rel="apple-touch-icon" href="/favicon.png" sizes="180x180" /> */}
        </Helmet>
    );
};

export default Title;
