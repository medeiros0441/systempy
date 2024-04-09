
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
      var children = container.children;
      for (var i = 0; i < children.length; i++) {
          children[i].style.display = 'none';
      }

      // Cria o campo de carregamento
      var loadingContainer = document.createElement('div');
      loadingContainer.classList.add('loading');
      loadingContainer.classList.add('text-center');
      loadingContainer.classList.add('text-primary');

      var spinner = document.createElement('div');
      spinner.classList.add('spinner-border');
      spinner.setAttribute('role', 'status');

      var spinnerText = document.createElement('span');
      spinnerText.classList.add('visually-hidden');
      spinnerText.textContent = 'Loading...';

      spinner.appendChild(spinnerText);
      loadingContainer.appendChild(spinner);
      container.appendChild(loadingContainer);
  } else if (status === false) {
      // Remove o campo de carregamento, se existir
      var loadingContainer = container.querySelector('.loading');
      if (loadingContainer) {
          container.removeChild(loadingContainer);
      }

      // Exibe novamente os elementos filhos
      var children = container.children;
      for (var i = 0; i < children.length; i++) {
          children[i].style.display = 'block';
      }
  } else {
      console.error('Status inválido.');
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
    if (data) {
            requestOptions.body = JSON.stringify(data);
        }
  // Fazer uma requisição Fetch para o backend
  fetch(url, requestOptions)
      .then(response => {
          // Verificar se a resposta da requisição foi bem sucedida
          if (!response.ok) {
              throw new Error('Erro ao chamar a função Python: ' + response.statusText);
          }
          // Converter a resposta para JSON
          return response.json();
      })
      .then(data => {
          // Manipular a resposta do backend, se necessário
          console.log('Função Python chamada com sucesso!');
          callback({ success: true, data: data }); // Chamando o callback com sucesso e dados
      })
      .catch(error => {
          // Lidar com erros de requisição
          console.error('Erro ao chamar a função Python:', error.message);
          callback({ success: false, error: error.message });
      });
}

//alerta customizado
function alertCustomer(text,time=180000) {
    // Verificar se o container já existe
    let toastContainer = document.querySelector('.toast-container');

    // Se não existir, criar um novo container
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.classList.add('toast-container', 'position-fixed', 'top-0', 'end-0', 'p-3');
      document.body.appendChild(toastContainer);
    }

    // Criar um novo toast
    const toastElement = document.createElement('div');
    toastElement.classList.add('toast');
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');

    // Criar o cabeçalho do toast
    const toastHeader = document.createElement('div');
    toastHeader.classList.add('toast-header');
    const strongElement = document.createElement('strong');
    strongElement.classList.add('me-auto', 'Font-Gliker', 'fw-bold');
    strongElement.innerText = '{ S M W }';
    const buttonClose = document.createElement('button');
    buttonClose.setAttribute('type', 'button');
    buttonClose.classList.add('btn-close');
    buttonClose.setAttribute('data-bs-dismiss', 'toast');
    buttonClose.setAttribute('aria-label', 'Close');

    // Criar o corpo do toast
    const toastBody = document.createElement('div');
    toastBody.classList.add('toast-body');
    toastBody.classList.add('bg-white');
    toastBody.classList.add('rounded-bottom');
    toastBody.classList.add('shadow-lg');
    toastBody.innerText = text;

    // Montar a estrutura do toast
    toastHeader.appendChild(strongElement);
    toastHeader.appendChild(buttonClose);
    toastElement.appendChild(toastHeader);
    toastElement.appendChild(toastBody);
    toastContainer.appendChild(toastElement);

    // Inicializar o Bootstrap Toast
    const toastBootstrap = new bootstrap.Toast(toastElement);
    toastBootstrap.show();

    // Remover o toast após um tempo padrão (por exemplo, 5 segundos)
    setTimeout(() => {
      toastContainer.removeChild(toastElement);
    }, time); // Tempo em milissegundos, ajuste conforme necessário
  
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
            // Preenche os campos do formulário com os dados do endereço
            document.getElementById("id_rua").value = data.logradouro;
            document.getElementById("id_bairro").value = data.bairro;
            document.getElementById("id_cidade").value = data.localidade;
            document.getElementById("id_estado").value = data.uf;
            document.getElementById("id_numero").focus(); // Muda o foco para o campo de número
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

 