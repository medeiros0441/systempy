import React from 'react';
import { createRoot } from 'react-dom/client';
import { LifeLine } from 'react-loading-indicators';

// Mapeia containers para suas raízes correspondentes
const rootMap = new Map();

export default function loading(status, container) {
  let targetContainer = null;

  if (typeof container === 'string') {
    targetContainer = document.getElementById(container);
    if (!targetContainer) {
      console.error(`Container com ID '${container}' não encontrado.`);
      return;
    }
  } else if (container instanceof HTMLElement) {
    targetContainer = container;
  } else {
    console.error('Tipo inválido para o container. Deve ser uma string (ID do elemento) ou HTMLElement.');
    return;
  }

  const loadingContainerId = `${targetContainer.id}-loading`;

  if (status === true) {
    // Oculta o container original
    targetContainer.style.display = 'none';

    // Cria e insere o container de loading
    let loadingContainer = document.getElementById(loadingContainerId);
    if (!loadingContainer) {
      loadingContainer = document.createElement('div');
      loadingContainer.id = loadingContainerId;
      loadingContainer.classList.add('loading', 'd-flex', 'justify-content-center', 'align-items-center');

      // Estilos para centralizar o loading
      loadingContainer.style.position = 'absolute';
      loadingContainer.style.top = '50%';
      loadingContainer.style.left = '50%';
      loadingContainer.style.transform = 'translate(-50%, -50%)';
      loadingContainer.style.minHeight = '200px';
      loadingContainer.style.width = '100%';
      loadingContainer.style.zIndex = '1000';

      // Insere o container no DOM
      targetContainer.insertAdjacentElement('afterend', loadingContainer);
    }

    // Se a raiz já existir, use-a; caso contrário, crie uma nova
    let root;
    if (rootMap.has(loadingContainerId)) {
      root = rootMap.get(loadingContainerId);
    } else {
      root = createRoot(loadingContainer);
      rootMap.set(loadingContainerId, root);
    }

    // Renderiza o componente LifeLine dentro do container de loading
    root.render(
      <LifeLine color="#32cd32" size="medium" text="" textColor="#ffffff" />
    );
  } else if (status === false) {
    // Remove o componente LifeLine e o container de loading
    const loadingContainer = document.getElementById(loadingContainerId);
    if (loadingContainer) {
      const root = rootMap.get(loadingContainerId); // Obtém a raiz existente
      if (root) {
        root.unmount(); // Desmonta o componente React
      }
      loadingContainer.remove(); // Remove o elemento do DOM
    }

    // Mostra o container original novamente
    targetContainer.style.display = '';
  }
}
