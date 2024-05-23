
 // Máscara para CNPJ
 $('.cnpj-mask').mask('00.000.000/0000-00');
 $('.cpf-mask').mask('000.000.000-00');
 $('.telefone-mask').mask('+55 (00) 0000-00000');
 $('.codigo-mask').mask('000-000');
 $('.cep-mask').mask('00000-000');
 $('.data-mask').mask('00/00/0000');
 $('.data-mes-ano-mask').mask('00/0000');
 $('.quantidade-mask').mask('00000000');
 $('.money-mask').mask('000.000.000,00', {reverse: true,});  


 


 function manageLoading(status, id_container) {
  var container = document.getElementById(id_container);
  
  if (!container) {
      console.error('Container não encontrado.');
      return;
  }

  if (status === true) {
      // Oculta o conteúdo do contêiner
      toggleContainerAnimation(id_container, true);
      // Cria o campo de carregamento 
      loadingContainer = document.createElement('div');
        loadingContainer.classList.add('loading', 'd-flex', 'justify-content-center','my-5', 'align-items-center');
        loadingContainer.classList.add('text-primary');

      var spinner = document.createElement('div');
      spinner.classList.add('spinner-border');
      spinner.setAttribute('role', 'status');

      var spinnerText = document.createElement('span');
      spinnerText.classList.add('visually-hidden');
      spinnerText.textContent = 'Loading...';

      spinner.appendChild(spinnerText);
      loadingContainer.appendChild(spinner);
      container.insertAdjacentElement('afterend', loadingContainer);
  } else if (status === false) {
    var loadingContainer = container.nextElementSibling;
    
    if (loadingContainer && loadingContainer.classList.contains('loading')) {
        loadingContainer.remove();
    }  
      // Exibe novamente os elementos filhos
      toggleContainerAnimation(id_container, false);
  }  
} 
  // Definir uma variável global para rastrear se uma animação está em andamento
var animationInProgress = false;
function toggleContainerAnimation(containerId, isOpen) {
    const container = document.getElementById(containerId);
    
    if (!container) {
        console.error('Container não encontrado.');
        return;
    }
        if (!isOpen) {
            container.classList.remove('d-none'); // Adicionar a classe d-none para ocultar o container após a animação terminar
          
        } else {
             container.classList.add('d-none'); // Adicionar a classe d-none para ocultar o container após a animação terminar
        }
    } 
  
  
function chamarFuncaoPython(url, data,type, callback)  {
  // Configuração do objeto de requisição
  const requestOptions = {
      method: type,
      headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json' 
      },
      
  };
  if (type === 'POST' || type === 'PUT') {
    requestOptions.body = JSON.stringify(data);
  }

  // Fazer uma requisição Fetch para o backend
  fetch(url, requestOptions)
      .then(response => response.json())
      .then(data => {
          callback(data); // Chamando o callback com sucesso e dados
      })
      .catch(error => {
          callback(error);
      });
}function showAlert(type, text, containerId) {
    const container = document.getElementById(containerId) || document.getElementById("id_alert_container");
    if (!container) return;

    // Remove any existing alert
    const existingAlert = container.querySelector('.alert');
    if (existingAlert) {
        container.removeChild(existingAlert);
    }

    // Define alert types
    const alertTypes = {
        1: { class: "alert-success", icon: "bi-check-circle-fill" },
        2: { class: "alert-danger", icon: "bi-exclamation-circle-fill" },
        3: { class: "alert-warning", icon: "bi-exclamation-triangle-fill" },
        default: { class: "alert-info", icon: "bi-info-circle-fill" }
    };

    const { class: alertClass, icon: iconClass } = alertTypes[type] || alertTypes.default;

    // Create the alert div
    const alertDiv = document.createElement("div");
    alertDiv.classList.add("alert", alertClass, "alert-dismissible", "fade", "show");
    alertDiv.setAttribute("role", "alert");

    // Create and add the close button
    const closeButton = document.createElement("button");
    closeButton.classList.add("btn-close");
    closeButton.setAttribute("type", "button");
    closeButton.setAttribute("data-bs-dismiss", "alert");
    closeButton.setAttribute("aria-label", "Close");
    alertDiv.appendChild(closeButton);

    // Create and add the icon
    const iconSpan = document.createElement("span");
    iconSpan.classList.add("bi", iconClass);
    iconSpan.setAttribute("aria-hidden", "true");
    alertDiv.appendChild(iconSpan);

    // Add the text message
    alertDiv.appendChild(document.createTextNode(" " + text));

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

    const toastBootstrap = new bootstrap.Toast(toastElement);
    toastBootstrap.show();

    setTimeout(() => {
        toastContainer.removeChild(toastElement);
    }, time);
}

function alertCustomer(text, type = null, container = false, time = 180000) {
    if (type === null) {
        showCustomAlert(text, container, time);
    } else {
        showAlert(type, text, container);
    }
}

  // Função para buscar o endereço com base no CEP
  function buscarEnderecoPorCEP() {
    // Pega o valor do campo de CEP
    var cep = document.getElementById("id_codigo_postal").value;
    
    // Remove qualquer caractere que não seja um número
    cep = cep.replace(/\D/g, '');

    // Verifica se o CEP tem a quantidade correta de dígitos
    if (cep.length === 8) {
        // Faz a requisição para o serviço que retorna os detalhes do endereço
        fetch('https://viacep.com.br/ws/' + cep + '/json/')
        .then(response => response.json())
        .then(data => {
            if(!data.erro){   // Preenche os campos do formulário com os dados do endereço
            document.getElementById("id_rua").value = data.logradouro;
            document.getElementById("id_bairro").value = data.bairro;
            document.getElementById("id_cidade").value = data.localidade;
            document.getElementById("id_estado").value = data.uf;
            document.getElementById("id_numero").focus();
            } // Muda o foco para o campo de número
        })
        .catch(error => {
            console.error('Erro ao buscar endereço:', error);
        });
    } else {
        alertCustomer('CEP inválido. Por favor, insira um CEP válido.');
    }
}

// Adiciona um event listener para chamar a função ao sair do campo de CEP
if (document.getElementById("id_codigo_postal")) {
  document.getElementById("id_codigo_postal").addEventListener("blur", buscarEnderecoPorCEP);
}

 