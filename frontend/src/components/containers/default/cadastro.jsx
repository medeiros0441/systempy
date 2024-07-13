import React, { useState } from 'react';
import { Modal, Button, Form, FloatingLabel } from 'react-bootstrap';

function CadastroForm() {
  const [step, setStep] = useState(1);

  const voltarModal = () => {
    setStep(1);
  };

  const alterModal = () => {
    if (step === 1) {
      // Validation logic for first step (if needed)
      setStep(2);
    } else if (step === 2) {
      // Validation logic for second step (if needed)
      // Example: submitForm();
      console.log("Submitting form...");
    }
  };

  // Function to handle form submission (if needed)
  const submitForm = () => {
    // Example: Perform form submission logic here
    console.log("Form submitted!");
  };

  return (
    <Modal.Dialog className="m-0 m-sm-auto">
      <Modal.Header>
        <Modal.Title>Cadastro Empresa</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {step === 1 && (
          <Form className="form-signin container mx-auto">
            <div className="modal modal-signin position-static d-block align-items-center">
              <div className="modal-content mb-2 bg-body rounded-3 border" id="container_cadastro">
                <div className="modal-header">
                  <div className="d-flex align-items-center">
                    <i className="bi mb-1 bi-person"></i>
                    <h1 className="text-center mb-1 ms-2 fw-normal small text-dark mx-auto fs-5 text-black">Cadastro Empresa</h1>
                  </div>
                </div>
                <div className="modal-body" id="container_empresa">
                  <FloatingLabel controlId="nome_empresa" label="Nome da Empresa">
                    <Form.Control type="text" placeholder="Nome da Empresa" />
                  </FloatingLabel>
                  <FloatingLabel controlId="nro_cnpj" label="Número do CNPJ">
                    <Form.Control type="text" placeholder="Número do CNPJ" />
                    <div className="invalid-feedback">Por favor, insira um CNPJ válido.</div>
                  </FloatingLabel>
                  <FloatingLabel controlId="razao_social_empresa" label="Razão Social da Empresa">
                    <Form.Control type="text" placeholder="Razão Social da Empresa" />
                  </FloatingLabel>
                </div>
                <Modal.Footer>
                  <Button variant="secondary" onClick={voltarModal} className="me-auto d-none" id="btn_voltar">
                    Voltar
                  </Button>
                  <Button variant="primary" onClick={alterModal} id="btn_salvar">
                    Próximo
                  </Button>
                </Modal.Footer>
              </div>
            </div>
          </Form>
        )}

        {step === 2 && (
          <Form className="form-signin container mx-auto">
            <div className="modal modal-signin position-static d-block align-items-center">
              <div className="modal-content mb-2 bg-body rounded-3 border" id="container_responsavel">
                <div className="modal-body">
                  <FloatingLabel controlId="nome_responsavel" label="Nome do Responsável">
                    <Form.Control type="text" placeholder="Nome do Responsável" />
                  </FloatingLabel>
                  <FloatingLabel controlId="cargo_responsavel" label="Cargo do Responsável">
                    <Form.Control type="text" placeholder="Cargo do Responsável" />
                  </FloatingLabel>
                  <FloatingLabel controlId="email_responsavel" label="E-mail do Responsável">
                    <Form.Control type="email" placeholder="E-mail do Responsável" />
                    <div className="invalid-feedback">Por favor, insira um e-mail válido.</div>
                  </FloatingLabel>
                  <FloatingLabel controlId="telefone_responsavel" label="Telefone do Responsável">
                    <Form.Control type="text" placeholder="Telefone do Responsável" />
                  </FloatingLabel>
                  <FloatingLabel controlId="nro_cpf" label="Número do CPF">
                    <Form.Control type="text" placeholder="Número do CPF" />
                    <div className="invalid-feedback">Por favor, insira um CPF válido.</div>
                  </FloatingLabel>
                  <FloatingLabel controlId="senha" label="Senha">
                    <Form.Control type="password" placeholder="Senha" />
                    <div className="invalid-feedback" id="senha-feedback"></div>
                  </FloatingLabel>
                </div>
                <Modal.Footer>
                  <Button variant="secondary" onClick={voltarModal} className="me-auto" id="btn_voltar">
                    Voltar
                  </Button>
                  <Button variant="primary" onClick={alterModal} id="btn_salvar">
                    Finalizar
                  </Button>
                </Modal.Footer>
              </div>
            </div>
          </Form>
        )}

        {/* Final step confirmation */}
        {step === 3 && (
          <div className="modal-content mb-2 bg-body rounded-3 border" id="container_conclusao">
            <div className="modal-body d-flex flex-column align-items-center">
              <p className="font-monospace fw-bold mb-3">Cadastro concluído com sucesso.</p>
              <img src="/assets/img/undraw/undraw_welcome_cats_thqn.svg" className="img-fluid col-10" style={{ maxWidth: '300px', maxHeight: '300px' }} alt="Welcome Cats" />
            </div>
            <Modal.Footer>
              <Button variant="primary" onClick={submitForm}>
                Ir para o login
              </Button>
            </Modal.Footer>
          </div>
        )}
      </Modal.Body>
    </Modal.Dialog>
  );
}

export default CadastroForm;
