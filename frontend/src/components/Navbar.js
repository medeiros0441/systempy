import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ isCliente }) => {
  const toggleMenu = () => {
    var menu = document.getElementById('navbarNav');
    var icon = document.getElementById('menuIcon');
    if (menu.classList.contains('d-none')) {
      menu.classList.remove('d-none');
      icon.classList.remove('bi-box-arrow-down');
      icon.classList.add('bi-box-arrow-in-up');
    } else {
      menu.classList.add('d-none');
      icon.classList.remove('bi-box-arrow-in-up');
      icon.classList.add('bi-box-arrow-down');
    }
  };

  return (
    <nav className="navbar-expand-md navbar-dark p-2" style={{ background: 'var(--tema-blue)' }}>
      <div className="p-0 m-0 mx-auto container-xl row">
        <div className="p-0 m-0 col-12 container justify-content-between row align-items-center">
          <Link className="col text-sm-center text-start text-decoration-none" to="/">
            <p className="Font-Gliker mb-2 text-white" style={{ fontSize: '20px' }}>
              <span className="Font-Gliker" style={{ fontSize: '30px', color: 'var(--tema-verde)' }}>{"{"}</span>
              Comércio Prime
              <span className="Font-Gliker" style={{ fontSize: '30px', color: 'var(--tema-verde)' }}>{"}"}</span>
            </p>
          </Link>
          <button className="btn text-white col-auto d-inline-flex ms-auto d-sm-none" type="button" onClick={toggleMenu}>
            <span className="bi bi-box-arrow-in-up" id="menuIcon" style={{ fontSize: '20px' }}></span>
          </button>
        </div>
        <div className="col-12 d-sm-block" id="navbarNav">
          <ul className="text-center text-white my-2 row mx-auto mx-sm-0 col-auto container-xl font-monospace text-center text-sm-end justify-content-center align-items-center">
            {!isCliente && (
              <>
                <li className="text-sm-end text-center d-inline-flex col-auto">
                  <Link className="nav-link text-decoration-underline" to="/">Início</Link>
                </li>
                <li className="text-center d-inline-flex col-auto">
                  <Link className="nav-link text-decoration-underline" to="/sobre">Sobre nós</Link>
                </li>
                <li className="text-center d-inline-flex col-auto">
                  <Link className="nav-link text-white nav-link-icon login-btn px-0" to="/login">
                    <span className="login-icon">
                      <i className="bi bi-person"></i>
                    </span>
                    <span className="text-decoration-underline">Login</span>
                  </Link>
                </li>
              </>
            )}
            {isCliente && (
              <>
                {/* Renderizar itens do menu para cliente */}
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
