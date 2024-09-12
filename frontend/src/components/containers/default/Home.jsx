// Importe as imagens necessárias
import backgroundImg from 'src/assets/img/biblioteca/pexels-mikael-blomkvist-6476590.jpg';
import {FAQSection, PricingSection,ComparisonSection} from './js/components'; 
import React from 'react';
// Componente para a seção de introdução
const Introduction = () => (
  <div className="featurette text-dark my-5 container mx-auto">
    <div className="col-md-10 mx-auto">
      <h2 className="featurette-heading lh-1">
        <span className="font-monospace fs-1 text-dark Font-Gliker fw-bold" style={{ letterSpacing: '1px', fontSize: '1rem' }} >O Poder da Simplicidade na Palma da Sua Mão</span></h2>
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
 
 
// Componente principal do aplicativo React
const Home = () => (
  <>
    <Introduction />
    <BackgroundSection />
    <PricingSection />
    <ComparisonSection />
    <FAQSection />
  </>
);

export default Home;
         
 