import React, { useEffect, useRef } from 'react';
import Cookies from 'js-cookie';
import loading from 'src/utils/loading';

const ErrorBoundary = ({ children }) => {
    const containerRef = useRef(null);

    useEffect(() => {
        if (containerRef.current) {
            // Exibe a mensagem de carregamento
            loading(true, containerRef.current);
            const timer = setTimeout(() => loading(false, containerRef.current), 3000);

            return () => clearTimeout(timer); // Limpa o timer ao desmontar
        }
    }, []);

    return (
        <ErrorBoundaryFallback onError={handleError}>
            <div ref={containerRef}  >
                {children}
            </div>
        </ErrorBoundaryFallback>
    );
};

// Função para capturar erros e salvar detalhes nos cookies
const handleError = (error, errorInfo) => {
    const errorDetails = JSON.stringify({
        error: error.toString(),
        componentStack: errorInfo.componentStack,
    });

    Cookies.set('errorTitle', 'Erro');
    Cookies.set('errorDescricao', 'Ocorreu um erro inesperado.');
    Cookies.set('errorDetails', errorDetails);
};

// Componente para exibição de fallback de erro
const ErrorDisplay = () => (
    <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="container-erro text-center">
            <h1 className="h1-erro">Erro</h1>
            <p className="p-erro">Ocorreu um erro inesperado. Você pode ser redirecionado manualmente.</p>
            <a className="btn btn-primary" href="/">Ir para página de início</a>
        </div>
    </div>
);

// Componente que captura erros e renderiza fallback
class ErrorBoundaryFallback extends React.Component {
    state = { hasError: false };

    componentDidCatch(error, errorInfo) {
        this.setState({ hasError: true });
        this.props.onError(error, errorInfo);
    }

    render() {
        return this.state.hasError ? <ErrorDisplay /> : this.props.children;
    }
}

export default ErrorBoundary;
