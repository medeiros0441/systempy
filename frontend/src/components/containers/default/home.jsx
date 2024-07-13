// Importe as imagens necessárias
import backgroundImg from 'src/assets/img/biblioteca/pexels-mikael-blomkvist-6476590.jpg';
import './css/CommentsSection.css';
import './js/CommentsSection.js';
import React from 'react';
// Componente para a seção de introdução
const Introduction = () => (
  <div className="featurette text-dark my-5 container mx-auto">
    <div className="col-md-10 mx-auto">
      <h2 className="featurette-heading lh-1"><span className="font-monospace fs-1 text-dark Font-Gliker fw-bold" style={{ letterSpacing: '1px', fontSize: '1rem' }} >O Poder da Simplicidade na Palma da Sua Mão</span></h2>
      <hr className="featurette-divider" />
      <p className="lead text-dark" style={{ fontSize: '1rem' }}>
        Comércio Prime Soluções, sua solução completa para otimizar a seu comercio varejista.
        Estamos aqui para facilitar o dia a dia do seu negócio, oferecendo ferramentas poderosas para gerenciar pedidos, controlar estoques, acompanhar vendas.
      </p>
    </div>
  </div>
);

// Componente para a seção de imagem de fundo
const BackgroundSection = () => (
  <div
    style={{
      backgroundImage: `url(${backgroundImg})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      position: 'relative',
      overflow: 'hidden',
      height: '300px',
    }}
    className="p-5 text-white text-center" >
    <div className="align-items-center" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0, 0, 0, 0.7)', backdropFilter: 'blur(1.8px)' }}>
      <div className="container text-white text-center py-5">
        <h1 className="text-white" style={{ fontSize: '1.9rem' }}>Mais do que Software, Uma Experiência de Controle</h1>
        <p className="col-lg-8 mx-auto text-white lead" style={{ fontSize: '1rem' }}>
          Sua solução completa para otimizar a gestão de seu comércio. Estamos aqui para facilitar o dia a dia do seu negócio, oferecendo ferramentas poderosas para gerenciar pedidos, controlar estoques, acompanhar vendas e muito mais.
        </p>
      </div>
    </div>
  </div>
);

// Componente para a seção de planos
const PricingSection = () => (
  <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
    <h1 className="display-4 fw-normal text-dark">Planos</h1>
    <p className="fs-5 text-dark">Suas Lojas em seu controle. A transformação que podemos trazer para a gestão do seu negócio.</p>
  </div>
);

// Componente para a seção de comparação
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
          {/* Inserir linhas da tabela aqui */}
        </tbody>
      </table>
    </div>
  </div>
);

function toggleFilter(element) {
  var isOpen = element.nextElementSibling.classList.contains('show');

  // Fecha todos os containers que estão abertos
  var openContainers = document.querySelectorAll('.card-body.show');
  openContainers.forEach(function(container) {
    container.classList.remove('show');
    container.previousElementSibling.querySelector('.bi').classList.replace('bi-chevron-up', 'bi-chevron-down');
  });

  // Abre ou fecha o container atual e altera o ícone
  var body = element.nextElementSibling;
  if (!isOpen) {
    body.classList.add('show');
    element.querySelector('.bi').classList.replace('bi-chevron-down', 'bi-chevron-up');
  } else {
    element.querySelector('.bi').classList.replace('bi-chevron-up', 'bi-chevron-down');
  }
}
// Componente para a seção de perguntas frequentes
const FAQSection = () => (
  <div className="container mx-auto my-3 border-white border">
    <div className="card bg-dark rounded pb-2 text-light">
      <span className="m-3 text-center font-monospace fs-5 border-bottom border-white">Perguntas frequentes</span>

      <div id="faq1" className="card-header bg-dark text-light border-bottom border-white d-flex align-items-center py-3 px-2 justify-content-between" onClick={() => toggleFilter('faq1')}>
        <span className="ms-1">O que é este software de gerenciamento?</span>
        <i className="bi bi-chevron-down ml-auto ms-auto"></i>
      </div>
      <div className="card-body collapse bg-dark text-light border-bottom border-white">
        Este software é uma ferramenta online feita para ajudar empresários a administrar suas lojas e negócios de médio e pequeno porte. Ele cuida de coisas como vendas, estoque e até usuários em sua empresa.
      </div>
 
    </div>
  </div>
);     
const CommentsSection = () => {
  const comments = [
    {
      id: 1,
      image: '',
      name: 'João Silva',
      date: '10 de Março, 2024',
      rating: 4,
      comment: 'Ferramenta indispensável para o nosso negócio. Altamente recomendada!'
    },
    {
      id: 2,
      image: '',
      name: 'Mariana Costa',
      date: '22 de Abril, 2024',
      rating: 3.5,
      comment: 'Plataforma fácil de usar e muito eficiente na gestão de projetos.'
    },
    {
      id: 3,
      image: '',
      name: 'Carlos Oliveira',
      date: '15 de Maio, 2024',
      rating: 5,
      comment: 'Excelente suporte ao cliente e funcionalidades robustas.'
    },
    // Adicione mais comentários conforme necessário
  ];

  return (
    <div className="person-carousel">
      <div className="container">
        <h1 className="m-3 text-center col-12 font-monospace h1 text-dark border-bottom border-dark">
          O que nossos clientes dizem
        </h1>
        <div className="inner--carousel">
          {comments.map(comment => (
            <div className="item--carousel" key={comment.id}>
              <div className="inner-item--carousel">
                <div className="image">
                  <img src={comment.image} alt="Imagem do Cliente" className="rounded img-fluid col-12 mb-2" />
                </div>
                <div className="name">
                  <h5 className="card-title" id="nome_cliente">{comment.name}</h5>
                </div>
                <div className="job">
                  <h6 className="card-subtitle mb-2 small" id="date_post">{comment.date}</h6>
                  <div className="star-rating mb-2">
                    {[...Array(Math.floor(comment.rating))].map((_, index) => (
                      <i key={index} className="bi bi-star-fill"></i>
                    ))}
                    {comment.rating % 1 !== 0 && (
                      <i className="bi bi-star-half"></i>
                    )}
                  </div>
                </div>
                <div className="info">
                  <p className="card-text" id="comenst">{comment.comment}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="indicators--carousel only-mobile">
          <div className="inner-indicators--carousel">
            {[...Array(comments.length)].map((_, index) => (
              <span key={index} className={index === 0 ? 'active' : ''}></span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
// Componente principal do aplicativo React
const Home = () => (
  <>
    <Introduction />
    <BackgroundSection />
    <PricingSection />
    <ComparisonSection />
    <FAQSection />
    <CommentsSection />
  </>
);

export default Home;
         
 