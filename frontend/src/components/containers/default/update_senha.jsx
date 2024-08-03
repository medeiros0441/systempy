import React, { useState, useRef } from 'react';
import { Button } from 'react-bootstrap';
import CustomModal from 'src/components/objetos/modal'; // Certifique-se de ajustar o caminho se necessário
import img_etapa1 from 'src/assets/img/undraw/undraw_emails_6uqr.svg';
import img_etapa2 from 'src/assets/img/undraw/undraw_letter_re_8m03.svg';
import img_etapa3 from 'src/assets/img/undraw/undraw_Security_on_re_e491.svg';
import img_etapa4 from 'src/assets/img/undraw/undraw_world_re_768g.svg';
import request from 'src/utils/api';
import alerta from 'src/utils/alerta';
import loading from 'src/utils/loading'
let openModalFunction = () => { }; // Inicialize como função vazia

const RecuperarSenhaModal = () => {
  const [step, setStep] = useState(1);
  const [emailSaved, setEmailSaved] = useState('');
  const [senhaValida, setSenhaValida] = useState(false);
  const [senhaConfirmada, setSenhaConfirmada] = useState(false);
  const id_container_loading = "id_container";

  const emailInputRef = useRef(null);
  const codigoInputRef = useRef(null);
  const senhaInputRef1 = useRef(null);
  const senhaInputRef2 = useRef(null);
  const modalRef = useRef(null);

  const validarEmail = () => {
    const email = emailInputRef.current.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      emailInputRef.current.classList.add('is-invalid');
      return false;
    } else {
      emailInputRef.current.classList.remove('is-invalid');
      setEmailSaved(email);
      return true;
    }
  };

  const reenviarCodigo = async () => {
    try {
      loading(true, id_container_loading);
      const retorn = await request('public/code/send/', "POST", { email: emailSaved });
      if (retorn.sucess) {
        setStep(2);
      } else {
        alerta(retorn.mensag, 2, id_container_loading);
      }
    } catch {
      alerta("erro interno", 2, id_container_loading);
    } finally {
      loading(false, id_container_loading);
    }
  };

  const validarCodigoBackend = async () => {
    try {
      loading(true, id_container_loading);
      const retorn = await request('public/code/confirm', "POST", { email: emailSaved });
      if (retorn.sucess) {
        setStep(2);
      } else {
        alerta(retorn.message, 2, id_container_loading);
      }
      return retorn.sucess;
    } catch {
      alerta("erro interno", 2, id_container_loading);
      return false;

    } finally {
      loading(false, id_container_loading);
    }
  };
  const validarCodigo = () => {
    const codigo = codigoInputRef.current.value.trim();

    if (codigo === '') {
      codigoInputRef.current.classList.add('is-invalid');
      return false;
    } else {
      codigoInputRef.current.classList.remove('is-invalid');
      validarCodigoBackend(codigo);
      return true;
    }
  };

  const validarSenha = () => {
    const senha = senhaInputRef1.current.value;
    if (senha.length < 8 || !/[A-Z]/.test(senha) || !/[a-z]/.test(senha) || !/[0-9]/.test(senha)) {
      senhaInputRef1.current.classList.add('is-invalid');
      setSenhaValida(false);
    } else {
      senhaInputRef1.current.classList.remove('is-invalid');
      setSenhaValida(true);
    }
  };

  const validarSenhaConfirmacao = () => {
    const senha1 = senhaInputRef1.current.value;
    const senha2 = senhaInputRef2.current.value;

    if (senha1 !== senha2) {
      senhaInputRef2.current.classList.add('is-invalid');
      setSenhaConfirmada(false);
    } else {
      senhaInputRef2.current.classList.remove('is-invalid');
      setSenhaConfirmada(true);
    }
  };

  const finalizar = () => {
    console.log('Nova senha:', senhaInputRef2.current.value);
  };

  const Etapa1 = () => (
    <div className="modal-body">
      <div className="row mb-2 text-center">
        <img src={img_etapa1} className="image-fluid mx-auto" height="150" alt="undraw_emails" />
        <div className="fs-3 font-monospace">Confirme seu email</div>
      </div>
      <div className="form-floating mb-2">
        <input
          type="email"
          className="form-control"
          autoComplete="off"
          id="email_recuperacao"
          ref={emailInputRef}
        />
        <label htmlFor="email_recuperacao">E-mail</label>
        <div className="invalid-feedback ms-2">Por favor, insira um Email válido.</div>
      </div>

    </div>
  );

  const Etapa2 = () => (
    <div className="modal-body">
      <div className="row mb-2 text-center">
        <img src={img_etapa2} className="image-fluid mx-auto" height="150" alt="undraw_letter" />
        <div className="fs-3 font-monospace">Confirme seu email com o código que foi enviado</div>
      </div>
      <div className="input-group mb-3">
        <input
          maxLength="7"
          id="codigo_recuperacao"
          ref={codigoInputRef}
          className="form-control codigo-mask"
          type="text"
          placeholder="Confirme seu email..."
        />
        <span className="small ms-3 text-danger d-none">O campo é obrigatório</span>

      </div>
    </div>
  );

  const Etapa3 = () => (
    <div className="modal-body">
      <div className="row mb-2 text-center">
        <img src={img_etapa3} className="image-fluid mx-auto" height="150" alt="undraw_security" />
        <div className="fs-3 font-monospace">E-mail Confirmado, Atualize a senha</div>
      </div>
      <div className="form-floating mb-2">
        <input
          type="password"
          className="form-control"
          id="senha_recuperacao1"
          ref={senhaInputRef1}
          onChange={validarSenha}
        />
        <label htmlFor="senha_recuperacao1">Senha</label>
        <div className="invalid-feedback ms-2"></div>
      </div>
      <div className="form-floating mb-2">
        <input
          type="password"
          className="form-control"
          id="senha_recuperacao2"
          ref={senhaInputRef2}
          onChange={validarSenhaConfirmacao}
        />
        <label htmlFor="senha_recuperacao2">Senha Confirmar</label>
        <div className="invalid-feedback ms-2"></div>
      </div>

    </div>
  );

  const Etapa4 = () => (
    <div className="modal-body">
      <div className="row mb-2 text-center">
        <img src={img_etapa4} className="image-fluid mx-auto" height="150" alt="undraw_world" />
        <label htmlFor="senha">Senha Alterada.</label>
      </div>
    </div>
  );

  const renderFooter = () => {
    switch (step) {
      case 1:
        return (
          <Button
            type="button"
            className="btn btn-primary"
            onClick={() => {
              if (validarEmail()) {
                reenviarCodigo();
              }
            }}
          >
            Avançar
          </Button>
        );
      case 2:
        return (
          <>
            <Button
              type="button"
              className="btn me-auto btn-sm btn-secondary"
              onClick={() => setStep(1)}
            >
              Voltar
            </Button>
            <Button
              type="button"
              className="btn ms-auto btn-sm btn-primary"
              onClick={() => {
                if (validarCodigo()) {
                  setStep(3);
                }
              }}
            >
              Avançar
            </Button>
          </>
        );
      case 3:
        return (
          <>
            <Button
              type="button"
              className="btn me-auto btn-sm btn-secondary"
              onClick={() => setStep(2)}
            >
              Voltar
            </Button>
            <Button
              type="button"
              className="btn ms-auto btn-sm btn-primary"
              onClick={() => {
                if (senhaValida && senhaConfirmada) {
                  finalizar();
                  setStep(4);
                }
              }}
            >
              Avançar
            </Button>
          </>
        );
      case 4:
        return (
          <Button
            type="button"
            className="btn ms-auto btn-sm btn-primary"
            onClick={() => {
              if (modalRef.current) {
                modalRef.current.openModal();
              }
            }}
          >
            Fechar
          </Button>
        );
      default:
        return null;
    }
  };

  openModalFunction = () => {
    if (modalRef.current) {
      modalRef.current.openModal();
    }
  };

  return (
    <>
      <CustomModal
        ref={modalRef}
        title="Recuperação de Senha"
        footer={renderFooter()}
      >
        <div id={id_container_loading}>

          {step === 1 && <Etapa1 />}
          {step === 2 && <Etapa2 />}
          {step === 3 && <Etapa3 />}
          {step === 4 && <Etapa4 />}
        </div>
      </CustomModal>
    </>
  );
};

// Exporta a função de abertura do modal junto com o componente
export { RecuperarSenhaModal, openModalFunction };
