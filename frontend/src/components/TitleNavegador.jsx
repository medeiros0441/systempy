import React from 'react';
import { Helmet } from 'react-helmet';

const CPS = "{ CPS } ";

const Title = ({ text = null }) => {
    return (
        <>
            <Helmet>
                <title>{CPS} {text ? `+ ${text}` : ''}</title>
                <meta name="description" content={text || 'Descrição padrão'} />
            </Helmet>
        </>
    );
};

export default Title;
