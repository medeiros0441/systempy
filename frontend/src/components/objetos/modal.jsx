import React, { forwardRef, useImperativeHandle, useState } from 'react';
import { Modal, Button } from 'react-bootstrap';

const CustomModal = forwardRef(({ title, children, footer }, ref) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  useImperativeHandle(ref, () => ({
    openModal: handleShow,
    closeModal: handleClose,
  }));

  return (
    <Modal
      show={show}
      onHide={handleClose}
      backdrop="static"
      keyboard={false}
      contentClassName="bg-light  "
      dialogclassName=" modal-md modal-dialog-centered"
      aria-labelledby="staticBackdropLabel" className=" ">
      <Modal.Header className="text-dark ">
        <h5 id="staticBackdropLabel" className="modal-title fs-5 font-monospace text-black fw-bolder">
          {title}
        </h5>
        <Button variant="link" onClick={handleClose} className="ms-auto mt-0 p-0" style={{ textDecoration: 'none', color: 'black' }} >
          <i class="bi bi-x fw-bold" style={{ fontSize: '25px' }} />
        </Button>
      </Modal.Header>
      <Modal.Body className=" text-dark">
        {children}
      </Modal.Body>
      <Modal.Footer className=" text-dark">
        {footer}
      </Modal.Footer>
    </Modal>
  );
});

export default CustomModal;
