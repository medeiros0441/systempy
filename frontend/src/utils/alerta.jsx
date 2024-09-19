import { Toast } from 'bootstrap';  // Importação correta do toast do Bootstrap

// Função para criar um alert div
function createAlertDiv(type, text) {
  const alertTypes = {
    1: { class: 'alert-success', icon: 'bi-check-circle-fill' },
    2: { class: 'alert-danger', icon: 'bi-exclamation-circle-fill' },
    3: { class: 'alert-warning', icon: 'bi-exclamation-triangle-fill' },
    default: { class: 'alert-info', icon: 'bi-info-circle-fill' },
  };

  const { class: alertClass, icon: iconClass } = alertTypes[type] || alertTypes.default;

  const alertDiv = document.createElement('div');
  alertDiv.className = `alert ${alertClass} alert-dismissible fade show mt-1  mb-1  mx-2 d-inline-flex`;
  alertDiv.setAttribute('role', 'alert');

  const closeButton = document.createElement('button');
  closeButton.className = 'btn-close';
  closeButton.type = 'button';
  closeButton.setAttribute('data-bs-dismiss', 'alert');
  closeButton.setAttribute('aria-label', 'Close');

  closeButton.addEventListener('click', () => {
    const containerWrapper = alertDiv.parentElement;
    if (containerWrapper) containerWrapper.remove();
  });

  const iconSpan = document.createElement('span');
  iconSpan.className = `bi ${iconClass} me-2`;
  iconSpan.setAttribute('aria-hidden', 'true');

  alertDiv.appendChild(iconSpan);
  alertDiv.appendChild(document.createTextNode(` ${text}`));
  alertDiv.appendChild(closeButton);

  return alertDiv;
}

// Função para mostrar um alert
function showAlert(type, text, containerId) {
  const container = document.getElementById(containerId) || document.getElementById('id_alert_container');
  if (!container) return;

  const existingAlert = container.querySelector('.alert');
  if (existingAlert) existingAlert.parentElement.remove();

  const alertDiv = createAlertDiv(type, text);
  const containerWrapper = document.createElement('div');
  containerWrapper.className = 'd-flex justify-content-center';
  containerWrapper.appendChild(alertDiv);

  container.insertBefore(containerWrapper, container.firstChild);
}

// Função para mostrar um toast
function showCustomAlert(text, containerId, time) {
  let toastContainer = document.querySelector('.toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(toastContainer);
  }

  const toastElement = document.createElement('div');
  toastElement.className = 'toast';
  toastElement.setAttribute('role', 'alert');
  toastElement.setAttribute('aria-live', 'assertive');
  toastElement.setAttribute('aria-atomic', 'true');

  const toastHeader = document.createElement('div');
  toastHeader.className = 'toast-header';

  const strongElement = document.createElement('strong');
  strongElement.className = 'me-auto Font-Gliker fw-bold';
  strongElement.innerText = '{ C P S }';

  const buttonClose = document.createElement('button');
  buttonClose.type = 'button';
  buttonClose.className = 'btn-close';
  buttonClose.setAttribute('data-bs-dismiss', 'toast');
  buttonClose.setAttribute('aria-label', 'Close');

  const toastBody = document.createElement('div');
  toastBody.className = 'toast-body bg-white rounded-bottom shadow-lg';
  toastBody.innerText = text;

  toastHeader.append(strongElement, buttonClose);
  toastElement.append(toastHeader, toastBody);
  toastContainer.appendChild(toastElement);

  const toastBootstrap = new Toast(toastElement);
  toastBootstrap.show();

  setTimeout(() => {
    toastContainer.removeChild(toastElement);
  }, time);
}

// Função principal para mostrar alertas ou toasts
export default function alerta(text, type = null, container = false, time = 180000) {
  if (type === null) {
    showCustomAlert(text, container, time);
  } else {
    showAlert(type, text, container);
  }
}
