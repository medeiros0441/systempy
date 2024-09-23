import React from 'react';

// Componente genérico de formulário
const Formulario = ({
    headerIcon,
    headerTitle,
    formBody,
    footerLeftButtonText,
    footerLeftButtonAction,
    footerRightButtonText,
    footerRightButtonAction,
    isDark = false, // Atributo isDark com valor padrão false
}) => {
    return (
        <div className='container my-3'>
            <div className={`card ${isDark ? 'bg-dark' : ''}`}>
                <div className={`card-header d-flex align-items-center border-bottom ${isDark ? 'bg-dark text-white' : ''}`}>
                    <i className={`bi bi-${headerIcon} fs-5 me-2 ${isDark ? 'text-white' : 'text-dark'}`}></i>
                    <p className={`fs-5 font-monospace fw-bold mb-0 ${isDark ? 'text-white' : 'text-dark'}`}>
                        {headerTitle}
                    </p>
                </div>
                <form className={`container card-body ${isDark ? 'bg-dark text-white' : ''}`} id="formulario">
                    {formBody}
                </form>
                <div className={`card-footer d-flex justify-content-${footerRightButtonAction ? 'between' : 'center'} ${isDark ? 'bg-dark' : ''}`}>
                    <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        onClick={footerLeftButtonAction}
                    >
                        {footerLeftButtonText}
                    </button>
                    {footerRightButtonAction && (
                        <button
                            type="button"
                            className="btn btn-primary btn-sm"
                            onClick={footerRightButtonAction}
                        >
                            {footerRightButtonText}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Formulario;
