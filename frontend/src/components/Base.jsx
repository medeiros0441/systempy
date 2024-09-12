import React from 'react';
import Navbar from './containers/default/Navbar';
import MainContent from './containers/default/MainContent';
import Footer from './containers/default/Footer';
import 'react-bootstrap';
import Title from './TitleNavegador'
const Base = ({ children }) => {

  return (
    <>
      <Title />
      <div className="container-fluid m-0 p-0 wrapper  " style={{ background: '#f5f7fa' }}>
        <div className="wrapper">
          <div className="content">
            <Navbar />
            <MainContent>
              {children}
            </MainContent>
          </div>
          <div className="footer">

            <div className="custom-shape-divider-bottom-1708368458 mt-3" style={{ marginBottom: '-2px' }}>
              <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M985.66,92.83C906.67,72,823.78,31,743.84,14.19c-82.26-17.34-168.06-16.33-250.45.39-57.84,11.73-114,31.07-172,41.86A600.21,600.21,0,0,1,0,27.35V120H1200V95.8C1132.19,118.92,1055.71,111.31,985.66,92.83Z" className="shape-fill"></path>
              </svg>
            </div>
            <Footer />
          </div>
        </div>

      </div>
    </>
  );
};

export default Base;
