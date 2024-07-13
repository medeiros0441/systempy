
  
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
    } 
}

// Adiciona um event listener para chamar a função ao sair do campo de CEP
if (document.getElementById("id_codigo_postal")) {
  document.getElementById("id_codigo_postal").addEventListener("blur", buscarEnderecoPorCEP);
}
function applyAutocomplete() {
    document.querySelectAll(".autocomplete_input").each(function() {
        var $input = this;
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

        // Definir o número máximo de itens
        var maxItems = 5; // Altere este valor para o número desejado de sugestões

        // Inicializando o autocompletar no campo de entrada atual
        $input.autocomplete({
            source: function(request, response) {
                var filteredValues = this.ui.autocomplete.filter(values, request.term);
                response(filteredValues.slice(0, maxItems));
            },
            minLength: 0,
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

        $input.focus(function() {
            this.autocomplete("search", ""); // Chamar o método search com uma string vazia
        });
    });
}
 

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