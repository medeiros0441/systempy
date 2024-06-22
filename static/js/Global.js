
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
  if (data != null) {
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
    alertDiv.classList.add("alert", alertClass, "alert-dismissible", "fade", "show","my-2");
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

function applyAutocomplete() {
    // Selecionando todos os elementos com a classe 'autocomplete_input'
    $(".autocomplete_input").each(function() {
        var $input = $(this);
        var storageKey = $input.data("storage"); // Chave para acessar os dados no localStorage
        var propertyKeys = $input.data("key"); // Propriedade a ser usada como valor
        var propertyLabels = $input.data("label").split(","); // Propriedades a serem exibidas

        // Tentando obter os dados do localStorage
        var rawData = localStorage.getItem(storageKey);
        if (!rawData) {
            console.error(`Nenhum dado encontrado no localStorage para a chave: ${storageKey}`);
            return;
        }

        // Tentando fazer o parse dos dados
        var data;
        try {
            data = JSON.parse(rawData);
        } catch (e) {
            console.error(`Erro ao fazer o parse dos dados do localStorage para a chave: ${storageKey}`, e);
            return;
        }

        var values = []; // Array de valores para o autocomplete

        // Função auxiliar para obter valores de propriedades de um objeto
        function getPropertyValues(item, keys) {
            if (keys === '*') {
                return JSON.stringify(item); // Retorna todo o objeto como uma string se todas as propriedades forem necessárias
            } else if (typeof keys === 'string') {
                return item[keys]; // Retorna o valor da propriedade especificada
            } else if (Array.isArray(keys)) {
                return keys.map(key => item[key]).join(', '); // Retorna os valores das propriedades especificadas como uma string
            }
        }

        // Iterando sobre os dados e construindo a lista de valores disponíveis
        data.forEach(function(item) {
            var id = getPropertyValues(item, propertyKeys);
            var label = getPropertyValues(item, propertyLabels);

            if (id && typeof label === 'string') {
                values.push({ label: label, id: id });
            }
        });

        // Inicializando o autocompletar no campo de entrada atual
        $input.autocomplete({
            source: values,
            select: function(event, ui) {
                var selectedId = ui.item.id;
                var selectedLabel = ui.item.label;

                // Mudar o valor do input para o label do item selecionado
                $input.val(selectedLabel);
                // Armazenar o id do item selecionado no atributo data-value
                $input.attr("data-value", selectedId);

                var onSelectConfig = $input.data("onselect"); // Configuração de seleção
                if (onSelectConfig) {
                    var onSelectParams = onSelectConfig.split(","); // Dividindo a configuração
                    var onSelectFunction = window[onSelectParams[0]]; // Função de seleção
                    if (typeof onSelectFunction === "function") {
                        onSelectFunction(selectedId); // Chamando a função de seleção com o valor relevante
                    }
                }

                return false; // Evitar que o valor padrão do label seja inserido no input
            }
        });
    });
}

$(function () {
    // Selecionar todos os botões com a classe btn_confirmacao
    const buttons = document.querySelectorAll('.btn_confirmacao');
    
    // Adicionar um evento de clique a cada botão
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Desativar o botão clicado
            button.disabled = true;
            // Adicionar a classe de desativação do Bootstrap
            button.classList.add('disabled');

            // Reativar o botão após um tempo (por exemplo, 5 segundos)
            setTimeout(() => {
                button.disabled = false;
                button.classList.remove('disabled');
            }, 5000);
        });
    });
});
document.addEventListener("DOMContentLoaded", function() {
    // Verifica todos os alertas com data-info-codigo
    document.querySelectorAll('.container-alert-personalizado').forEach(function(alert) {
        var infoCodigo = alert.getAttribute('data-codigo');
        var data_label_a = alert.getAttribute('data-labela');
        var data_label_b = alert.getAttribute('data-labelb') || "";

        // Cria a nova estrutura de alerta
        var newContainer = document.createElement('div');
        newContainer.className = 'container text-light mt-2 mx-auto pt-2';

        var alertDiv = document.createElement('div');
        alertDiv.id = 'alert1';
        alertDiv.className = 'alert alert-warning text-dark d-none';
        alertDiv.setAttribute('role', 'alert');
        alertDiv.setAttribute('data-info-codigo', infoCodigo);

        var alertHeader = document.createElement('div');
        alertHeader.className = 'd-flex mb-2 justify-content-between align-items-center border-bottom border-dark';

        var alertHeading = document.createElement('h4');
        alertHeading.className = 'alert-heading col-auto';
        alertHeading.style.fontSize = '1.0rem';
        alertHeading.innerHTML = '<i style="font-size:1.0rem" class="bi me-2 bi-info-circle-fill"></i> Informações';

        var closeButton = document.createElement('div');
        closeButton.className = 'close ms-auto';
        closeButton.setAttribute('type', 'button');
        closeButton.setAttribute('aria-label', 'Close');
        closeButton.onclick = function() { closeAlert(infoCodigo); };
        closeButton.innerHTML = '<i style="font-size:1.0rem" class="bi me-2 bi-x-circle"></i>';

        alertHeader.appendChild(alertHeading);
        alertHeader.appendChild(closeButton);

        var alertContent = document.createElement('p');
        alertContent.className = 'text-dark';
        alertContent.style.fontSize = '0.9rem';
        alertContent.textContent = data_label_a; // Valor do primeiro data-label0000000000000000
      
        alertDiv.appendChild(alertHeader);
        alertDiv.appendChild(alertContent);
          if (data_label_b != ""){
            var alertHr = document.createElement('hr');
            alertHr.className = 'my-2';
            var alertFooter = document.createElement('p');
            alertFooter.className = 'mb-0 text-dark small';
            alertFooter.textContent = data_label_b; // Valor do segundo data-label
            alertDiv.appendChild(alertHr);
            alertDiv.appendChild(alertFooter);
        }    

        newContainer.appendChild(alertDiv);

        // Substitui o container original com o novo
        alert.replaceWith(newContainer);

        // Verifica o cookie para exibir o alerta
        if (getCookie(infoCodigo) !== 'true') {
            alertDiv.classList.remove('d-none');
        }
    });
});

function closeAlert(codigo) {
    var alert = document.querySelector('[data-info-codigo="' + codigo + '"]');
    if (alert) {
        alert.classList.add('d-none');
        setCookie(codigo, 'true', 30);
    }
}
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}