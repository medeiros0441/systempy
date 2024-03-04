
 // Máscara para CNPJ
 $('.cnpj-mask').mask('00.000.000/0000-00');
 $('.cpf-mask').mask('000.000.000-00');

 // Máscara para telefone
 $('.telefone-mask').mask('+55 (00) 0000-00000');
 $('.codigo-mask').mask('000-000');
 $('.cep-mask').mask('00000-000');
 
 function chamarFuncaoPython(DefName, data, callback, Type ="POST") {
  // Fazer uma requisição AJAX para o backend
  $.ajax({
    url: DefName,
    type: Type,
    data: data,
    success: function(response) {
      // Manipular a resposta do backend, se necessário
      console.log('Função Python chamada com sucesso!');
      console.log('Resposta:', response);
      callback({ success: true, data: response }); // Chamando o callback com sucesso e dados
    },
    error: function(xhr, status, error) {
      // Lidar com erros de requisição, se houver
      console.error('Erro ao chamar a função Python:', error);

      if (xhr.status === 404) {
        // Se o recurso não foi encontrado
        callback({ success: false, error: xhr.responseJSON.erro });
      } else if (xhr.status === 500) {
        // Se houve um erro interno do servidor
        callback({ success: false, error: 'Erro interno do servidor (500)' });
      } else {
        // Outros erros não especificados
        callback({ success: false, error: 'Erro desconhecido: ' + error });
      }
    }
  });
}


//alerta customizado
function alertCustomer(text) {



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
    }, 10000); // Tempo em milissegundos, ajuste conforme necessário
  
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
