import React from 'react';

import img_samuel from 'src/assets/img/biblioteca/IMG_20200803_150117_803.jpg'
import img_comercioprime from 'src/assets/img/logo/5.png'
const Sobre = () => {
  return (
    <div className="container-fluid p-4" style={{ background: 'var(--tema-blue)', marginTop: '-9px' }}>
      <h1 className="font-monospace fs-4 fw-bold mnA offcanvas-title text-white" >Sobre a Comércio Prime Soluções</h1>
      <div className="row featurette container mx-auto p-2 text-light">
        <div className="clearfix">
          <p className="font-monospace small font-weight-light text-center" style={{ fontSize: '15px' }}>
            A Comércio Prime Soluções é uma empresa focada na inovação e excelência em gestão de comércios.
            Nosso compromisso é simplificar e aprimorar os processos comerciais por meio de soluções tecnológicas avançadas.
            Com uma equipe de profissionais dedicados, unimos tecnologia e empreendedorismo para criar ferramentas que transformam a operação das empresas.
            Combinamos anos de experiência no desenvolvimento de software com um profundo entendimento das necessidades do mercado para oferecer soluções eficazes.
            Valorizamos a transparência, confiabilidade e a satisfação do cliente, construindo relacionamentos sólidos e oferecendo suporte personalizado.
            Na Comércio Prime, somos parceiros na jornada rumo ao sucesso, proporcionando insights valiosos e suporte contínuo.
          </p>
          <div className="float-md-end mb-3 ms-md-3 ">
            <img src={img_comercioprime} className="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto object-fit-fill rounded" width="300" height="300" alt="logo" />
          </div>
          <h1 className="font-monospace fs-4 fw-bold mnA offcanvas-title" style={{ color: 'var(--white)' }}>Nossa Missão</h1>
          <p className="font-monospace small font-weight-light" style={{ fontSize: '15px' }}>
            Na Comércio Prime Soluções, nossa missão é revolucionar a gestão das distribuidoras de água por meio de soluções tecnológicas inovadoras.
            Comprometemo-nos a simplificar os processos do seu negócio, oferecendo ferramentas avançadas para um controle completo das operações.
            Buscamos proporcionar uma experiência de gestão transparente e eficiente, capacitando os empresários a atingirem novos patamares de sucesso.
          </p>
          <h1 className="font-monospace fs-4 fw-bold mnA offcanvas-title" style={{ color: 'var(--laranja)', fontSize: '20px' }}>O Que Fazemos</h1>
          <p className="font-monospace small font-weight-light" style={{ fontSize: '15px' }}>
            Na Comércio Prime Soluções, oferecemos uma plataforma completa para otimizar a gestão de distribuidoras de água.
            Por meio de nossa assinatura, proporcionamos um gerenciamento eficaz de um ou mais comércios, com recursos para controle de estoque, acompanhamento de vendas, gestão de produtos e clientes, além de análises mensais de lucro e despesas.
            Com nossa tecnologia inovadora, oferecemos uma visão abrangente dos negócios, facilitando a tomada de decisões estratégicas e impulsionando o crescimento.
          </p>
        </div>
      </div>
      <hr className="featurette-divider" />
      <div className="row featurette text-light font-monospace">
        <div className="col-sm-7 order-sm-2">
          <h1 className="lh-2 font-monospac">Samuel Medeiros</h1>
          <h2 className="featurette-heading fw-bolder lh-2 font-monospac" style={{ color: 'white', fontSize: '15px' }}>"Sou protagonista em uma história cujo Deus é o autor"</h2>
          <p className="lead" style={{ fontSize: '15px' }}>
            Samuel Medeiros, desenvolvedor em .NET e formado em Tecnologia da Informação pelo SENAC, é a mente por trás da inovadora plataforma de gestão de comércios.
            O projeto teve origem durante sua jornada na Gota Azul, uma empresa que atuava no ramo de comércio varejista de água.
            A visão empreendedora de Samuel identificou uma oportunidade única enquanto trabalhava como Gerente Local e desenvolveu o software, transformando essa visão em uma realidade comercial de sucesso.
            Para conhecer mais sobre suas conquistas e o impacto de sua visão no mercado de trabalho, siga-o nas redes sociais.
          </p>
          <div className="col-12 text-center text-white">
            <a className="text-decoration-none text-white" href="https://br.linkedin.com/in/samuelmedeirosbc" target="blank">
              <i className="bi me-2 bi-linkedin mx-auto figure-img" width="50" height="50"></i>
            </a>
            <a className="text-decoration-none text-white" href="https://www.instagram.com/osamuel.medeiros/" target="blank">
              <i className="bi me-2 bi-instagram mx-auto figure-img" width="50" height="50"></i>
            </a>
          </div>
        </div>
        <div className="col-sm-5 order-1 my-1">
          <img src={img_samuel} className="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto object-fit-fill rounded" width="300" height="300" alt="imagem" />
        </div>
      </div>
      <div className="custom-shape-divider-top-1708368195" style={{ marginTop: '-2px' }}>
        <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M985.66,92.83C906.67,72,823.78,31,743.84,14.19c-82.26-17.34-168.06-16.33-250.45.39-57.84,11.73-114,31.07-172,41.86A600.21,600.21,0,0,1,0,27.35V120H1200V95.8C1132.19,118.92,1055.71,111.31,985.66,92.83Z" className="shape-fill"></path>
        </svg>
      </div>
    </div>
  );
};

export default Sobre;
