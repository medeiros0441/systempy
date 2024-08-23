import React, { useState } from 'react';
import { Button, Form, FloatingLabel } from 'react-bootstrap';
import img_cat from 'src/assets/img/undraw/undraw_welcome_cats_thqn.svg';
import img_email from 'src/assets/img/undraw/undraw_mail_re_duel.svg'
import alerta from 'src/utils/alerta';
import request from 'src/utils/api';
import loading from 'src/utils/loading';
import InputMask from 'react-input-mask';

import { useNavigate } from 'react-router-dom'; // Para redirecionar
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({ ...prevState, [name]: value }));
  };

  const validateStep1 = () => {
    const { nome_empresa, nro_cnpj, razao_social_empresa } = formData;
    return nome_empresa && nro_cnpj && razao_social_empresa;
  };

  const validateStep2 = () => {
    const { nome_responsavel, cargo_responsavel, email_responsavel, telefone_responsavel, nro_cpf, senha } = formData;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return (
      nome_responsavel &&
      cargo_responsavel &&
      emailRegex.test(email_responsavel) &&
      telefone_responsavel &&
      nro_cpf &&
      senha
    );
  };


  const sendCode = async () => {
    const { email_responsavel, nome_responsavel } = formData;

    try {
      loading(true, "ContainerFormulario");
      const response = await request("public/code/send", "POST", { "email": email_responsavel, "nome": nome_responsavel });
      if (response.success) {
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
      if (response.success) {
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
      if (response.success) {
        alerta(response.message, 1);
      } else {
        alerta(response.message, 2);
      }
    } catch (error) {
      alerta('Erro ao registrar. Por favor, tente novamente.', 2);
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
              <Form.Control
                type="text"
                placeholder="Número do CNPJ"
                name="nro_cnpj"
                value={formData.nro_cnpj}
                onChange={handleInputChange}
              />
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
              <Form.Control
                type="text"
                placeholder="Telefone do Responsável"
                name="telefone_responsavel"
                value={formData.telefone_responsavel}
                onChange={handleInputChange}
              />
            </FloatingLabel>
            <FloatingLabel controlId="nro_cpf" className="mb-2" label="Número do CPF">
              <Form.Control
                type="text"
                placeholder="Número do CPF"
                name="nro_cpf"
                value={formData.nro_cpf}
                onChange={handleInputChange}
              />
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
            <p>Cadastro concluído com sucesso!</p>;
          </>
        );
      default:
        return null;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault(); // Previne o comportamento padrão de envio do formulário
    if (step === 4) {
      // Redireciona para a página de login no último passo
      navigate('/login');
    } else {
      // Lógica para enviar o formulário ou concluir o cadastro
      console.log('Dados do formulário:', formData);
      // Adicione aqui a lógica para enviar os dados via API, etc.
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
          await register();
          setStep(4);
        } else {
          console.error('Código inválido.');
        }
      } else if (step === 4) {
        navigate('/login');
      }
    } catch (error) {
      console.error('Erro ao processar o próximo passo:', error);
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
          {step > 1 && (
            <Button variant="secondary" onClick={handleBack}>Voltar</Button>
          )}
          <Button variant="primary" type="button" onClick={handleNext}>
            {step === 4 ? 'Finalizar' : 'Próximo'}
          </Button>
        </div>
      </div>
    </div>
  );
}

export default CadastroForm;
