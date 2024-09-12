import React, { useState } from 'react';
import { Button, Form, FloatingLabel } from 'react-bootstrap';
import img_cat from 'src/assets/img/undraw/undraw_welcome_cats_thqn.svg';
import img_email from 'src/assets/img/undraw/undraw_mail_re_duel.svg'
import alerta from 'src/utils/alerta';
import request from 'src/utils/api';
import loading from 'src/utils/loading';
import InputMask from 'react-input-mask';
import { isValidCNPJ, isValidCPF, isValidPhone, isValidEmail } from 'src/utils/validate'
import { useNavigate } from 'react-router-dom';
import { autoLogin, useAuth } from 'src/utils/auth'; // Use o hook useAuth
import { setCookie } from 'src/utils/storage';

function CadastroForm() {
  const [step, setStep] = useState(1);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nome_empresa: '',
    nro_cnpj: '',
    razao_social: '',
    descricao_empresa: '',
    nome_responsavel: '',
    cargo_responsavel: '',
    email_responsavel: '',
    telefone_responsavel: '',
    nro_cpf: '',
    senha: '',
    codigo: '',
  });

  const { setIsAuthenticated } = useAuth();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({ ...prevState, [name]: value }));
  }; const validateStep1 = () => {
    const { nome_empresa, nro_cnpj, razao_social_empresa } = formData;

    if (!nome_empresa) {
      alerta('Nome da empresa é obrigatório.', 2);
      return false;
    }

    if (!isValidCNPJ(nro_cnpj)) {
      alerta('Número de CNPJ inválido.', 2);
      return false;
    }

    if (!razao_social_empresa) {
      alerta('Razão social da empresa é obrigatória.', 2);
      return false;
    }

    return true;
  };

  const validateStep2 = () => {
    const {
      nome_responsavel,
      cargo_responsavel,
      email_responsavel,
      telefone_responsavel,
      nro_cpf,
      senha
    } = formData;

    if (!nome_responsavel) {
      alerta('Nome do responsável é obrigatório.', 2);
      return false;
    }

    if (!cargo_responsavel) {
      alerta('Cargo do responsável é obrigatório.', 2);
      return false;
    }

    if (!isValidEmail(email_responsavel)) {
      alerta('Email do responsável inválido.', 2);
      return false;
    }

    if (!isValidPhone(telefone_responsavel)) {
      alerta('Telefone do responsável inválido.', 2);
      return false;
    }

    if (!isValidCPF(nro_cpf)) {
      alerta('Número de CPF inválido.', 2);
      return false;
    }

    if (!senha) {
      alerta('Senha é obrigatória.', 2);
      return false;
    }

    return true;
  };


  const sendCode = async () => {
    const { email_responsavel, nome_responsavel } = formData;

    try {
      loading(true, "ContainerFormulario");
      const response = await request("public/code/send", "POST", { "email": email_responsavel, "nome": nome_responsavel });
      if (response.sucesso === true) {
        alerta(response.message, 1);
        return true;
      } else {
        alerta(response.message, 2);
        return false;
      }
    } catch (error) {
      alerta('Erro ao enviar o código. Por favor, tente novamente.', 2);
      return false;
    } finally {
      loading(false, "ContainerFormulario");
    }
  };

  const confirmCode = async () => {
    const { codigo } = formData;
    try {
      loading(true, "ContainerFormulario");
      const response = await request("public/code/confirm", "POST", { codigo });
      if (response.sucesso === true) {
        alerta(response.message, 1);
        return true;
      } else {
        alerta(response.message, 2);
        return false;
      }
    } catch (error) {
      alerta('Erro ao confirmar o código. Por favor, tente novamente.', 2);
      return false;
    } finally {
      loading(false, "ContainerFormulario");
    }
  };

  const register = async () => {
    const { nome_empresa, nro_cnpj, razao_social_empresa, nome_responsavel, cargo_responsavel, email_responsavel, telefone_responsavel, nro_cpf, senha } = formData;
    try {
      loading(true, "ContainerFormulario");
      const response = await request("public/register/", "POST", { nome_empresa, nro_cnpj, razao_social_empresa, nome_responsavel, cargo_responsavel, email_responsavel, telefone_responsavel, nro_cpf, senha });
      if (response.sucesso === true) {
        const autoLoginSuccess = await autoLogin(email_responsavel, senha);
        if (autoLoginSuccess) {
          setIsAuthenticated(true); // Atualiza o estado de autenticação
          setCookie('authentication', true);
        }
        return true
      } else {
        alerta(response.message, 2);
        return false
      }

    } catch (error) {
      alerta('Erro ao registrar. Por favor, tente novamente.', 2);
      return false
    } finally {
      loading(false, "ContainerFormulario");
    }
  };


  const handleBack = () => setStep((prevStep) => prevStep - 1);


  const renderStepContent = () => {
    switch (step) {
      case 1:
        return (
          <>
            <FloatingLabel controlId="nome_empresa" className="mb-2" label="Nome da Empresa">
              <Form.Control
                type="text"
                placeholder="Nome da Empresa"
                name="nome_empresa"
                value={formData.nome_empresa}
                onChange={handleInputChange}
              />
            </FloatingLabel>
            <FloatingLabel controlId="nro_cnpj" className="mb-2" label="Número do CNPJ">
              <InputMask
                mask="99.999.999/9999-99"
                value={formData.nro_cnpj}
                onChange={handleInputChange}
              >
                {() => (
                  <Form.Control
                    type="text"
                    placeholder="Número do CNPJ"
                    name="nro_cnpj"
                  />
                )}
              </InputMask>
            </FloatingLabel>
            <FloatingLabel controlId="razao_social_empresa" className="mb-2" label="Razão Social da Empresa">
              <Form.Control
                type="text"
                placeholder="Razão Social da Empresa"
                name="razao_social_empresa"
                value={formData.razao_social_empresa}
                onChange={handleInputChange}
              />
            </FloatingLabel>
          </>
        );
      case 2:
        return (
          <>
            <FloatingLabel controlId="nome_responsavel" className="mb-2" label="Nome do Responsável">
              <Form.Control
                type="text"
                placeholder="Nome do Responsável"
                name="nome_responsavel"
                value={formData.nome_responsavel}
                onChange={handleInputChange}
              />
            </FloatingLabel>
            <FloatingLabel controlId="cargo_responsavel" className="mb-2" label="Cargo do Responsável">
              <Form.Control
                type="text"
                placeholder="Cargo do Responsável"
                name="cargo_responsavel"
                value={formData.cargo_responsavel}
                onChange={handleInputChange}
              />
            </FloatingLabel>
            <FloatingLabel controlId="email_responsavel" className="mb-2" label="E-mail do Responsável">
              <Form.Control
                type="email"
                placeholder="E-mail do Responsável"
                name="email_responsavel"
                value={formData.email_responsavel}
                onChange={handleInputChange}
              />
            </FloatingLabel>
            <FloatingLabel controlId="telefone_responsavel" className="mb-2" label="Telefone do Responsável">
              <InputMask
                mask="(99) 99999-9999"
                value={formData.telefone_responsavel}
                onChange={handleInputChange}
              >
                {() => (
                  <Form.Control
                    type="text"
                    placeholder="Telefone do Responsável"
                    name="telefone_responsavel"
                  />
                )}
              </InputMask>
            </FloatingLabel>
            <FloatingLabel controlId="nro_cpf" className="mb-2" label="Número do CPF">
              <InputMask
                mask="999.999.999-99"
                value={formData.nro_cpf}
                onChange={handleInputChange}
              >
                {() => (
                  <Form.Control
                    type="text"
                    placeholder="Número do CPF"
                    name="nro_cpf"
                  />
                )}
              </InputMask>
            </FloatingLabel>
            <FloatingLabel controlId="senha" className="mb-2" label="Senha">
              <Form.Control
                type="password"
                placeholder="Senha"
                name="senha"
                value={formData.senha}
                onChange={handleInputChange}
              />
            </FloatingLabel>
          </>
        );
      case 3:
        return (
          <>
            <img src={img_email} className="img-fluid justify-content-center d-grid d-12 mx-auto" style={{ maxWidth: '300px', maxHeight: '300px' }} alt="Welcome Cats" />
            <p className="font-monospace fw-bold mb-3">Enviamos um código para seu e-mail. Precisamos que confirme o código.</p>
            <FloatingLabel controlId="codigo" className="mb-2" label="Código de Confirmação">
              <InputMask
                mask="999-999"
                value={formData.codigo}
                onChange={handleInputChange}
              >
                {(inputProps) => <Form.Control {...inputProps} placeholder="Código de Confirmação" name="codigo" />}
              </InputMask>
            </FloatingLabel>
          </>
        );
      case 4:
        return (
          <>
            <img src={img_cat} className="img-fluid justify-content-center d-grid d-12 mx-auto" style={{ maxWidth: '300px', maxHeight: '300px' }} alt="Welcome Cats" />
            <p>Cadastro concluído com sucesso!</p>
          </>
        );
      default:
        return null;
    }
  };


  const handleNext = async (e) => {
    e.preventDefault(); // Previne o comportamento padrão de envio do formulário

    try {
      if (step === 1) {
        if (validateStep1()) {
          setStep(2);
        }
      } else if (step === 2) {
        if (validateStep2()) {
          const codeSent = await sendCode();
          if (codeSent) {
            setStep(3);
          } else {
            console.error('Falha ao enviar o código.');
          }
        }
      } else if (step === 3) {
        const codeConfirmed = await confirmCode();
        if (codeConfirmed) {
          const value = await register();
          if (value === true) {
            setStep(4);
          }
        } else {
          console.error('Código inválido.');
        }
      } else if (step === 4) {
        navigate('/dashboard');
      }
    } catch (error) {
      console.error('Erro ao processar o próximo passo:');
    }
  };


  return (
    <div className="container my-5">
      <div className="card justify-content-center" id="ContainerFormulario">
        <div className="card-header">
          <h1 className="fw-bolder mt-2 mb-1 fs-6 font-monospace">
            <span className="bi bi-building me-2"></span>Cadastro Empresa
          </h1>
        </div>
        <div className="card-body">
          {renderStepContent()}
        </div>
        <div className="d-flex justify-content-between card-footer">
          {step > 1 && step !== 4 && (
            <Button variant="secondary" onClick={handleBack}>Voltar</Button>
          )}
          <Button variant="primary" type="button" onClick={handleNext}>
            {step === 4 ? "ir ao Dashboard" : "Próximo"}
          </Button>
        </div>
      </div>
    </div>
  );
}

export default CadastroForm;
