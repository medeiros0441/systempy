import React from 'react';
import { useNavigate } from 'react-router-dom';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, errorDetails: {} };
    }

    static getDerivedStateFromError(error) {
        // Atualiza o estado para indicar que ocorreu um erro
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // Captura o erro e as informações adicionais
        console.error("Erro capturado no ErrorBoundary:", error, errorInfo);

        // Atualiza o estado com os detalhes do erro
        this.setState({
            errorDetails: {
                message: error.toString(),
                componentStack: errorInfo.componentStack,
            }
        });
    }

    render() {
        if (this.state.hasError) {
            const { message, componentStack } = this.state.errorDetails;
            const errorInfoEncoded = encodeURIComponent(JSON.stringify({
                message,
                stack: componentStack,
            }));

            return (
                <RedirectOnError
                    to={`/erro-interno?title=Erro Interno&descricao=Ocorreu um erro inesperado.&details=${errorInfoEncoded}`}
                />
            );
        }

        return this.props.children;
    }
}

const RedirectOnError = ({ to }) => {
    const navigate = useNavigate();

    React.useEffect(() => {
        // Redireciona para a página de erro
        navigate(to);
    }, [navigate, to]);

    return null;
};

export default ErrorBoundary;
