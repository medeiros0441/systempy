import React, { createContext, useState, useEffect, useContext } from 'react';
import request from './api';
import { getCookie, setCookie } from './storage';


export const autoLogin = async (email, senha) => {
  try {
    const response = await request('public/login/', 'POST', { email, senha });
    return response.sucesso;
  } catch (error) {
    console.error('Erro ao autenticar:', error);
    return false;
  }
};
// Cria o contexto
const AuthContext = createContext();

// Provedor do contexto de autenticação
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => getCookie('authentication'));

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await request('public/check-auth/');
        const authenticated = response.sucesso && response.authenticated;
        setCookie('authentication', authenticated);
        setIsAuthenticated(authenticated);

        if (!authenticated) {
          const storedEmail = getCookie('email_LembrarMe');
          const storedSenha = getCookie('senha_LembrarMe');

          if (storedEmail && storedSenha) {
            const autoLoginSuccess = await autoLogin(storedEmail, storedSenha);
            setCookie('authentication', autoLoginSuccess);
            setIsAuthenticated(autoLoginSuccess);
          }
        }
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        setCookie('authentication', false);
        setIsAuthenticated(false);
      }
    };

    checkAuthentication();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook para usar o contexto de autenticação
export const useAuth = () => useContext(AuthContext);
