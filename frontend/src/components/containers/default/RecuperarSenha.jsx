
import React, { useState, useRef } from 'react';
import { Button, Form, FloatingLabel } from 'react-bootstrap';
import { useCustomModal } from 'src/components/objetos/Modal';
import img_etapa1 from 'src/assets/img/undraw/undraw_emails_6uqr.svg';
import img_etapa2 from 'src/assets/img/undraw/undraw_letter_re_8m03.svg';
import img_etapa3 from 'src/assets/img/undraw/undraw_Security_on_re_e491.svg';
import img_etapa4 from 'src/assets/img/undraw/undraw_world_re_768g.svg';
import request from 'src/utils/api';
import alerta from 'src/utils/alerta';
import loading from 'src/utils/loading';
import { isValidEmail } from 'src/utils/validate';
import InputMask from 'react-input-mask';

const useRecuperarSenhaModal = () => {

  const { CustomModal, setShow } = useCustomModal();
  const [step, setStep] = useState(1);
  const [emailSaved, setEmailSaved] = useState('');
  const id_container_loading = "id_container";

  const emailInputRef = useRef(null);
  const codigoInputRef = useRef(null);
  const senhaInputRef1 = useRef(null);
  const senhaInputRef2 = useRef(null);
  const modalRef = useRef(null);
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);


  const reenviarCodigo = async (email) => {
    try {
      const retorn = await request('public/code/send/password', "POST", { email });
      if (retorn.sucesso) {
        alerta("E-mail Enviado com sucesso.", 1, id_container_loading);
        setEmailSaved(email);
        return true;
      } else {
        alerta(retorn.message, 2, id_container_loading);
        return false;
      }
    } catch {
      alerta("Erro interno", 2, id_container_loading);
      return false;
    }
  };

  const validarCodigoBackend = async (codigo) => {
    try {
      const retorn = await request('public/code/confirm', "POST", { email: emailSaved, codigo });
      if (retorn.sucesso) {
        alerta("código confirmado.", 1, id_container_loading);
        return true;
      } else {
        alerta(retorn.message, 2, id_container_loading);
        return false;
      }
    } catch {
      alerta("Erro interno", 2, id_container_loading);
      return false;
    }
  };
  const updatePassword = async (new_password) => {
    if (!handleValidatePassword()) {
      return false;
    }
    try {
      const response = await request('public/password/update', 'POST', { senha: new_password });

      if (response.sucesso) {
        alerta("Senha Atualizada com sucesso.", 1, id_container_loading);
        setStep(4);
        return true;
      } else {
        alerta(response.message, 2, id_container_loading);
        return false;
      }
    } catch {
      alerta('Erro interno', 2, id_container_loading);
      return false;
    }
  };
  const handleValidaEmail = () => {
    const email = emailInputRef.current.value.trim();
    const isValid = isValidEmail(email);
    emailInputRef.current.classList.toggle('is-invalid', !isValid);
    return isValid;
  };

  const handleValidarCodigo = () => {
    const codigo = codigoInputRef.current.value.trim();
    const isValid = codigo !== '';
    codigoInputRef.current.classList.toggle('is-invalid', !isValid);
    return isValid;
  };
  const handleValidatePassword = () => {
    const senha = senhaInputRef1.current?.value || '';
    const senhaConfirmada = senhaInputRef2.current?.value || '';

    const isValidSenha =
      senha.length >= 8 &&
      /[A-Z]/.test(senha) &&  // Testa se tem ao menos uma letra maiúscula
      /[a-z]/.test(senha) &&  // Testa se tem ao menos uma letra minúscula
      /[0-9]/.test(senha);    // Testa se tem ao menos um número

    const isConfirmed = senha === senhaConfirmada;

    if (senhaInputRef1.current) {
      senhaInputRef1.current.classList.toggle('is-invalid', !isValidSenha);
    }

    if (senhaInputRef2.current) {
      senhaInputRef2.current.classList.toggle('is-invalid', !isConfirmed);
    }

    if (!isValidSenha) {
      return false;
    }

    if (!isConfirmed) {
      return false;
    }

    return true;
  };

  async function handleButtonClick() {
    setIsButtonDisabled(true);  // Desabilita o botão no início do processamento
    loading(true, id_container_loading);
    let isValido = false;

    switch (step) {
      case 1:
        isValido = handleValidaEmail();
        if (isValido) {
          const foiEnviado = await reenviarCodigo(emailInputRef.current.value.trim());
          if (foiEnviado) setStep(2);
        }
        break;
      case 2:
        isValido = handleValidarCodigo();
        if (isValido) {
          const codigoConfirmado = await validarCodigoBackend(codigoInputRef.current.value.trim());
          if (codigoConfirmado) setStep(3);
        }
        break;
      case 3:
        isValido = handleValidatePassword();
        if (isValido) {
          const foiAtualizado = await updatePassword(senhaInputRef2.current.value);
          if (foiAtualizado) setStep(4);
        }
        break;
      default:
        break;
    }

    loading(false, id_container_loading);
    setIsButtonDisabled(false);
  }

  const Etapa1 = () => (
    <div className="modal-body">
      <div className="text-center row   mb-4">
        <img src={img_etapa1} className="img-fluid" style={{ maxHeight: '150px' }} alt="Confirme seu email" />
        <h3 className="font-monospace">Confirme seu email</h3>
      </div>
      <FloatingLabel controlId="email_recuperacao" label="E-mail" className="mb-3">
        <Form.Control
          type="email"
          autoComplete="off"
          ref={emailInputRef}
        />
        <Form.Control.Feedback type="invalid">
          Por favor, insira um Email válido.
        </Form.Control.Feedback>
      </FloatingLabel>
    </div>
  );

  const Etapa2 = () => (
    <div className="modal-body">
      <div className="text-center row  mb-4">
        <img src={img_etapa2} className="img-fluid" style={{ maxHeight: '150px' }} alt="Confirme seu email com o código que foi enviado" />
        <h3 className="font-monospace">Enviamos um código para seu e-mail. Precisamos que confirme o código.</h3>
      </div>
      <FloatingLabel controlId="codigo" label="Código de Confirmação" className="mb-3">
        <InputMask mask="999-999"  >
          {(inputProps) => <Form.Control {...inputProps} ref={codigoInputRef} />}
        </InputMask>
        <Form.Control.Feedback type="invalid">
          O campo é obrigatório.
        </Form.Control.Feedback>
      </FloatingLabel>
    </div>
  );

  const Etapa3 = () => (
    <div className="modal-body">
      <div className="text-center  row   mb-4">
        <img src={img_etapa3} className="img-fluid" style={{ maxHeight: '150px' }} alt="E-mail Confirmado, Atualize a senha" />
        <h3 className="font-monospace">E-mail Confirmado, Atualize a senha</h3>
      </div>
      <FloatingLabel controlId="senha_recuperacao1" label="Senha" className="mb-3">
        <Form.Control
          type="password"
          ref={senhaInputRef1}
        />
        <Form.Control.Feedback type="invalid">
          Senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas e números.
        </Form.Control.Feedback>
      </FloatingLabel>
      <FloatingLabel controlId="senha_recuperacao2" label="Confirmar Senha" className="mb-3">
        <Form.Control
          type="password"
          ref={senhaInputRef2}
        />
        <Form.Control.Feedback type="invalid">
          As senhas não coincidem.
        </Form.Control.Feedback>
      </FloatingLabel>
    </div>
  );

  const Etapa4 = () => (
    <div className="modal-body">
      <div className="row mb-2 text-center">
        <img src={img_etapa4} className="img-fluid mx-auto" style={{ maxHeight: '150px' }} alt="Senha Alterada com sucesso." />
        <label>Senha Alterada com sucesso.</label>
      </div>
    </div>
  );
  const renderFooter = () => {
    const renderButton = (text, onClick, className = "btn btn-primary") => (
      <Button type="button" className={className} onClick={onClick} disabled={isButtonDisabled} >
        {text}
      </Button>
    );

    const renderBackAndNextButtons = (backStep) => (
      <>
        {renderButton("Voltar", () => setStep(backStep), "btn me-auto btn-sm btn-secondary")}
        {renderButton("Avançar", handleButtonClick, "btn ms-auto btn-sm btn-primary")}
      </>
    );

    switch (step) {
      case 1:
        return renderButton("Avançar", handleButtonClick);
      case 2:
        return renderBackAndNextButtons(1);
      case 3:
        return renderBackAndNextButtons(2);
      case 4:
        return renderButton("Fechar", () => modalRef.current?.closeModal(), "btn ms-auto btn-sm btn-primary");
      default:
        return null;
    }
  };
  const RenderModal = () => {
    return (
      <>
        <CustomModal
          icon="block"
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
  
  const openModal = () => {
    setShow(true);
  };
  
  return { RenderModal, openModal };
  };
  
  export default useRecuperarSenhaModal;