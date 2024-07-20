import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import { FaTimes } from 'react-icons/fa'; // Importa o ícone X

const CustomModal = ({ title, children, footer }) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <Modal
        show={show}
        onHide={handleClose}
        backdrop="static"
        keyboard={false}
        aria-labelledby="staticBackdropLabel"
      >
        <Modal.Dialog  className="modal-dialog modal-md modal-dialog-centered">
          <Modal.Content className="bg-dark">
            <Modal.Header>
              <Modal.Title id="staticBackdropLabel" className="fs-5 font-monospace text-white">
                {title}
              </Modal.Title>
              <Button variant="link" onClick={handleClose} style={{ textDecoration: 'none', color: 'white' }}>
                <FaTimes />
              </Button>
            </Modal.Header>
            <Modal.Body className="text-white">
              {children}
            </Modal.Body>
            <Modal.Footer className="text-white">
              {footer}
            </Modal.Footer>
          </Modal.Content>
        </Modal.Dialog>
      </Modal>
    </>
  );
};

export default CustomModal;
