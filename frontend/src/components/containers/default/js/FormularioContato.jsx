import React, { useState } from 'react';
import request from 'src/utils/api';
import alerta from 'src/utils/alerta';
import loading from 'src/utils/loading';

const FormularioContato = () => {
  const [formulario, setFormulario] = useState({
    nome: '',
    email: '',
    telefone: '',
    mensagem: '',
  });

  const [erros, setErros] = useState({
    nome: '',
    email: '',
    telefone: '',
    mensagem: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormulario((prevFormulario) => ({
      ...prevFormulario,
      [name]: value,
    }));
  };

  const limparFormulario = () => {
    setFormulario({
      nome: '',
      email: '',
      telefone: '',
      mensagem: '',
    });
    setErros({
      nome: '',
      email: '',
      telefone: '',
      mensagem: '',
    });
  };

  const validarFormulario = () => {
    let formValido = true;
    const { nome, email, telefone, mensagem } = formulario;
    const novosErros = {
      nome: '',
      email: '',
      telefone: '',
      mensagem: '',
    };

    if (!nome.trim()) {
      novosErros.nome = 'Campo obrigatório';
      formValido = false;
    }

    if (!email.trim()) {
      novosErros.email = 'Campo obrigatório';
      formValido = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      novosErros.email = 'Email inválido';
      formValido = false;
    }

    if (!telefone.trim()) {
      novosErros.telefone = 'Campo obrigatório';
      formValido = false;
    }

    if (!mensagem.trim()) {
      novosErros.mensagem = 'Campo obrigatório';
      formValido = false;
    }

    setErros(novosErros);
    return formValido;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validarFormulario()) {
      const data = { ...formulario };
      try {
        loading(true, 'form');
        const response = await request('public/contato', 'POST', data);
        alerta(response.message, 1, 'form');
        limparFormulario();
      } catch (error) {
        alerta(error, 2, 'form');
      } finally {
        loading(false, 'form');
      }
    }
  };

  return (
    <form className="row p-sm-4 container mx-auto" onSubmit={handleSubmit} id="form">
      <div className="py-5">
        <i className="bi me-2 bi-envelope figure-img" width="25" height="25" fill="currentColor"></i>
        <label className="menu">
          <p style={{ color: 'black' }} className="text-uppercase font-monospace card-title" id="Contato">E-mail</p>
        </label>
        <hr />
        <div className="form-floating mb-3">
          <input
            name="nome"
            type="text"
            id="txtNome"
            className={`form-control ${erros.nome && 'is-invalid'}`}
            placeholder="name"
            value={formulario.nome}
            onChange={handleChange}
            tabIndex="1"
          />
          <label htmlFor="txtNome" className="form-label text-secondary">Nome</label>
          {erros.nome && <div className="invalid-feedback">{erros.nome}</div>}
        </div>
        <div className="form-floating mb-3">
          <input
            name="email"
            type="text"
            maxLength="100"
            id="txtEmail"
            className={`form-control ${erros.email && 'is-invalid'}`}
            placeholder="email"
            value={formulario.email}
            onChange={handleChange}
            tabIndex="2"
          />
          <label htmlFor="txtEmail" className="form-label text-secondary">E-mail</label>
          {erros.email && <div className="invalid-feedback">{erros.email}</div>}
        </div>
        <div className="form-floating mb-3">
          <input
            name="telefone"
            type="text"
            maxLength="14"
            id="txtTelefone"
            className={`form-control telefone-mask ${erros.telefone && 'is-invalid'}`}
            placeholder="telefone"
            value={formulario.telefone}
            onChange={handleChange}
            tabIndex="3"
          />
          <label htmlFor="txtTelefone" className="form-label text-secondary">WhatsApp</label>
          {erros.telefone && <div className="invalid-feedback">{erros.telefone}</div>}
        </div>
        <div className="form-floating mb-3">
          <textarea
            name="mensagem"
            rows="2"
            cols="20"
            maxLength="1000"
            id="txtMensagem"
            className={`form-control ${erros.mensagem && 'is-invalid'}`}
            placeholder="mensagem"
            style={{ height: '200px' }}
            value={formulario.mensagem}
            onChange={handleChange}
            tabIndex="4"
          ></textarea>
          <label htmlFor="txtMensagem" className="form-label text-secondary">Mensagem</label>
          {erros.mensagem && <div className="invalid-feedback">{erros.mensagem}</div>}
        </div>
        <input
          type="button"
          name="Btncancelar"
          value="limpar"
          onClick={limparFormulario}
          id="Btncancelar"
          className="btn btn-outline-secondary btn-sm order-2 float-end mx-2 my-1"
          tabIndex="6"
        />
        <input
          type="submit"
          name="BtnEnviar"
          value="Enviar"
          className="btn text-white btn-lg float-start order-1"
          style={{ background: 'var(--tema-blue)' }}
          tabIndex="5"
        />
      </div>
    </form>
  );
};

export default FormularioContato;
