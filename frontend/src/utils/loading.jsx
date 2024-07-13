import React from 'react';
import { createRoot } from 'react-dom/client';

export function manageLoading(status, idContainer) {
  const container = document.getElementById(idContainer);

  if (!container) {
    console.error('Container não encontrado.');
    return;
  }

  const loadingContainerId = `${idContainer}-loading`;

  if (status === true) {
    const loadingContainer = document.createElement('div');
    loadingContainer.id = loadingContainerId;
    loadingContainer.classList.add('loading', 'd-flex', 'justify-content-center', 'my-5', 'align-items-center', 'text-primary');

    const spinner = document.createElement('div');
    spinner.classList.add('spinner-border');
    spinner.setAttribute('role', 'status');

    const spinnerText = document.createElement('span');
    spinnerText.classList.add('visually-hidden');
    spinnerText.textContent = 'Loading...';

    spinner.appendChild(spinnerText);
    loadingContainer.appendChild(spinner);
    container.insertAdjacentElement('afterend', loadingContainer);
  } else if (status === false) {
    const loadingContainer = document.getElementById(loadingContainerId);
    if (loadingContainer) {
      loadingContainer.remove();
    }
  }
}

export function LoadingIndicator() {
  return (
    <div className="d-flex justify-content-center my-5 align-items-center text-primary">
      <div className="spinner-border" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
}
