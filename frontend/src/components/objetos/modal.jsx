import React, { forwardRef, useImperativeHandle, useState } from 'react';
import { Modal, Button } from 'react-bootstrap';

const CustomModal = forwardRef(({ title, children, footer }, ref) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  useImperativeHandle(ref, () => ({
    openModal: handleShow,
  }));

  return (
    <Modal
      show={show}
      onHide={handleClose}
      backdrop="static"
      keyboard={false}
      contentClassName=" bg-dark "
      dialogclassName=" modal-md modal-dialog-centered"
      aria-labelledby="staticBackdropLabel" className=" ">
    <Modal.Header  className="modal-header">
            <h5 id="staticBackdropLabel" className="modal-title fs-5 font-monospace text-white">
              {title}
            </h5>
            <Button variant="link" onClick={handleClose} className="ms-auto mt-0 p-0" style={{ textDecoration: 'none', color: 'white' }} >
            <i class="bi bi-x fw-bold" style={{fontSize: '25px'}}  />
            </Button>
        </Modal.Header>
          <Modal.Body className="modal-body text-white">
            {children}
          </Modal.Body>
          <Modal.Footer  className="modal-footer text-white">
            {footer}
          </Modal.Footer>
    </Modal>
  );
});

export default CustomModal;
