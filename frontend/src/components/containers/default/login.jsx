import React, { useState, useEffect } from 'react';
import { manageLoading } from 'src/utils/loading';
import { alertCustomer } from 'src/utils/alerta';
import RecuperarSenhaModal from './modal_recuperar_senha';
import { Modal } from 'bootstrap';  // Importação do modal do Bootstrap

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [lembrarMe, setLembrarMe] = useState(false);

  const isValidEmail = (email) => {
    return /\S+@\S+\.\S+/.test(email);
  };

  const validateForm = () => {
    let status = true;

    if (!isValidEmail(email)) {
      alert("Email inválido.");
      status = false;
    }

    return status;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      const data = {
        email: email,
        senha: senha,
        flexCheckDefault: lembrarMe ? "on" : "off"
      };
      setLogin(data);
    }
  };

  useEffect(() => {
    const elemento = document.getElementById('btn-login-nav');
    if (elemento) {
      elemento.style.display = 'none';
    }

    const myModal = new Modal(RecuperarSenhaModal);
  }, []);

  const setLogin = (data) => {
    manageLoading(true, "form_login");

    // Substitua chamarFuncaoPython pela chamada adequada à sua API em React
    // Exemplo: axios.post('/api_login', data).then(response => { ... }).catch(error => { ... });
    // Simulação:
    setTimeout(() => {
      const response = {
        success: true,
        redirect_url: '/dashboard' // URL para redirecionamento em caso de sucesso
      };
      if (response.success === true) {
        window.location.href = response.redirect_url;
      } else {
        alertCustomer(response.message, 2);
      }
      manageLoading(false, "form_login");
    }, 1000); // Simulação de chamada assíncrona, remova isso no seu código real
  };

  return (
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
                  id="email"
                  name="email"
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
                <button
                  type="button"
                  className="link link-secondary small float-end"
                  data-bs-toggle="modal"
                  data-bs-target="#ModalRecuperarSenha"
                >
                  Recuperar senha
                </button>
              </div>

              <div className="col-12 mb-4">
                <a tabIndex="8" className="ms-auto link-secondary small mx-auto rounded-2" href="/cadastro">
                  Cadastre-se
                </a>
                <button
                  id="submit-btn"
                  className="btn btn-primary float-end me-2 btn-md"
                  type="button"
                  onClick={handleSubmit}
                >
                  Entrar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  );
};

export default LoginForm;
