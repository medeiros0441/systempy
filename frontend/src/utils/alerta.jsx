import { Modal } from 'bootstrap';  // Importação do modal do Bootstrap

function showAlert(type, text, containerId) {
  const container = document.getElementById(containerId) || document.getElementById('id_alert_container');
  if (!container) return;

  // Remove any existing alert
  const existingAlert = container.querySelector('.alert');
  if (existingAlert) {
    container.removeChild(existingAlert);
  }

  // Define alert types
  const alertTypes = {
    1: { class: 'alert-success', icon: 'bi-check-circle-fill' },
    2: { class: 'alert-danger', icon: 'bi-exclamation-circle-fill' },
    3: { class: 'alert-warning', icon: 'bi-exclamation-triangle-fill' },
    default: { class: 'alert-info', icon: 'bi-info-circle-fill' },
  };

  const { class: alertClass, icon: iconClass } = alertTypes[type] || alertTypes.default;

  // Create the alert div
  const alertDiv = document.createElement('div');
  alertDiv.classList.add('alert', alertClass, 'alert-dismissible', 'fade', 'show', 'my-2');
  alertDiv.setAttribute('role', 'alert');

  // Create and add the close button
  const closeButton = document.createElement('button');
  closeButton.classList.add('btn-close');
  closeButton.setAttribute('type', 'button');
  closeButton.setAttribute('data-bs-dismiss', 'alert');
  closeButton.setAttribute('aria-label', 'Close');
  alertDiv.appendChild(closeButton);

  // Create and add the icon
  const iconSpan = document.createElement('span');
  iconSpan.classList.add('bi', iconClass);
  iconSpan.setAttribute('aria-hidden', 'true');
  alertDiv.appendChild(iconSpan);

  // Add the text message
  alertDiv.appendChild(document.createTextNode(' ' + text));

  // Prepend the alert to the container (to place it above other elements)
  container.insertBefore(alertDiv, container.firstChild);
}

function showCustomAlert(text, containerId, time) {
  let toastContainer = document.querySelector('.toast-container');

  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.classList.add('toast-container', 'position-fixed', 'top-0', 'end-0', 'p-3');
    document.body.appendChild(toastContainer);
  }

  const toastElement = document.createElement('div');
  toastElement.classList.add('toast');
  toastElement.setAttribute('role', 'alert');
  toastElement.setAttribute('aria-live', 'assertive');
  toastElement.setAttribute('aria-atomic', 'true');

  const toastHeader = document.createElement('div');
  toastHeader.classList.add('toast-header');
  const strongElement = document.createElement('strong');
  strongElement.classList.add('me-auto', 'Font-Gliker', 'fw-bold');
  strongElement.innerText = '{ C P S }';
  const buttonClose = document.createElement('button');
  buttonClose.setAttribute('type', 'button');
  buttonClose.classList.add('btn-close');
  buttonClose.setAttribute('data-bs-dismiss', 'toast');
  buttonClose.setAttribute('aria-label', 'Close');

  const toastBody = document.createElement('div');
  toastBody.classList.add('toast-body', 'bg-white', 'rounded-bottom', 'shadow-lg');
  toastBody.innerText = text;

  toastHeader.appendChild(strongElement);
  toastHeader.appendChild(buttonClose);
  toastElement.appendChild(toastHeader);
  toastElement.appendChild(toastBody);
  toastContainer.appendChild(toastElement);

  const toastBootstrap =   Modal.Toast(toastElement);
  toastBootstrap.show();

  setTimeout(() => {
    toastContainer.removeChild(toastElement);
  }, time);
}

export default function alerta(text, type = null, container = false, time = 180000) {
  if (type === null) {
    showCustomAlert(text, container, time);
  } else {
    showAlert(type, text, container);
  }
}
