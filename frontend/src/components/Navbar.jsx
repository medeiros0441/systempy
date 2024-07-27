import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuthentication } from '../utils/auth';
import Cookies from 'js-cookie';

const Navbar = () => {
  const isCliente = useAuthentication();
  const session = {
    isCliente: true,
    configs_ativos: {
      1: true,
      3: true,
      5: true,
      6: true,
      7: true,
      8: true,
      12: true
    }
  };

  useEffect(() => {
    const menuState = Cookies.get('menuState');
    const menu = document.getElementById('navbarNav');
    const icon = document.getElementById('menuIcon');
    if (menuState === 'visible') {
      menu.classList.remove('d-none');
      icon.classList.remove('bi-box-arrow-down');
      icon.classList.add('bi-box-arrow-in-up');
    } else {
      menu.classList.add('d-none');
      icon.classList.remove('bi-box-arrow-in-up');
      icon.classList.add('bi-box-arrow-down');
    }
  }, []);

  const toggleMenu = () => {
    const menu = document.getElementById('navbarNav');
    const icon = document.getElementById('menuIcon');
    if (menu.classList.contains('d-none')) {
      menu.classList.remove('d-none');
      icon.classList.remove('bi-box-arrow-down');
      icon.classList.add('bi-box-arrow-in-up');
      Cookies.set('menuState', 'visible');
    } else {
      menu.classList.add('d-none');
      icon.classList.remove('bi-box-arrow-in-up');
      icon.classList.add('bi-box-arrow-down');
      Cookies.set('menuState', 'hidden');
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
        <div className="col-12 d-sm-block d-none" id="navbarNav">
          <ul className="text-decoration-none text-center text-white my-2 row mx-auto mx-sm-0 col-auto container-xl font-monospace text-center text-sm-end justify-content-center align-items-center">
            {!isCliente && (
              <>
                <li className="text-sm-end text-decoration-none text-center d-inline-flex col-auto">
                  <Link className="nav-link text-decoration-underline" to="/">
                    <i className="bi bi-house"></i> Início
                  </Link>
                </li>
                <li className="text-center text-decoration-none d-inline-flex col-auto">
                  <Link className="nav-link text-decoration-underline" to="/sobre">
                    <i className="bi bi-building-exclamation"></i> Sobre nós
                  </Link>
                </li>
                <li className="text-center d-inline-flex col-auto">
                  <Link className="nav-link  text-decoration-none text-white nav-link-icon login-btn px-0 align-items-center" to="/login">
                    <span className="login-icon">
                      <i className="bi bi-person"></i>
                    </span>
                    <span className="text-decoration-none">Login</span>
                  </Link>
                </li>
              </>
            )}
            {isCliente && (
              <>
                {session.configs_ativos[12] && (
                  <li className="d-inline-flex col-auto">
                    <Link className="nav-link" to="/dashboard">
                      <i className="bi bi-speedometer2"></i> Início
                    </Link>
                  </li>
                )}
                {session.configs_ativos[1] && (
                  <li className="d-inline-flex col-auto">
                    <Link className="nav-link nav-link-icon" to="/listar_usuarios">
                      <i className="bi bi-people"></i> Usuários
                    </Link>
                  </li>
                )}
                {session.configs_ativos[5] && (
                  <li className="d-inline-flex col-auto">
                    <Link className="nav-link nav-link-icon" to="/lista_lojas">
                      <i className="bi bi-shop"></i> Lojas
                    </Link>
                  </li>
                )}
                {session.configs_ativos[3] && (
                  <li className="d-inline-flex col-auto">
                    <Link className="nav-link nav-link-icon" to="/pdv">
                      <i className="bi bi-geo-alt"></i> Ponto De Vendas
                    </Link>
                  </li>
                )}
                {session.configs_ativos[6] && (
                  <li className="d-inline-flex col-auto">
                    <Link className="nav-link nav-link-icon" to="/lista_produtos">
                      <i className="bi bi-cart4"></i> Produtos
                    </Link>
                  </li>
                )}
                {session.configs_ativos[7] && (
                  <li className="d-inline-flex col-auto">
                    <Link className="nav-link nav-link-icon" to="/lista_vendas">
                      <i className="bi bi-cash"></i> Venda
                    </Link>
                  </li>
                )}
                {session.configs_ativos[8] && (
                  <li className="d-inline-flex col-auto">
                    <Link className="nav-link nav-link-icon" to="/lista_clientes">
                      <i className="bi bi-person-check"></i> Clientes
                    </Link>
                  </li>
                )}
                <li className="d-inline-flex col-auto">
                  <Link className="nav-link nav-link-icon" to="/configuracao">
                    <i className="bi bi-gear"></i> Configurações
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
