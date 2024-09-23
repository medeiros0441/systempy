import React, { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import loading from '@utils/loading';

const LoadingWrapper = ({ children }) => {
    const location = useLocation();
    const containerRef = useRef(null);
    const [isMounted, setIsMounted] = useState(true); // Flag de montagem

    useEffect(() => {
        setIsMounted(true); // Marca como montado ao iniciar o efeito

        if (containerRef.current) {
            loading(true, containerRef.current);
            const timer = setTimeout(() => {
                if (isMounted) {
                    loading(false, containerRef.current); // Atualiza somente se ainda estiver montado
                }
            }, 2000); // 2 segundos de atraso

            return () => {
                clearTimeout(timer); // Limpa o timer ao desmontar
                setIsMounted(false); // Marca como desmontado
            };
        }
    }, [location.pathname, isMounted]); // Inclua isMounted aqui

    return (
        <div ref={containerRef}>
            {children}
        </div>
    );
};

export default LoadingWrapper;
