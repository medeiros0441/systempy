import React from 'react';

const FAQSection = () => {
  const toggleFilter = (event) => {
    const header = event.currentTarget;
    if (!header) return;

    const body = header.nextElementSibling;
    if (!body) return;

    const isOpen = body.classList.contains('show');

    // Fecha todos os containers que estão abertos
    const openContainers = document.querySelectorAll('.card-body.show');
    openContainers.forEach(container => {
      container.classList.remove('show');
      const icon = container.previousElementSibling.querySelector('.bi');
      if (icon) {
        icon.classList.replace('bi-chevron-up', 'bi-chevron-down');
      }
    });

    // Abre ou fecha o container atual e altera o ícone
    if (!isOpen) {
      body.classList.add('show');
      const icon = header.querySelector('.bi');
      if (icon) {
        icon.classList.replace('bi-chevron-down', 'bi-chevron-up');
      }
    } else {
      const icon = header.querySelector('.bi');
      if (icon) {
        icon.classList.replace('bi-chevron-up', 'bi-chevron-down');
      }
    }
  };

  return (
    <div className="container mx-auto my-3 border-white border">
      <div className="card bg-dark rounded pb-2 text-light">
        <span className="m-3 text-center font-monospace fs-5 border-bottom border-white">Perguntas frequentes</span>

        <div id="faq1" className="card-header bg-dark text-light border-bottom border-white d-flex align-items-center py-3 px-2 justify-content-between" onClick={toggleFilter}>
          <span className="ms-1">O que é este software de gerenciamento?</span>
          <i className="bi bi-chevron-down ml-auto ms-auto"></i>
        </div>
        <div className="card-body collapse bg-dark text-light border-bottom border-white">
          Este software é uma ferramenta online feita para ajudar empresários a administrar suas lojas e negócios de médio e pequeno porte. Ele cuida de coisas como vendas, estoque e até usuários em sua empresa.
        </div>

        <div id="faq2" className="card-header bg-dark text-light border-bottom border-white d-flex align-items-center py-3 px-2 justify-content-between" onClick={toggleFilter}>
          <span className="ms-1">Quais são as coisas mais importantes que este software faz?</span>
          <i className="bi bi-chevron-down ml-auto ms-auto"></i>
        </div>
        <div className="card-body collapse bg-dark text-light border-bottom border-white">
          Ele gerencia suas vendas, controle de estoque, faturamento, e até permite que você crie relatórios detalhados para acompanhar o desempenho.
        </div>

        <div id="faq3" className="card-header bg-dark text-light border-bottom border-white d-flex align-items-center py-3 px-2 justify-content-between" onClick={toggleFilter}>
          <span className="ms-1">Como posso obter este software?</span>
          <i className="bi bi-chevron-down ml-auto ms-auto"></i>
        </div>
        <div className="card-body collapse bg-dark text-light border-bottom border-white">
          Você pode ter este software assinando um plano mensal. Escolha o plano que melhor atenda às necessidades da sua empresa.
        </div>

        <div id="faq4" className="card-header bg-dark text-light border-bottom border-white d-flex align-items-center py-3 px-2 justify-content-between" onClick={toggleFilter}>
          <span className="ms-1">Posso cancelar minha assinatura deste software?</span>
          <i className="bi bi-chevron-down ml-auto ms-auto"></i>
        </div>
        <div className="card-body collapse bg-dark text-light border-bottom border-white">
          Sim, você pode cancelar sua assinatura a qualquer momento através do painel de controle. Você não será cobrado após o cancelamento, pois o sistema é pré-pago.
        </div>

        <div id="faq5" className="card-header bg-dark text-light d-flex py-3 px-2 justify-content-between" onClick={toggleFilter}>
          <span className="ms-1">Este software é seguro?</span>
          <i className="bi bi-chevron-down ml-auto ms-auto"></i>
        </div>
        <div className="card-body collapse bg-dark text-light border-bottom border-top border-white">
          Sim, este software é muito seguro. Ele usa tecnologias avançadas para manter seus dados protegidos contra qualquer acesso não autorizado.
        </div>
      </div>
    </div>
  );
};

 

const link_whatsapp = "https://api.whatsapp.com/send?phone=+5511971486656&amp;text=Ol%C3%A1%20gostaria%20de%20saber%20mais%20sobre%20os%20servi%C3%A7os%20da%20empresa%20Com%C3%A9rcio%20Prime";

const PricingSection = () => (
  <>
    <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
      <h1 className="display-4 fw-normal text-dark">Planos</h1>
      <p className="fs-5 text-dark">Suas Lojas em seu controle. A transformação que podemos trazer para a gestão do seu negócio.</p>
    </div>
    <div className="container-xl container-lg mx-auto row row-cols-1 row-cols-md-3 mb-3 text-center">
      <div className="col px-1">
        <div className="card mb-4 rounded-3 shadow-sm">
          <div className="card-header py-3">
            <h4 className="my-0 fw-normal">Plano Essencial</h4>
          </div>
          <div className="card-body">
            <h1 className="card-title pricing-card-title">R$ 79<small className="text-body-secondary fw-light">/mês</small></h1>
            <ul className="list-unstyled mt-3 mb-4">
              <li>Até 2 usuários</li>
              <li>Suporte online</li>
              <li>Até uma loja</li>
            </ul>
            <a href={link_whatsapp} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.8rem' }} className="w-100 btn btn-lg btn-outline-primary">Fale com um consultor.</a>
          </div>
        </div>
      </div>
      <div className="col px-1">
        <div className="card mb-4 rounded-3 shadow-sm">
          <div className="card-header py-3">
            <h4 className="my-0 fw-normal">Plano Intermediário</h4>
          </div>
          <div className="card-body">
            <h1 className="card-title pricing-card-title">R$ 119<small className="text-body-secondary fw-light">/mês</small></h1>
            <ul className="list-unstyled mt-3 mb-4">
              <li>Relatório personalizado</li>
              <li>Até 5 Usuários</li>
              <li>Até 2 Lojas</li>
            </ul>
            <a href={link_whatsapp} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.8rem' }} className="w-100 btn btn-lg btn-primary">Fale com um consultor</a>
          </div>
        </div>
      </div>
      <div className="col px-1">
        <div className="card mb-4 rounded-3 shadow-sm border-primary">
          <div className="card-header py-3 text-bg-primary border-primary">
            <h4 className="my-0 fw-normal">Plano Premium</h4>
          </div>
          <div className="card-body">
            <h1 className="card-title pricing-card-title">R$ 299<small className="text-body-secondary fw-light">/mês</small></h1>
            <ul className="list-unstyled mt-3 mb-4">
              <li>Até 10 ou mais Usuários</li>
              <li>Até 3 Lojas</li>
              <li>Software personalizado</li>
            </ul>
            <a href={link_whatsapp} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.8rem' }} className="w-100 btn btn-lg btn-primary">Fale com um consultor</a>
          </div>
        </div>
      </div>
    </div>
  </>
);

const ComparisonSection = () => (
  <div className="rounded-3 col-11 col-sm-12 bg-white container mx-auto">
    <h2 className="display-5 text-center pt-3 font-monospace fw-bolder" style={{ fontSize: '1.2rem' }}>Comparativo</h2>
    <div className="table-responsive rounded-3">
      <table className="table text-center">
        <thead>
          <tr>
            <th style={{ width: '34%' }}></th>
            <th style={{ width: '22%' }}>Essencial</th>
            <th style={{ width: '22%' }}>Intermediário</th>
            <th style={{ width: '22%' }}>Premium</th>
          </tr>
        </thead>
        <tbody>
          <tr >
            <th scope="row" className="col-6 text-start">Gestão de usuários</th>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
          <tr>
            <th scope="row" className="text-start">Gestão de Lojas</th>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
          <tr>
            <th scope="row" className="text-start">Gestão de produtos</th>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
          <tr>
            <th scope="row" className="text-start">Gestão de clientes</th>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
          <tr>
            <th scope="row" className="text-start">Suporte técnico prioritário</th>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
          <tr>
            <th scope="row" className="text-start">Treinamento personalizado</th>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
          <tr>
            <th scope="row" className="text-start">Relatório personalizado</th>
            <td></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
          <tr>
            <th scope="row" className="text-start">Customização personalizada</th>
            <td></td>
            <td></td>
            <td><i width="24" height="24" className="bi bi-check"></i></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
);

export { PricingSection, ComparisonSection,FAQSection };