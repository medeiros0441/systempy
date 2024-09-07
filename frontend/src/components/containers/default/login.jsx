import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import request from 'src/utils/api';
import alerta from 'src/utils/alerta';
import loading from 'src/utils/loading';
import { openModalFunction, RecuperarSenhaModal } from './update_senha';
import { getCookie, setCookie } from 'src/utils/storage';

const LoginForm = () => {
  const [email, setEmail] = useState(getCookie('email_LembrarMe') || '');
  const [senha, setSenha] = useState(getCookie('senha_LembrarMe') || '');
  const [lembrarMe, setLembrarMe] = useState(!!getCookie('email_LembrarMe'));
  const [loadingState, setLoadingState] = useState(false);
  const navigate = useNavigate();

  // Validação de campos
  const validateForm = useCallback((email, senha) => email.trim() && senha.trim(), []);

  // Função de autenticação
  const handleLogin = useCallback(async (email, senha) => {
    if (!validateForm(email, senha)) {
      return { sucesso: false, message: 'Preencha todos os campos!' };
    }
    try {
      const response = await request('public/login/', 'POST', { email, senha });
      return response;
    } catch (error) {
      return { sucesso: false, message: 'Erro ao autenticar!' };
    }
  }, [validateForm]);

  // Submissão do formulário
  const handleSubmit = useCallback(async () => {
    if (!validateForm(email, senha)) {
      alerta('Preencha todos os campos!', 2);
      return;
    }

    loading(true, "form_login");
    setLoadingState(true);

    const response = await handleLogin(email, senha);

    if (response.sucesso) {
      setCookie('authentication', true);
      if (lembrarMe) {
        setCookie('email_LembrarMe', email);
        setCookie('senha_LembrarMe', senha);
      } else {
        setCookie('email_LembrarMe', '');
        setCookie('senha_LembrarMe', '');
      }
      navigate('/dashboard');
    } else {
      alerta(response.message, 2, 'form_login');
    }

    loading(false, "form_login");
    setLoadingState(false);
  }, [email, senha, lembrarMe, handleLogin, navigate, validateForm]);

  return (
    <>
      <form id="form_login" className="form-signin container mx-auto">
        <div className="px-sm-2 p-4 my-3 modal modal-signin position-static d-block align-items-center">
          <div className="modal-dialog m-0 m-sm-auto">
            <div className="modal-content mb-2 bg-body rounded-3 border">
              <div className="modal-header">
                <div className="d-flex align-items-center">
                  <i width="32" height="32" className="bi mb-1 bi-person"></i>
                  <h1 className="text-center mb-1 ms-2 fw-normal small text-dark mx-auto">Acessar Conta</h1>
                </div>
              </div>
              <div className="modal-body">
                <div className="form-floating mb-2">
                  <input
                    type="email"
                    className="form-control"
                    autoComplete="off"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <label htmlFor="email">E-mail</label>
                </div>

                <div className="form-floating mb-2">
                  <input
                    type="password"
                    className="form-control"
                    autoComplete="off"
                    id="senha"
                    name="senha"
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                  />
                  <label htmlFor="senha">Senha</label>
                </div>

                <div className="form-check text-start my-3 text-dark">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    value="on"
                    checked={lembrarMe}
                    onChange={(e) => setLembrarMe(e.target.checked)}
                    id="flexCheckDefault"
                    name="flexCheckDefault"
                  />
                  <label className="form-check-label" htmlFor="flexCheckDefault">
                    Lembre-me
                  </label>
                  <Link
                    type="button"
                    className="link link-secondary link-button small float-end"
                    onClick={openModalFunction}
                  >
                    Recuperar senha
                  </Link>
                </div>

                <div className="col-12 mb-4">
                  <Link tabIndex="8" className="ms-auto link-secondary small mx-auto rounded-2" to="/cadastro">
                    Cadastre-se
                  </Link>
                  <button
                    id="submit-btn"
                    className="btn btn-primary float-end me-2 btn-md"
                    type="button"
                    onClick={handleSubmit}
                    disabled={loadingState}
                  >
                    {loadingState ? 'Entrando...' : 'Entrar'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>

      <RecuperarSenhaModal />
    </>
  );
};

export default LoginForm;
