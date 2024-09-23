import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom'; // Remova o useLocation se não for usado
import Base from '@components/Base';
import RouterConfig from './routes/router';
import { AuthProvider } from '@utils/auth';
import ErrorBoundary from '@components/ErrorBoundary';

const App = () => (
  <AuthProvider>
    <Router>
      <ErrorBoundary>
        <Base>
          <RouterConfig />
        </Base>
      </ErrorBoundary>
    </Router>
  </AuthProvider>
);

export default App;
