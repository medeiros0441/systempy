
document.getElementById('id_metodo_entrega').addEventListener('change', function() {
    var selectedOption = this.value; // Obtém o valor selecionado
    var containerEntrega = document.getElementById('id_container_entrega');

    // Verifica se a opção selecionada é "entrega_no_local"
    if (selectedOption === 'entrega_no_local') {
      containerEntrega.classList.remove('d-none'); // Remove a classe d-none
    } else {
      containerEntrega.classList.add('d-none'); // Adiciona a classe d-none
    }
  });
 
function toggleGestaoCliente(status) {
    var container = document.getElementById("container_gestao_cliente");  
    var btn_gestao_cliente = document.getElementById("btn_gestao_cliente");
    if(status===1){
        status = true;
        gerencia_container_cliente(1)
    }
    if (status) {
        container.classList.remove("d-none");
        btn_gestao_cliente.innerHTML = '<i class="bi bi-eye"></i>'; 
        btn_gestao_cliente.onclick = function() { toggleGestaoCliente(false); };
    }  else  {
        container.classList.add("d-none");
        btn_gestao_cliente.innerHTML = '<i class="bi bi-eye-slash"></i>'; 
        btn_gestao_cliente.onclick = function() { toggleGestaoCliente(true); };
    }

}
function gerencia_container_cliente(obj) {
    var selectcliente = document.getElementById("select_cliente");
    var btnCadastrarCliente = document.getElementById("btnCadastrarCliente");
    var formcliente = document.getElementById("cadastrar_cliente");
    // Verifica se a chamada foi para mostrar o formulário de seleção de cliente
    if (obj == 1 && selectcliente.classList.contains("d-none")) {
        // Mostra o formulário de seleção de cliente e oculta o formulário de cadastro de cliente
        selectcliente.classList.remove("d-none");
        formcliente.classList.add("d-none");
        // Atualiza o ícone do botão de cadastrar cliente e atribui a função toggleGestaoCliente
        btnCadastrarCliente.innerHTML = '<i class="bi bi-person-plus"></i>';
        // Atualiza o valor do onclick do botão para chamar toggleGestaoCliente com o argumento 1
        btnCadastrarCliente.onclick =function() { gerencia_container_cliente(2); };
        // Carrega a lista de clientes
        carregarListaClientes();
    } 
    // Verifica se a chamada foi para mostrar o formulário de cadastro de cliente
    if (obj == 2 && formcliente.classList.contains("d-none")) {
        // Oculta o formulário de seleção de cliente e mostra o formulário de cadastro de cliente
        selectcliente.classList.add("d-none");
        formcliente.classList.remove("d-none");
        // Atualiza o ícone do botão de cadastrar cliente e atribui a função toggleGestaoCliente
        btnCadastrarCliente.innerHTML = '<i class="bi bi-arrow-return-left"></i>'; 
        btnCadastrarCliente.onclick =function() { gerencia_container_cliente(1); };
        toggleGestaoCliente(true);
    }
} 
function listarMotoboys() {
    var container = document.getElementById('container_gestao_entrega');
    manageLoading(true,"container_gestao_entrega"); 
    if (container) {
        listarMotoboysPorEmpresa()
        .then(result => {
            if (result.success) {
                var selectMotoboy = document.getElementById('id_motoboy');
                selectMotoboy.innerHTML = ''; // Limpar as opções existentes
                
                // Adicionar as opções dos motoboys
                result.data.forEach(motoboy => {
                    var option = document.createElement('option');
                    option.value = motoboy.id_motoboy;
                    option.text = motoboy.nome;
                    selectMotoboy.appendChild(option);
                });
            alertCustomer('Lista de motoboys atualizada.');
            } else {
                alertCustomer(result.data);
            }
        manageLoading(false,"container_gestao_entrega"); 
        })
    .catch(error => {
        alertCustomer(error.message);
    });
}
}


function insertCliente() {
    const formInputs = {
        'nome': document.getElementById('id_nome_cliente').value.trim(),
        'telefone': document.getElementById('id_telefone_cliente').value.trim(),
        'descricao': document.getElementById('id_descricao_cliente').value.trim(),
        'rua': document.getElementById('id_rua').value.trim(),
        'numero': document.getElementById('id_numero').value.trim(),
        'cep': document.getElementById('id_codigo_postal').value.trim(),
        'estado': document.getElementById('id_estado').value.trim(),
        'bairro': document.getElementById('id_bairro').value.trim(),
        'cidade': document.getElementById('id_cidade').value.trim(),
        'descricao_endereco': document.querySelector('#form_descricao #id_descricao').value.trim(),
        'tipo_cliente': document.getElementById('id_select_tipo_cliente').value.trim()
    };

    // Verificar se todos os campos obrigatórios estão preenchidos
    const obrigatoryFields = ['nome', 'telefone', 'tipo_cliente'];
    for (const field of obrigatoryFields) {
        if (!formInputs[field]) {
            alertCustomer(`preencha o campo ${field}, é obrigatório.`);
            return;
        }
    }

    // Ativar o indicador de carregamento
    manageLoading(true, "cadastrar_cliente");
    chamarFuncaoPython('/api/cliente/create/', formInputs, 'POST', function(response) {
        if (response.data) {
            alertCustomer("Cliente criado com sucesso!");
            manageLoading(false, "cadastrar_cliente");
            toggleGestaoCliente(1)
            montarInfoCliente(response.data);
        } else {
            alertCustomer('Ocorreu um erro ao criar o cliente: ' + response.error);
            manageLoading(false, "cadastrar_cliente"); // Chamando o callback sem dados do cliente e com o erro
        }
    } );
     
}
var clientesCache = null;
function manipularPesquisaClientes(clientes) {
    const inputPesquisa = document.getElementById('pesquisa_cliente');
    const resultPesquisa = document.getElementById('result-pesquisa');
    const clienteIdInput = document.getElementById('id_cliente');
    exibirResultados(clientes);
    inputPesquisa.addEventListener('input', function(event) {
        const termoPesquisa = event.target.value.toLowerCase();
        manageLoading(true, "result-pesquisa");

        const resultados = clientes.filter(cliente => {
            return Object.values(cliente).some(value =>
                value && value.toString().toLowerCase().includes(termoPesquisa)
            );
        });

        exibirResultados(resultados);
    });

    function exibirResultados(resultados) {
        resultPesquisa.innerHTML = '';

        resultados.forEach(cliente => {
            const divResultado = document.createElement('div');
            divResultado.classList.add('p-2', 'my-1', 'mx-2',  'border', 'rounded',  'flex-wrap', 'text-center', 'd-intial-flex',);

            const iconUsuario = document.createElement('i');
            iconUsuario.classList.add('bi', 'bi-person-fill', 'me-2');

            const detalhesCliente = document.createElement('div');
            detalhesCliente.classList.add('flex-grow-1', 'me-3');

            const nomeCliente = document.createElement('span');
            nomeCliente.textContent = cliente.nome;
            nomeCliente.classList.add('fw-bold');
            detalhesCliente.appendChild(iconUsuario);
            detalhesCliente.appendChild(nomeCliente);
            detalhesCliente.appendChild(document.createElement('br'));

            const telefoneCliente = document.createElement('span');
            telefoneCliente.textContent = cliente.telefone;
            detalhesCliente.appendChild(telefoneCliente);
            detalhesCliente.appendChild(document.createElement('br'));

            const enderecoCliente = document.createElement('span');
            enderecoCliente.textContent = `${cliente.rua} ${cliente.numero} ${cliente.bairro} ${cliente.cidade}`;
            detalhesCliente.appendChild(enderecoCliente);

            divResultado.appendChild(detalhesCliente);

            const btnSelecionar = document.createElement('button');
            btnSelecionar.textContent = 'Selecionar';
            btnSelecionar.classList.add('btn', 'btn-primary', 'btn-sm', 'mx-auto');
            btnSelecionar.setAttribute("type", "button");
            btnSelecionar.addEventListener('click', function() {
                clienteIdInput.value = cliente.id_cliente;
                montarInfoCliente(cliente); 
            });

            divResultado.appendChild(btnSelecionar);

            resultPesquisa.appendChild(divResultado);
        });

        toggleResultadoPesquisa(true);
        manageLoading(false, "result-pesquisa");
    }
}
// Função para alternar a visibilidade do container
function toggleResultadoPesquisa(status=null) {
    const container = document.getElementById('result-pesquisa');
    const iconeClose = document.getElementById('icone_pesquisa_close');
    const iconeOpen = document.getElementById('icone_pesquisa_open');

   
    if (status !== null) {
        // Se o status for fornecido, definir a visibilidade com base no status
        if (status) {
            container.classList.remove('d-none');
            iconeClose.classList.add('d-none');
            iconeOpen.classList.remove('d-none');
        } else {
            container.classList.add('d-none');
            iconeClose.classList.remove('d-none');
            iconeOpen.classList.add('d-none');
        }
    } else {
        if (container.classList.contains("d-none")) {
            container.classList.remove('d-none');
            iconeClose.classList.add('d-none');
            iconeOpen.classList.remove('d-none');
        } else {
            container.classList.add('d-none');
            iconeClose.classList.remove('d-none');
            iconeOpen.classList.add('d-none');
        }
    }
}
 // Função para montar o container de informações
 function montarInfoCliente(data) {
    // Atualizar os valores dos campos com os dados fornecidos
    document.getElementById("info_nome_cliente").textContent = data.nome;
    document.getElementById("info_telefone_cliente").textContent = data.telefone;
    document.getElementById("info_tipo_cliente").textContent = data.tipo_cliente;
    document.getElementById("info_descricao_cliente").textContent = data.descricao;
    document.getElementById("info_codigo_postal").textContent = data.codigo_postal;
    document.getElementById("info_rua").textContent = data.rua;
    document.getElementById("info_numero").textContent = data.numero;
    document.getElementById("info_bairro").textContent = data.bairro;
    document.getElementById("info_cidade").textContent = data.cidade;
    document.getElementById("info_estado").textContent = data.estado;
    document.getElementById("info_descricao_endereco").textContent = data.descricao_endereco;
    document.getElementById("id_cliente").textContent = data.id_cliente;
    // Verificar se há informações da última venda
    if (data.ultima_venda) {
        // Atualizar os valores das informações da última venda
        document.getElementById("info_ultima_venda_descricao").textContent = data.ultima_venda.descricao || "N/A";
        document.getElementById("info_ultima_venda_data_venda").textContent = data.ultima_venda.data_venda || "N/A";
        document.getElementById("info_ultima_venda_forma_pagamento").textContent = data.ultima_venda.forma_pagamento || "N/A";
        document.getElementById("info_ultima_venda_valor_total").textContent = data.ultima_venda.valor_total || "N/A";
        document.getElementById("info_ultima_venda_produtos").textContent = data.ultima_venda.produtos ? data.ultima_venda.produtos.join(", ") : "N/A";
    } else {
        // Ocultar a seção de informações da última venda se não houver dados
        document.getElementById("info_ultima_venda_descricao").textContent = "N/A";
        document.getElementById("info_ultima_venda_data_venda").textContent = "N/A";
        document.getElementById("info_ultima_venda_forma_pagamento").textContent = "N/A";
        document.getElementById("info_ultima_venda_valor_total").textContent = "N/A";
        document.getElementById("info_ultima_venda_produtos").textContent = "N/A";
    }
    
    toggleResultadoPesquisa(false);
    alertCustomer(`Cliente selecionado: ${data.nome}`);
    // Exibir o container de informações
    document.getElementById("info_cliente").classList.remove("d-none");
}



// Chamada inicial para buscar as lojas quando a página carrega
window.addEventListener('load', function() {
    buscarLojas();
});

function buscarLojas() {
    const url = '/buscar_lojas/';  // URL para buscar as lojas
    const type = 'GET';  // Tipo de requisição é GET
    const callback = function(data) {
        if (data.success) {
            // Se a chamada for bem-sucedida, atualize o dropdown com as lojas
            atualizarDropdownLojas(data.list_lojas);
        } else {
            console.error('Erro ao buscar lojas:', data.error);
            // Trate o erro conforme necessário
        }
    };

    // Chamar a função Python para buscar as lojas
    chamarFuncaoPython(url, null, type, callback);
}

// Função para atualizar o dropdown com as lojas
function atualizarDropdownLojas(list_lojas) {
    const dropdown = document.getElementById('id_loja');  // Obtém o dropdown de lojas

    // Limpa as opções existentes
    dropdown.innerHTML = '';

    // Adiciona a opção padrão
    const optionDefault = document.createElement('option');
    optionDefault.value = '0';
    optionDefault.textContent = 'Selecione';
    dropdown.appendChild(optionDefault);

    // Adiciona as opções de lojas
    list_lojas.forEach(function(loja) {
        const option = document.createElement('option');
        option.value = loja.id;
        option.textContent = loja.nome_loja;
        dropdown.appendChild(option);
    });
}
// Função para carregar e manipular a lista de clientes
function carregarListaClientes() {
    // Verifica se já temos os clientes em cache
        // Carrega a função manageLoading para mostrar o indicador de carregamento
        manageLoading(true, "select_cliente");
        alertCustomer('Atualizando Lista de clientes');
        // Chama a função para obter os clientes por empresa
        const url = '/api/cliente/by_empresa/';
        chamarFuncaoPython(url, null, 'GET', function(response) {
            if (response.success == true) {
                clientesCache = response.clientes;
                manipularPesquisaClientes(clientesCache);   
                manageLoading(false, "select_cliente");

            } else {
                alertCustomer(response.message);
            manageLoading(false, "select_cliente");
            }
        });  
         
}
function toggleGestaoEntrega() {
    var container = document.getElementById("container_gestao_entrega");
    var iconeOpen = document.getElementById("icone_entrega_open");
    var iconeClose = document.getElementById("icone_entrega_close");

    if (container.classList.contains("d-none")) {
        listarMotoboys();
        // Se o container estiver oculto, mostrá-lo e trocar os ícones
        container.classList.remove("d-none");
        iconeOpen.classList.remove("d-none");
        iconeClose.classList.add("d-none");
    } else {
        // Se o container estiver visível, ocultá-lo e trocar os ícones
        container.classList.add("d-none");
        iconeOpen.classList.add("d-none");
        iconeClose.classList.remove("d-none");
    }
}
function toggleMotoboyFields() {
    var selectMotoboy = document.getElementById("select_motoboy");
    var cadastrarMotoboy = document.getElementById("cadastrar_motoboy");
    var btnCadastrarBoy = document.getElementById("btnCadastrarBoy");
    var container = document.getElementById("container_gestao_entrega");
    var iconeOpen = document.getElementById("icone_entrega_open");
    var iconeClose = document.getElementById("icone_entrega_close");

    if (selectMotoboy.classList.contains("d-none")) {
    // Se estiver oculto, mostra o campo de seleção de motoboy e oculta o campo de cadastro
        selectMotoboy.classList.remove("d-none");
        cadastrarMotoboy.classList.add("d-none");
        // Altera o texto do botão para "Cadastrar Motoboy" e adiciona um ícone adequado 
        btnCadastrarBoy.innerHTML = '<i class="bi bi-person-plus"></i>';
        listarMotoboys();
    } else {
    // Se estiver visível, mostra o campo de cadastro e oculta o campo de seleção de motoboy
        selectMotoboy.classList.add("d-none");
        cadastrarMotoboy.classList.remove("d-none");
        // Altera o conteúdo do botão para o ícone "arrow-return-left"
        btnCadastrarBoy.innerHTML = '<i class="bi bi-arrow-return-left"></i>';
    }
    if (container.classList.contains("d-none")) {
    // Se o container estiver oculto, mostrá-lo e trocar os ícones
        container.classList.remove("d-none");
        iconeOpen.classList.remove("d-none");
        iconeClose.classList.add("d-none");
    }
}
function toggleGestaproduto() {
    var container = document.getElementById("body_gestao_pay");
    var iconeOpen = document.getElementById("icone_pagamento_open");
    var iconeClose = document.getElementById("icone_pagamento_close");

    if (container.classList.contains("d-none")) {
        // Se o container estiver oculto, mostrá-lo e trocar os ícones
        container.classList.remove("d-none");
        iconeOpen.classList.remove("d-none");
        iconeClose.classList.add("d-none");
    } else {
        // Se o container estiver visível, ocultá-lo e trocar os ícones
        container.classList.add("d-none");
        iconeOpen.classList.add("d-none");
        iconeClose.classList.remove("d-none");
    }
}

function insertMotoboy() {
    var nomeMotoboy = document.getElementById('nome_motoboy').value.trim();
    var telefoneMotoboy = document.getElementById('telefone_motoboy').value.trim();
    manageLoading(true,"cadastrar_motoboy"); 
    // Validar se os campos não estão vazios
    if (nomeMotoboy === '') {
        alertCustomer('insira o nome do motoboy.');
        return;
    }
    if (telefoneMotoboy === '') {
        alertCustomer('insira o telefone do motoboy.');
        return;
    }


// Chamar a função para criar um motoboy, passando o objeto de dados como parâmetro
createMotoboy(nomeMotoboy, telefoneMotoboy)
    .then(result => {
        if (result.success) {
            // Limpar os campos após a criação bem-sucedida
            document.getElementById('nome_motoboy').value = '';
            document.getElementById('telefone_motoboy').value = '';
        }
        manageLoading(false,"cadastrar_motoboy");
        toggleMotoboyFields()
    })
    .catch(error => {
        alertCustomer('Ocorreu um erro ao criar o motoboy: ' + error.message);
        // Habilitar o contêiner e remover o indicador de carregamento em caso de erro
        container.classList.remove('disabled');
    });
}


// Defina sua função de verificação
function verificarAntesDoSubmit() {

   // Verifica se uma loja foi selecionada
    if (document.getElementById('id_loja').value == "0") {
        alertCustomer('selecione uma loja antes de enviar o formulário.');
        return false;  
    }
    // Verifica se há itens no carrinho
    if (!atualizarCamposCarrinho()) {
        alertCustomer('Não foram adicionados itens ao formulário. adicione itens ao carrinho antes de enviar.');
        return false;
    }
    // Verifica se o método de entrega foi selecionado
    var metodoEntrega = document.getElementById('id_metodo_entrega').value;
    if (metodoEntrega == "0") {
        alertCustomer('selecione um método de entrega antes de enviar o formulário.');
        return false;  
    } 
    // Se o método de entrega for "entrega_no_local", verifica se foi inserido um valor no campo de taxa de entrega
    else if (metodoEntrega == "entrega_no_local") {
        var taxaEntrega = document.getElementById('txt_taxa_entrega').value;
        if (taxaEntrega.trim() === '') {
            alertCustomer('informe a taxa de entrega antes de enviar o formulário.');
            return false;
        }
    }

    // Verifica se a forma de pagamento foi selecionada
    if (document.getElementById('id_forma_pagamento').value == "0") {
        alertCustomer('selecione uma forma de pagamento antes de enviar o formulário.');
        return false;  
    } 
    // Verifica se o estado da transação foi selecionado
    if (document.getElementById('id_estado_transacao').value == "0") {
        alertCustomer('selecione um estado de transação antes de enviar o formulário.');
        return false;  
    }
    return true; // Permite o envio do formulário
}
function enviarDadosVenda() {
    manageLoading(true,"form_cadastro"); 
    $.ajax({
        url: 'insert_venda_ajax/',
        type: 'POST',
        data: $('#form_cadastro').serialize(),
        success: function(response) {
            console.log(response); // Exibe a resposta no console do navegador
            if (response.success) {
                alertCustomer(response.success);
            } else {
                alertCustomer(response.error);
            }
            manageLoading(false,"form_cadastro"); 
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.responseText); // Exibe o erro no console do navegador
            alert("Ocorreu um erro ao processar a venda. Por favor, tente novamente mais tarde.");
         manageLoading(false,"form_cadastro"); 
        }
    });
} 
document.getElementById("btnSubmit").addEventListener("click", function(event) {
    // Chama a função de verificação antes de permitir o envio do formulário
    if (!verificarAntesDoSubmit()) {
        event.preventDefault(); // Impede o envio do formulário se a verificação falhar
    } else {
        enviarDadosVenda();
    }
});
// Função para atualizar o campo oculto com os itens do carrinho
function atualizarCamposCarrinho() {
    var listaProdutos = document.getElementById('listaProdutos');
    var itensCarrinho = [];

// Percorrer os itens da lista de produtos
    var itensLista = listaProdutos.querySelectorAll('li');

    // Verificar se há itens na lista de produtos
    if (itensLista.length === 0) {
         return false; // Retorna false se não houver itens
    }

itensLista.forEach(function(item) {
    var idProduto = item.getAttribute('data-id-produto');
    var quantidade = parseInt(item.querySelector(".quantidade").textContent);
    // Concatenar o ID do produto e a quantidade com |
    var valorInput = idProduto + '|' + quantidade;
    // Criar um input oculto para cada item do carrinho
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'item_carrinho';
    input.value = valorInput;
    document.getElementById('form_cadastro').appendChild(input);
    });

    return true; // Retorna true se os itens foram adicionados com sucesso
}

    document.getElementById('id_metodo_entrega').addEventListener('change', function() {
        var selectedOption = this.options[this.selectedIndex];
        var selectedValue = selectedOption.value;

        if (selectedValue === "retirado_na_loja") {
            document.getElementById("id_estado_transacao").value = "finalizado";
        }

        if (selectedValue === "entrega_no_local") {
            document.getElementById("id_estado_transacao").value = "processando";
            toggleGestaoEntrega();
        }
    }); 
 

    document.getElementById('id_loja').addEventListener('change', function() {
        var selectedLoja = this.value;
        var produtosList = document.getElementById('produtosList');
        produtosList.innerHTML = ''; // Limpar os produtos existentes
        // Adicionar produtos relevantes ao datalist
        produtosArray.forEach(function(produto) {
            if (selectedLoja === '0' || produto.idLoja === selectedLoja) {
                var option = document.createElement('option');
                option.dataset.idProduto = produto.idProduto;
                option.value = produto.nome;
                produtosList.appendChild(option); 
                produtoInput.setAttribute('list', 'produtosList');
            }
        });
    });


    function calcularValorTotal() {
        var itensLista = listaProdutos.querySelectorAll(".list-group-item");
        var valorTotal = 0;
        // Itera sobre os itens da lista e calcula o valor total
            itensLista.forEach(function (item) {
                var quantidade = parseInt(item.querySelector(".quantidade").textContent);
                var idProduto = item.getAttribute("data-id-produto");
                    produtosArray.forEach(function(produto) {
                            if(produto.idProduto == idProduto){
                                var valorUnitario = parseFloat(produto.valor);
                                valorTotal += quantidade * valorUnitario;
                            }
                    });
            });
            // Define o valor total no label, formatando-o com vírgula e duas casas decimais
            var labelValorTotal = document.getElementById("id_valor_total");

            if (labelValorTotal) {
                labelValorTotal.textContent = valorTotal.toLocaleString('pt-BR', {minimumFractionDigits: 2});
            }  
            calcularTroco();

    }
 
    function calcularTroco() {
        // Obtém o valor total removendo a formatação
        var valorTotalInput = document.getElementById('id_valor_total');
        var valorTotalText = valorTotalInput ? valorTotalInput.textContent.trim() : '';
        // Remove a formatação (vírgulas) do valor total
        var valorTotal = parseFloat(valorTotalText.replace(',', '.')) || 0;
    
        // Repita o mesmo processo para a taxa de entrega e o desconto, se aplicável
        var taxaEntregaInput = document.getElementById('txt_taxa_entrega');
        var taxaEntregaText = taxaEntregaInput ? taxaEntregaInput.value.trim() : '';
        var taxaEntrega = parseFloat(taxaEntregaText.replace(',', '.')) || 0;
    
        var descontoInput = document.getElementById('txt_desconto');
        var descontoText = descontoInput ? descontoInput.value.trim() : '';
        var desconto = parseFloat(descontoText.replace(',', '.')) || 0;
    
        // Calcula o valor total considerando a taxa de entrega e o desconto
        var valorTotalComTaxaDesconto = valorTotal + taxaEntrega - desconto;
    
        // Define o valor total a ser pago no campo id_valor_total
        document.getElementById('id_valor_apagar').textContent = valorTotalComTaxaDesconto.toFixed(2).replace('.', ',');
        document.getElementById('total_apagar').value = valorTotalComTaxaDesconto.toFixed(2).replace('.', ',');
    
        // Obtém o valor pago
        var valorPagoInput = document.getElementById('id_valor_pago');
        var valorPago = valorPagoInput ? parseFloat(valorPagoInput.value) : 0;
    
        // Calcula o troco apenas se o valor pago for maior ou igual ao total
        var troco = valorPago - valorTotalComTaxaDesconto;
        document.getElementById('troco').value =troco
    
            // Exibe a mensagem dependendo do resultado
        if (valorPago < valorTotalComTaxaDesconto) {
            // Calcula o valor que está faltando para cobrir o total da compra
            var valorFaltante = valorTotalComTaxaDesconto - valorPago;
            // Exibe a mensagem informando o valor faltante
            $('#id_troco').text('Está Faltando: R$ ' + valorFaltante.toFixed(2).replace('.', ',')).css('color', 'red');
        } else {
            $('#id_troco').text('Troco a ser dado é: R$ ' + troco.toFixed(2).replace('.', ',')).css('color', 'green');
        }
    }
    
function aumentarQuantidade(elemento) {
    // Encontra o elemento pai do elemento atual
    var pai = elemento.closest(".list-group-item");
    // Obtém o ID do produto do atributo data-id-produto do elemento pai
    var idProduto = pai.getAttribute("data-id-produto");

    produtosArray.forEach(function(produto) {
        if(produto.idProduto == idProduto) {
            var quantidadeSpan = pai.querySelector(".quantidade");
            var quantidadeAtual = parseInt(quantidadeSpan.textContent);
                if(produto.quantidade >= quantidadeAtual) {
                    quantidadeSpan.textContent = quantidadeAtual + 1;
                    calcularValorTotal();
                } else {
                    alertCustomer("Não há mais produto disponível no estoque.");
                }
        }
    });
}

function diminuirQuantidade(elemento) {
    var quantidadeSpan = elemento.parentElement.querySelector(".quantidade");
    var quantidadeAtual = parseInt(quantidadeSpan.textContent);
    if (quantidadeAtual > 1) {
        quantidadeSpan.textContent = quantidadeAtual - 1;
    } else {
         elemento.parentElement.remove();
    }
    calcularValorTotal();
}

function toggleGestaoRetornavel( status ) {
    var container = document.getElementById("body_gestaoRetornavel");
    var iconeOpen = document.getElementById("icone_produto_open");
    var iconeClose = document.getElementById("icone_produto_close");
    var iconeBloqueado = document.getElementById("iconeBloqueado");
    var iconeDesbloqueado = document.getElementById("iconeDesbloqueado");
    botao = document.getElementById("btn_gestao_retornaveis");

        if (status ) {
            botao.setAttribute("onclick", "toggleGestaoRetornavel(false);");
            container.classList.remove("d-none");
            iconeOpen.classList.remove("d-none");
            iconeClose.classList.add("d-none");
            iconeBloqueado.classList.add("d-none");
            iconeDesbloqueado.classList.remove("d-none");
        } else {
            botao.setAttribute("onclick", "toggleGestaoRetornavel(true);");
            container.classList.add("d-none");
            iconeOpen.classList.add("d-none");
            iconeClose.classList.remove("d-none");

            iconeBloqueado.classList.remove("d-none");
            iconeDesbloqueado.classList.add("d-none");
        }
}

document.addEventListener("DOMContentLoaded", function () {




    // Adiciona ouvintes de evento de entrada aos campos relevantes
    document.getElementById('txt_taxa_entrega').addEventListener('input', calcularTroco);
    document.getElementById('txt_desconto').addEventListener('input', calcularTroco);
    document.getElementById('id_valor_pago').addEventListener('input', calcularTroco);
 
    var selectElement = document.getElementById("id_forma_pagamento");
    var containerElement = document.querySelector(".gestaotroco");

    selectElement.addEventListener("change", function () {
        var selectedOption = this.options[this.selectedIndex];
        var selectedValue = selectedOption.value;

            if (selectedValue === "dinheiro") {
                containerElement.classList.remove("d-none"); // Remove a classe que oculta o container
            } else {
                containerElement.classList.add("d-none"); // Adiciona a classe que oculta o container
            }
    }); 
     



const buttons = document.querySelectorAll('[data-bs-target]');
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const target = button.getAttribute('data-bs-target');
        const targetElement = document.querySelector(target);
        const otherTargets = document.querySelectorAll('.collapse');
        otherTargets.forEach(otherTarget => {
            if (otherTarget !== targetElement && otherTarget.classList.contains('show')) {
                const otherCollapse = new bootstrap.Collapse(otherTarget);
                otherCollapse.hide();
            }
        });
        if (!targetElement.classList.contains('show')) {
            const collapse = new bootstrap.Collapse(targetElement);
            collapse.show();
        }
    });
});

    var produtosList = document.getElementById('produtosList');
    produtosArray.forEach(function(produto) {
        var option = document.createElement('option');
        option.dataset.idProduto = produto.idProduto;
        option.value = produto.nome;
        produtosList.appendChild(option);
    });
    // Obtém o input do produto
    var produtoInput = document.getElementById("produtoInput");
        // Adiciona evento de entrada para detectar a seleção de uma opção
        produtoInput.addEventListener("input", function() {
        var selectedOption = document.querySelector("#produtosList option[value='" + this.value + "']");
        if (selectedOption) {
            OptionSelection(selectedOption);
        }
    });

     // Função para lidar com a seleção de opção
    function  OptionSelection(option) {
    var produtoId = option.getAttribute("data-id-produto");
        produtoInput.dataset.idProduto = produtoId;
    } 
    var adicionarBtn = document.getElementById("adicionarProdutoBtn");
     
    var listaProdutos = document.getElementById("listaProdutos");
    // Função para calcular o valor total e atualizar o label

        adicionarBtn.addEventListener("click", function () {
            var produtoInput = document.getElementById("produtoInput");
            var produtoSelecionado = null;
            var produtoId = produtoInput.getAttribute("data-id-produto");
            produtosArray.forEach(function(produto) {
                if (produto.idProduto == produtoId) {
                    produtoSelecionado = produto;
                    // Aqui você pode realizar outras operações relacionadas ao produto selecionado, se necessário
                }       
            });

                if (produtoInput.value !== "") {
                    var itensLista = listaProdutos.querySelectorAll(".list-group-item");
                    var produtoExistente = false;
                    
                    // Verifica se o produto já está na lista
                    itensLista.forEach(function (item) {
                        var idExistente = item.getAttribute("data-id-produto");
                        if (idExistente === produtoId) {
                            // Se já existir, aumenta a quantidade
                            var quantidadeSpan = item.querySelector(".quantidade");
                            var quantidadeAtual = parseInt(quantidadeSpan.textContent);
                            quantidadeSpan.textContent = quantidadeAtual + 1;
                            produtoExistente = true;
                        }
                    });
                    if (!produtoExistente) {
                        // Se o produto não existir na lista, cria um novo item
                        var novoItemLista = document.createElement("li");
                        novoItemLista.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
                        novoItemLista.setAttribute("data-id-produto", produtoSelecionado.idProduto);
                        novoItemLista.setAttribute("data-retornavel", produtoSelecionado.isRetornavel); 
                        novoItemLista.setAttribute("data-valor", produtoSelecionado.valor);
                        novoItemLista.innerHTML = `
                            <span class="badge text-bg-primary me-1 rounded-pill quantidade">1</span>
                            <span class="" >${produtoSelecionado.nome} R$ ${produtoSelecionado.valor} Unid</span>

                            <span class="btn btn-sm btn-outline-primary bi-plus ms-auto" data-id-produto="${produtoSelecionado.idProduto}" onclick="aumentarQuantidade(this)"></span>
                            <span class="btn btn-sm btn-outline-danger bi-dash ms-1" onclick="diminuirQuantidade(this)"></span>
                        `;
                        listaProdutos.appendChild(novoItemLista);
                    }
                    calcularValorTotal();
                    produtoInput.value =""
            }
    });
    // Função para verificar os produtos retornáveis
    function verificarRetornaveis() {
        var itensLista = listaProdutos.querySelectorAll(".list-group-item");
        var numeroGaloes = 0;
        // Verifica se há algum item retornado na lista e conta o número de galões saindo
        for (var item of itensLista) {
            var isRetornavel = item.dataset.retornavel === "True";
        
            if (isRetornavel) {
                numeroGaloes += parseInt(item.querySelector(".quantidade").textContent);
            }
        }

        // Alterna a visibilidade do corpo do acordeão e dos ícones com base na presença de itens retornáveis
        if (numeroGaloes > 0) {
            gerarInputs(numeroGaloes);
            toggleGestaoRetornavel(true);
        } else { 
            toggleGestaoRetornavel(false);
        }
    }

    // Função para gerar os inputs dinamicamente com base no número de galões que estão saindo
    function gerarInputs(numeroGaloes) {
        var formGestaoGalao = document.getElementById("form_galaoGestao");
        

        // Limpa os formulários de entrada e saída
        formGestaoGalao.innerHTML = '';
        formGestaoGalao.innerHTML = '';

    // Adiciona inputs para os galões que estão entrando e saindo
            for (var i = 0; i < numeroGaloes; i++) {
                // Inputs para os galões que estão entrando
                formGestaoGalao.innerHTML += `
                    <div class=" border-dark border rounded bg-success p-3 m-0 text-dark bg-opacity-25 mb-1">
                    <div class="row ">
                        <label class="form-label" style="font-size: 1.rem">Galão que está entrando ${i+1}.</label>
                        <div class="col mx-1 p-0">
                            <div class="form-floating mb-2">
                                <input type="text" id="data_validade_entrada_${i}" name="data_validade_entrada_${i}" class="form-control data-validade data-mes-ano-mask">
                                <label for="data_validade_entrada_${i}" style="font-size: 0.7rem" class="form-label">Data de Validade: <span style="font-size: 0.6rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                        <div class="col mx-1 p-0">
                            <div class="form-floating mb-2">
                                <input type="text" id="data_fabricacao_entrada_${i}" name="data_fabricacao_entrada_${i}" class="form-control data-fabricacao data-mes-ano-mask">
                                <label for="data_fabricacao_entrada_${i}" style="font-size: 0.7rem" class="form-label">Data de Fabricação: <span style="font-size: 0.6rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                    </div>
                        <div class="form-floating mb-2">
                            <select id="tipo_entrada_${i}" name="tipo_entrada_${i}" class="form-select">
                                <option value="1">Galão 20 Litros</option>
                                <option value="2">Galão 10 Litros</option>
                                <option value="3">outro</option>
                            </select>
                            <label for="tipo_entrada_${i}" style="font-size: 0.7rem" class="form-label">Tipo de entrada:</label>
                        </div> 
                        </div> `;

                // Inputs para os galões que estão saindo
                formGestaoGalao.innerHTML += `
                    <div class=" border-dark border rounded bg-danger p-3 m-0 text-dark bg-opacity-25 mb-2">
                    <div class="row">
                        <label class="form-label" style="font-size: 1.rem">Galão que está saindo ${i+1}.</label>
                        <div class="col mx-1 p-0">
                            <div class="form-floating mb-2">
                                <input type="text" id="data_validade_saida_${i}" name="data_validade_saida_${i}" class="form-control data-validade data-mes-ano-mask">
                                <label for="data_validade_saida_${i}" style="font-size: 0.7rem" class="form-label">Data de Validade: <span style="font-size: 0.6rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                        <div class="col mx-1 p-0">
                            <div class="form-floating mb-2">
                                <input type="text" id="data_fabricacao_saida_${i}" name="data_fabricacao_saida_${i}" class="form-control data-fabricacao data-mes-ano-mask">
                                <label for="data_fabricacao_saida_${i}" style="font-size: 0.7rem" class="form-label">Data de Fabricação: <span style="font-size: 0.6rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                    </div>
                    <div class="form-floating mb-2">
                        <select id="tipo_saida_${i}" name="tipo_saida_${i}" class="form-select">
                            <option value="Galão 20 Litros">Galão 20 Litros</option>
                            <option value="Galão 10 Litros">Galão 10 Litros</option>
                            <option value="Outro">outro</option>
                        </select>
                        <label for="tipo_saida_${i}" style="font-size: 0.7rem" class="form-label">Tipo de saída:</label>
                    </div>
                    <div class="form-floating mb-2">
                        <input type="text" id="id_descricao_gestão_galao${i}" name="id_descricao_gestão_galao" class="form-control  ">
                        <label for="id_descricao_gestão_galao${i}" style="font-size: 0.7rem" class="form-label">Descricao: <span style="font-size: 0.6rem;">(opicional)</span></label>
                    </div>
                    </div>
                   
                    `;
            }
        }

            // Opções para o observador de mutação
            var observerOptions = {
                childList: true, // Observar mudanças nos filhos do elemento
                subtree: true // Observar todos os descendentes do elemento
            };

        // Função de callback para o observador de mutação
        var observerCallback = function(mutationsList, observer) {
            for (var mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    verificarRetornaveis();
                    $('.data-mes-ano-mask').mask('00/0000');
                        document.querySelectorAll(".data-validade").forEach(function(input) {
                            input.addEventListener("input", function() {
                                // Limpa qualquer timeout existente
                                clearTimeout(input.timeoutId);
                                
                                // Configura um novo timeout para esperar que o usuário pare de digitar
                                input.timeoutId = setTimeout(function() {
                                    // Obtém o valor do campo data_validade
                                    var dataValidade = input.value.trim();
                                    
                                    // Verifica se a entrada está vazia
                                    if (dataValidade === "") {
                                        return; // Não faz nada se estiver vazio
                                    }
                                    
                                    // Verifica se a entrada possui o formato esperado (MM/AAAA)
                                    var regex = /^(0[1-9]|1[0-2])\/\d{4}$/;
                                    if (!regex.test(dataValidade)) {
                                      
                                        return; // Não faz nada se o formato for inválido
                                    }
                                    
                                    // Extrai o mês e o ano da entrada
                                    var partes = dataValidade.split("/");
                                    var mes = parseInt(partes[0], 10);
                                    var ano = parseInt(partes[1], 10);
                                    
                                    // Calcula a data de fabricação subtraindo três anos da data de validade
                                    var dataFabricacao = ("0" + mes).slice(-2) + "/" + (ano - 3);
                                
                                    
                                    // Encontra o campo de entrada data_fabricacao correspondente
                                    var dataFabricacaoField = input.closest('.row').querySelector(".data-fabricacao");
                                    
                                    // Define o valor do campo data_fabricacao se encontrado
                                    if (dataFabricacaoField) {
                                        dataFabricacaoField.value = dataFabricacao;
                                    }
                                }, 500); // Aguarda 500ms após a última entrada antes de executar o cálculo
                            });
                        });
                            
                    break;
                }
            }
        };

        // Elemento alvo para observar as mutações
        var listaProdutos = document.getElementById("listaProdutos");

        // Cria um observador de mutação
        var observer = new MutationObserver(observerCallback);

        // Inicia a observação do elemento alvo
        observer.observe(listaProdutos, observerOptions);

        // Verifica os produtos retornáveis ao carregar a página
        verificarRetornaveis();
    });
