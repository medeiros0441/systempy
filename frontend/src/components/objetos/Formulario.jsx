import React from 'react';

// Componente genérico de formulário

const Formulario = ({
    headerIcon,
    headerTitle,
    formBody,
    footerLeftButtonText,
    footerLeftButtonAction,
    footerRightButtonText,
    footerRightButtonAction
}) => {
    return (
        <div className='container my-3'>
            <div className="card">
                <div className="card-header d-flex align-items-center border-bottom">
                    <i className={`bi bi-${headerIcon} fs-5 me-2`}></i>
                    <p className="fs-5 font-monospace text-dark fw-bold mb-0">
                        {headerTitle}
                    </p>
                </div>
                <form className='container card-body' id="formulario">
                    {formBody}
                </form>
                <div className="card-footer d-flex justify-content-between">
                    <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        onClick={footerLeftButtonAction}
                    >
                        {footerLeftButtonText}
                    </button>
                    <button
                        type="button"
                        className="btn btn-primary btn-sm"
                        onClick={footerRightButtonAction}
                    >
                        {footerRightButtonText}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Formulario;