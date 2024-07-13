import React from 'react';
import { Link } from 'react-router-dom';

const Footer = ({ isCliente }) => {
  return (
    <footer className="footer" style={{ background: 'var(--tema-blue)' }}>
      <div className="container">
        <div className="row text-center">
          <div className="col-12">
            <p className="footer-title m-1 d-inline-flex border-bottom text-white">Páginas</p>
            <ul className="list-unstyled footer-links m-0">
              <li><Link to="/" className="text-secondary text-decoration-none">Home</Link></li>
              <li><Link to="/sobre" className="text-secondary text-decoration-none">Sobre-nós</Link></li>
              {!isCliente && (
                <>
                  <li><Link to="/login" className="text-secondary text-decoration-none">Login</Link></li>
                  <li><Link to="/cadastro" className="text-secondary text-decoration-none">Cadastre-se</Link></li>
                </>
              )}
            </ul>
          </div>
          <Link className="col text-center text-decoration-none" to="/">
            <p className="Font-Gliker mb-2 text-white" style={{ fontSize: '20px' }}>
              <span className="Font-Gliker" style={{ fontSize: '30px', color: 'var(--tema-verde)' }}>{"{"}</span>
              Comércio Prime
              <span className="Font-Gliker" style={{ fontSize: '30px', color: 'var(--tema-verde)' }}>{"}"}</span>
            </p>
          </Link>
        </div>
      </div>
      <div className="col-10 col-flex-inline redound p-0 text-center mb-auto full-width mx-auto">
        <p className="m-0 p-0 bg-white rounded text-black" style={{ fontSize: '0.8rem' }}>
          Software Desenvolvido por <a className="text-decoration-none text-black" href="https://br.linkedin.com/in/samuelmedeirosbc" target="blank">@Samuel Medeiros</a>.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
