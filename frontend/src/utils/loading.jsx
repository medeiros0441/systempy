export default function loading(status, container) {
  let targetContainer = null;

  if (typeof container === 'string') {
    // Se o container for uma string, assume-se que é o ID do elemento
    targetContainer = document.getElementById(container);
    if (!targetContainer) {
      console.error(`Container com ID '${container}' não encontrado.`);
      return;
    }
  } else if (container instanceof HTMLElement) {
    // Se o container for um elemento HTMLElement, utiliza diretamente
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
    const loadingContainer = document.createElement('div');
    loadingContainer.id = loadingContainerId;
    loadingContainer.classList.add('loading', 'd-flex', 'justify-content-center', 'align-items-center', 'text-primary');
    
    // Adiciona estilos inline para garantir tamanho significativo
    loadingContainer.style.minHeight = '200px'; // Defina a altura mínima desejada
    loadingContainer.style.width = '100%'; // Preenche a largura do container pai
    loadingContainer.style.backgroundColor = 'rgba(255, 255, 255, 0.8)'; // Fundo com leve transparência (opcional)

    const spinner = document.createElement('div');
    spinner.classList.add('spinner-border');
    spinner.setAttribute('role', 'status');

    const spinnerText = document.createElement('span');
    spinnerText.classList.add('visually-hidden');
    spinnerText.textContent = 'Loading...';

    spinner.appendChild(spinnerText);
    loadingContainer.appendChild(spinner);
    targetContainer.insertAdjacentElement('afterend', loadingContainer);
  } else if (status === false) {
    // Remove o container de loading
    const loadingContainer = document.getElementById(loadingContainerId);
    if (loadingContainer) {
      loadingContainer.remove();
    }

    // Mostra o container original novamente
    targetContainer.style.display = '';
  }
}
