import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';

// Hook customizado para controlar o modal
export const useCustomModal = () => {
  const [show, setShow] = useState(false);

  const CustomModal = ({ icon, title, children, footer }) => (
    <Modal
      show={show}
      backdrop="static"
      keyboard={false}
      contentClassName="bg-light"
      dialogClassName="modal-md modal-dialog-centered  modal-dialog-scrollable  "
      aria-labelledby="staticBackdropLabel"
    >
      <Modal.Header className="text-dark py-2">
        <h5 id="staticBackdropLabel" className="modal-title fs-5 font-monospace text-black fw-bolder">
          <i className={`me-2 bi bi-${icon}`}></i>
          {title}
        </h5>
        <Button
          variant="link"
          onClick={() => setShow(false)}  // <-- Corrigido aqui
          className="ms-auto mt-0 p-0"
          style={{ textDecoration: 'none', color: 'black' }}
        >
          <i className="bi bi-x fw-bold" style={{ fontSize: '25px' }} />
        </Button>
      </Modal.Header>
      <Modal.Body className="text-dark">
        {children}
      </Modal.Body>
      <Modal.Footer className="text-dark py-2 d-flex  justify-content-between">
        {footer}
      </Modal.Footer>
    </Modal>
  );

  return { CustomModal, setShow };
};
