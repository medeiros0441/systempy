import React, { useState } from 'react';
import { Modal, Button, Form, FloatingLabel } from 'react-bootstrap';
import img_cat from 'src/assets/img/undraw/undraw_welcome_cats_thqn.svg';

function CadastroForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    nome_empresa: '',
    nro_cnpj: '',
    razao_social_empresa: '',
    nome_responsavel: '',
    cargo_responsavel: '',
    email_responsavel: '',
    telefone_responsavel: '',
    nro_cpf: '',
    senha: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const validarStep1 = () => {
    // Validação do Step 1
    const { nome_empresa, nro_cnpj, razao_social_empresa } = formData;
    return nome_empresa && nro_cnpj && razao_social_empresa;
  };

  const validarStep2 = () => {
    // Validação do Step 2
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

  const alterarModal = () => {
    if (step === 1) {
      if (validarStep1()) {
        setStep(2);
      } else {
        alert('Por favor, preencha todos os campos obrigatórios.');
      }
    } else if (step === 2) {
      if (validarStep2()) {
        setStep(3);
      } else {
        alert('Por favor, preencha todos os campos obrigatórios e verifique a validade dos dados.');
      }
    }
  };

  const voltarModal = () => {
    setStep(step - 1);
  };

  const submitForm = () => {
    // Enviar dados do formulário
    console.log('Dados do formulário:', formData);
    // Aqui você pode enviar os dados para o backend ou realizar outras ações.
  };

  return (
    <>
      <Modal
        show={true}
        className="modal modal-signin position-static d-block align-items-center">
        <Modal.Header>
          <Modal.Title>Cadastro Empresa</Modal.Title>
        </Modal.Header>
        <Modal.Body className="modal-body">
          {step === 1 && (
            <div id="container_empresa">
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
                <div className="invalid-feedback">Por favor, insira um CNPJ válido.</div>
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
              <Modal.Footer>
                <Button variant="secondary" onClick={voltarModal} className="me-auto d-none" id="btn_voltar">
                  Voltar
                </Button>
                <Button variant="primary" onClick={alterarModal} id="btn_salvar">
                  Próximo
                </Button>
              </Modal.Footer>
            </div>
          )}

          {step === 2 && (
            <div id="container_responsavel">
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
                <div className="invalid-feedback">Por favor, insira um e-mail válido.</div>
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
                <div className="invalid-feedback">Por favor, insira um CPF válido.</div>
              </FloatingLabel>
              <FloatingLabel controlId="senha" className="mb-2" label="Senha">
                <Form.Control
                  type="password"
                  placeholder="Senha"
                  name="senha"
                  value={formData.senha}
                  onChange={handleInputChange}
                />
                <div className="invalid-feedback" id="senha-feedback"></div>
              </FloatingLabel>
              <Modal.Footer>
                <Button variant="secondary" onClick={voltarModal} className="me-auto" id="btn_voltar">
                  Voltar
                </Button>
                <Button variant="primary" onClick={alterarModal} id="btn_salvar">
                  Finalizar
                </Button>
              </Modal.Footer>
            </div>
          )}

          {step === 3 && (
            <div className="modal-content mb-2 bg-body rounded-3 border" id="container_conclusao">
              <div className="modal-body d-flex flex-column align-items-center">
                <p className="font-monospace fw-bold mb-3">Cadastro concluído com sucesso.</p>
                <img src={img_cat} className="img-fluid col-10" style={{ maxWidth: '300px', maxHeight: '300px' }} alt="Welcome Cats" />
              </div>
              <Modal.Footer>
                <Button variant="primary" onClick={submitForm}>
                  Ir para o login
                </Button>
              </Modal.Footer>
            </div>
          )}
        </Modal.Body>
      </Modal>
    </>
  );
}

export default CadastroForm;
