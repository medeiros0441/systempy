import React, { useEffect, useRef } from 'react';
import { BrowserRouter as Router, useLocation } from 'react-router-dom';
import Base from './components/Base';
import RouterConfig from './routes/router';
import { AuthProvider } from './utils/auth';
import ErrorBoundary from './components/ErrorBoundary';
import loading from './utils/loading';
const App = () => (
  <AuthProvider>
    <Router>
      <ErrorBoundary>
        <LoadingWrapper>
          <Base>
            <RouterConfig />
          </Base>
        </LoadingWrapper>
      </ErrorBoundary>
    </Router>
  </AuthProvider>
);

const LoadingWrapper = ({ children }) => {
  const location = useLocation();
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      loading(true, containerRef.current);
      const timer = setTimeout(() => {
        loading(false, containerRef.current);
      }, 2000); // 2 segundos de atraso

      return () => clearTimeout(timer); // Limpa o timer ao desmontar
    }
  }, [location.pathname]);

  return (
    <div ref={containerRef}>
      {children}
    </div>
  );
};

export default App;
