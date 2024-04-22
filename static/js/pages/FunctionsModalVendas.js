
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
            montarInfoCliente(response.data,"info_cliente");
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
                montarInfoCliente(cliente,"info_cliente"); 
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
}// Função para montar o container de informações
function montarInfoCliente(data, id_container) {
    var container = document.getElementById(id_container);
    // Atualizar os valores dos campos com os dados fornecidos
    container.querySelector("#info_nome_cliente").textContent = data.nome;
    container.querySelector("#info_telefone_cliente").textContent = data.telefone;
    container.querySelector("#info_tipo_cliente").textContent = data.tipo_cliente;
    container.querySelector("#info_descricao_cliente").textContent = data.descricao;
    container.querySelector("#info_codigo_postal").textContent = data.codigo_postal;
    container.querySelector("#info_rua").textContent = data.rua;
    container.querySelector("#info_numero").textContent = data.numero;
    container.querySelector("#info_bairro").textContent = data.bairro;
    container.querySelector("#info_cidade").textContent = data.cidade;
    container.querySelector("#info_estado").textContent = data.estado;
    container.querySelector("#info_descricao_endereco").textContent = data.descricao_endereco;
    // Verificar se há informações da última venda
    if (data.ultima_venda) {
        // Atualizar os valores das informações da última venda
        container.querySelector("#info_ultima_venda_descricao").textContent = data.ultima_venda.descricao || "N/A";
        container.querySelector("#info_ultima_venda_data_venda").textContent = data.ultima_venda.data_venda || "N/A";
        container.querySelector("#info_ultima_venda_forma_pagamento").textContent = data.ultima_venda.forma_pagamento || "N/A";
        container.querySelector("#info_ultima_venda_valor_total").textContent = data.ultima_venda.valor_total || "N/A";
        container.querySelector("#info_ultima_venda_produtos").textContent = data.ultima_venda.produtos ? data.ultima_venda.produtos.join(", ") : "N/A";
    }  
    
    toggleResultadoPesquisa(false);
    alertCustomer(`Cliente selecionado: ${data.nome}`);
    // Exibir o container de informações
    container.classList.remove("d-none");
}
 

// Função para atualizar o dropdown com as lojas
function atualizarDropdownLojas(list_lojas) {
    const dropdown = document.getElementById('id_loja');  // Obtém o dropdown de lojas

    // Limpa as opções existentes
    dropdown.innerHTML = '';

    // Adiciona a opção padrão
    if(list_lojas.length > 1){
        const optionDefault = document.createElement('option');
        optionDefault.value = '0';
        optionDefault.textContent = 'Selecione';
        dropdown.appendChild(optionDefault);
    }

    // Adiciona as opções de lojas
    list_lojas.forEach(function(loja) {
        const option = document.createElement('option');
        option.value = loja.id_loja;
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
        url: '/vendas/criar/insert_venda_ajax/',
        type: 'POST',
        data: $('#form_cadastro').serialize(),
        success: function(response) {
            console.log(response); // Exibe a resposta no console do navegador
            if (response.success===true) {
                alertCustomer(response.message);
                close_modal();
                get_data();

            } else {
                alertCustomer(response.error);
            }
            manageLoading(false,"form_cadastro"); 
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.responseText); // Exibe o erro no console do navegador
            alertCustomer("Ocorreu um erro ao processar a venda. Por favor, tente novamente mais tarde.");
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
function atualizarCamposCarrinho() {
    var itensLista = document.querySelectorAll('.item-list-carrinho');
    var itensCarrinho = [];

    // Verificar se há itens na lista de produtos
    if (itensLista.length === 0) {
        return false; // Retorna false se não houver itens
    }

    // Seleciona todos os inputs com o atributo name igual a 'item_carrinho'
    var inputsCarrinho = document.querySelectorAll('input[name="item_carrinho"]');

    // Verifica se há inputs encontrados
    if (inputsCarrinho.length > 0) {
        // Itera sobre cada input encontrado
        inputsCarrinho.forEach(function(input) {
            // Remove o input
            input.remove();
        });
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
        var selectedLoja = parseInt(this.value); 
        var produtosList = document.getElementById('produtosList');
        produtosList.innerHTML = ''; // Limpar os produtos existentes
        // Adicionar produtos relevantes ao datalist
        produtosArray.forEach(function(produto) {
            if (selectedLoja === '0' || produto.loja_id === selectedLoja) {
                var option = document.createElement('option');
                option.dataset.idProduto = produto.id_produto;
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
                            if(produto.id_produto == idProduto){
                                var valorUnitario = parseFloat(produto.preco_venda);
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
        document.getElementById('troco').value =troco;
    
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
        if(produto.id_produto == idProduto) {
            var quantidadeSpan = pai.querySelector(".quantidade");
            var quantidadeAtual = parseInt(quantidadeSpan.textContent);
                if(produto.quantidade_atual_estoque >= quantidadeAtual) {
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

 function FormModalVendas() {


    // Chamar a função para preencher a tabela ao carregar a página
    produtosArray = Utils.getLocalStorageItem('data_produtos');

    lojas_data = Utils.getLocalStorageItem('data_lojas');
    atualizarDropdownLojas(lojas_data);
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
     // Obtém a lista de produtos do DOM e itera sobre cada produto

// Chamar a função para preencher a tabela ao carregar a página 
var produtosList = document.getElementById('produtosList');
    produtosArray.forEach(function(produto) {
        // Cria uma nova opção para cada produto e a adiciona à lista de produtos
        var option = document.createElement('option');
        option.dataset.idProduto = produto.id_produto; // Define o atributo de dados 'idProduto' na opção
        option.value = produto.nome; // Define o valor da opção como o nome do produto
        produtosList.appendChild(option);
    });

// Obtém o input do produto
var produtoInput = document.getElementById("produtoInput");
// Adiciona um evento de entrada para detectar a seleção de uma opção
produtoInput.addEventListener("input", function() {
    // Obtém a opção selecionada com base no valor do input do produto
    var selectedOption = document.querySelector("#produtosList option[value='" + this.value + "']");
    if (selectedOption) {
        // Chama a função OptionSelection passando a opção selecionada como argumento
        OptionSelection(selectedOption);
    }
});

// Função para lidar com a seleção de opção
function OptionSelection(option) {
    // Obtém o ID do produto da opção selecionada e define o atributo de dados 'idProduto' no input do produto
    var produtoId = option.getAttribute("data-id-produto");
    produtoInput.dataset.idProduto = produtoId;
}

// Obtém o botão de adicionar produto do DOM
var adicionarBtn = document.getElementById("adicionarProdutoBtn");

// Obtém a lista de produtos do DOM
var listaProdutos = document.getElementById("listaProdutos");

// Adiciona um ouvinte de evento para calcular o valor total e atualizar o label quando o botão de adicionar produto é clicado
adicionarBtn.addEventListener("click", function () {
    // Obtém o input do produto
    var produtoInput = document.getElementById("produtoInput");
    var produtoSelecionado = null;
    var produtoId = produtoInput.getAttribute("data-id-produto");
    // Itera sobre a lista de produtos para encontrar o produto selecionado
   // Variável de controle para indicar se o loop deve continuar ou parar
    let continuarLoop = true;

    // Iterar sobre a lista de produtos
    produtosArray.forEach(function(produto) {
        // Verificar se o loop deve continuar
        if (!continuarLoop) {
            return; // Se não, saia do loop
        }

        // Verificar as condições do produto
        if (produtoInput.value == "") {
            alertCustomer("Selecione um produto da lista de sugestões..");
            continuarLoop = false; // Definir para false para parar o loop
            return;
        }

        if (produto.id_produto == produtoId) {
            if (produto.quantidade_atual_estoque >= 1) {
                produtoInput.value = "";
                produtoSelecionado = produto;
            } else {
                produtoInput.value = "";
                alertCustomer("Não há mais produto disponível no estoque.");
            }
            continuarLoop = false; // Definir para false para parar o loop
            return;
        }
    });
    // Verifica se o valor do input do produto não está vazio
    if (produtoSelecionado != null) {
        var itensLista = listaProdutos.querySelectorAll(".list-group-item");
        var produtoExistente = false;
        
        // Itera sobre os itens da lista para verificar se o produto já está na lista
        itensLista.forEach(function (item) {
            var idExistente = item.getAttribute("data-id-produto");
            if (idExistente === produtoId) {
                // Se o produto já existir na lista, aumenta a quantidade
                var quantidadeSpan = item.querySelector(".quantidade");
                var quantidadeAtual = parseInt(quantidadeSpan.textContent);
                quantidadeSpan.textContent = quantidadeAtual + 1;
                produtoExistente = true;
            }
        });
        if (!produtoExistente) {
            // Se o produto não existir na lista, cria um novo item na lista de produtos
            var novoItemLista = document.createElement("li");
            novoItemLista.classList.add("list-group-item",'item-list-carrinho', "d-flex", "justify-content-between", "align-items-center");
            novoItemLista.setAttribute("data-id-produto", produtoSelecionado.id_produto);
            novoItemLista.setAttribute("data-retornavel", produtoSelecionado.is_retornavel); 
            novoItemLista.setAttribute("data-valor", produtoSelecionado.valor);
            // Preenche o HTML do novo item na lista de produtos
            novoItemLista.innerHTML = `
                <span class="badge text-bg-primary me-1 rounded-pill quantidade">1</span>
                <span class="text-small small " style="font-size: 0.8rem;" >${produtoSelecionado.nome} R$ ${produtoSelecionado.preco_venda} Unid</span>
                <span class="btn btn-sm btn-outline-primary bi-plus ms-auto" data-id-produto="${produtoSelecionado.id_produto}" onclick="aumentarQuantidade(this)"></span>
                <span class="btn btn-sm btn-outline-danger bi-dash ms-1" onclick="diminuirQuantidade(this)"></span>
            `;
            listaProdutos.appendChild(novoItemLista);
        }
        // Calcula o valor total dos produtos e atualiza o label
        calcularValorTotal();
        // Limpa o valor do input do produto
        produtoInput.value ="";
    }
});

    // Função para verificar os produtos retornáveis
    function verificarRetornaveis() {
        var itensLista = listaProdutos.querySelectorAll(".list-group-item");
        var numeroGaloes = 0;
        // Verifica se há algum item retornado na lista e conta o número de galões saindo
        for (var item of itensLista) {
            var isRetornavel = item.dataset.retornavel === "true";
        
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
                                <label for="data_validade_entrada_${i}" style="font-size: 0.6rem" class="form-label">Data de Validade: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                        <div class="col mx-1 p-0">
                            <div class="form-floating mb-2">
                                <input type="text" id="data_fabricacao_entrada_${i}" name="data_fabricacao_entrada_${i}" class="form-control data-fabricacao data-mes-ano-mask">
                                <label for="data_fabricacao_entrada_${i}" style="font-size: 0.6rem" class="form-label">Data de Fabricação: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                    </div>
                        <div class="form-floating mb-2">
                            <select id="tipo_entrada_${i}" name="tipo_entrada_${i}" class="form-select">
                                <option value="Não Selecionado" disabled>Selecione</option>
                                <option value="Galão 20 Litros">Galão 20 Litros</option>
                                <option value="Galão 10 Litros">Galão 10 Litros</option>
                                <option value="Galão 10 Litros">Galão 5 Litros</option>
                                <option value="outro">outro</option>
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
                                <label for="data_validade_saida_${i}" style="font-size: 0.6rem" class="form-label">Data de Validade: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                        <div class="col mx-1 p-0">
                            <div class="form-floating mb-2">
                                <input type="text" id="data_fabricacao_saida_${i}" name="data_fabricacao_saida_${i}" class="form-control data-fabricacao data-mes-ano-mask">
                                <label for="data_fabricacao_saida_${i}" style="font-size: 0.6rem" class="form-label">Data de Fabricação: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                            </div>
                        </div>
                    </div>
                    <div class="form-floating mb-2">
                        <select id="tipo_saida_${i}" name="tipo_saida_${i}" class="form-select">
                            <option value="Não Selecionado" disabled>Selecione</option>
                            <option value="Galão 20 Litros">Galão 20 Litros</option>
                            <option value="Galão 10 Litros">Galão 10 Litros</option>
                            <option value="Galão 10 Litros">Galão 5 Litros</option>
                            <option value="outro">outro</option>
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
    };



function detalhes_modal_cliente(id_venda) {
    var data_vendas = Utils.getLocalStorageItem("data_vendas");
    var venda_selecionada = {};
    // Encontra a venda selecionada
    data_vendas.forEach(function(item) {
        if (item.id_venda === id_venda) {
            venda_selecionada = item;
        }
    });
    atualizarDetalhesTransacao(venda_selecionada);

    // Chama a API para obter os produtos da venda
    manageLoading(true,"ul_produtos");
    chamarFuncaoPython("/api/produtos/by/venda/" + id_venda, {}, "GET", function(response) {
        // Verifica se a resposta foi bem-sucedida
        if (response.success === true) {
            // Obtém a lista de produtos da resposta
            var produtos = response.list_produtos;

            // Itera sobre os produtos e os exibe
            produtos.forEach(function(valor) {
                var ul_produtos = document.getElementById("ul_produtos");
                var novoItemLista = document.createElement("li");
                novoItemLista.classList.add("list-group-item", "item-list-carrinho", "d-flex", "justify-content-between", "align-items-center");
                novoItemLista.innerHTML = `
                    <span class="badge text-bg-primary me-1 rounded-pill quantidade">${valor.quantidade_atual_estoque}</span>
                    <span class="text-small small" style="font-size: 0.8rem;">${valor.nome} R$ ${valor.preco_venda} Unid</span>
                `;
                ul_produtos.appendChild(novoItemLista);
            });
        }
        else {
            alertCustomer(response.message);
        }
         
        manageLoading(false,"ul_produtos");
    });
    manageLoading(true,"details-cliente");
    chamarFuncaoPython("/api/cliente/by/venda/" + id_venda, {}, "GET", function(response) {
        if (response.success === true) {
        montarInfoCliente(response.cliente,"details-cliente");
        } else {
            alertCustomer(response.message);
        }
        manageLoading(false,"details-cliente");
    });
    // Função para formatar números em moeda
    function formatarMoeda(valor) {
        // Converte o valor para um número decimal
        const valorDecimal = parseFloat(valor);
    
        // Verifica se o valorDecimal é um número
        if (!isNaN(valorDecimal)) {
            // Se for um número, formata para moeda e retorna
            return "R$ " + valorDecimal.toFixed(2);
        } else {
            // Se não for um número, retorna "N/A"
            return "N/A";
        }
    }

        // Função para atualizar os detalhes da transação com base nos dados recebidos
    function atualizarDetalhesTransacao(data) {
        manageLoading(true,"details-cliente");
        document.getElementById("detalhes_data_venda").textContent = data.data_venda || "N/A";
        document.getElementById("detalhes_forma_pagamento").textContent = data.forma_pagamento || "N/A";
        document.getElementById("detalhes_estado_transacao").textContent = data.estado_transacao || "N/A";
        document.getElementById("detalhes_metodo_entrega").textContent = data.metodo_entrega || "N/A";
        document.getElementById("detalhes_desconto").textContent = formatarMoeda(data.desconto);
        document.getElementById("detalhes_valor_total").textContent = formatarMoeda(data.valor_total);
        document.getElementById("detalhes_valor_entrega").textContent = formatarMoeda(data.valor_entrega);
        document.getElementById("detalhes_valor_pago").textContent = formatarMoeda(data.valor_pago);
        document.getElementById("detalhes_troco").textContent = formatarMoeda(data.troco);
        document.getElementById("detalhes_descricao").textContent = data.descricao || "N/A";

        const dataVenda = Utils.formatarDataHoraBR(data.data_venda, 1);
        const horarioVenda = Utils.formatarDataHoraBR(data.insert, 2);
        const Atualizacao = Utils.formatarDataHoraBR(data.update, 0);
    
        // Imprimir os dados nos spans correspondentes
        document.getElementById("detalhes_data_venda").textContent = dataVenda;
        document.getElementById("detalhes_horario_venda").textContent = horarioVenda;
        document.getElementById("detalhes_atualizacao").textContent = Atualizacao;

        var data_lojas = Utils.getLocalStorageItem("data_lojas");
        // Encontra a venda selecionada
        data_lojas.forEach(function(item) {
            if (item.id_loja === data.loja_id) {
                document.getElementById("detalhes_loja_venda").textContent = item.nome_loja;
            }
        });
        manageLoading(false,"details-cliente");

    }
     

    manageLoading(true,"details-retonaveis");
    
    chamarFuncaoPython("/api/retornaveis/by/venda/" + id_venda, {}, "GET", function(response) {
        if (response.success === true) {
            ProdutosRetornaveis(response.list_retornaveis);
        } else {
            alertCustomer(response.message);
        }
        manageLoading(false,"details-retonaveis");
    });function ProdutosRetornaveis(data_list) {
        const container = document.getElementById('details-retonaveis');
    
        for (let i = 0; i < data_list.length; i++) {
            const galaoEntrando = data_list[i];
    
            // Preencher os campos para o galão que está entrando
            const divEntrada = document.createElement('div');
            divEntrada.classList.add('border-dark', 'border', 'rounded', 'bg-success', 'p-3', 'm-0', 'text-dark', 'bg-opacity-25', 'mb-1');
            divEntrada.innerHTML = `
            <label class="form-label">Galão que entrou ${i + 1}.</label>
                <div class="col mx-1 p-0">
                        <span class="bi bi-calendar"></span>
                        <label class="form-label">Data de Validade:</label>
                        <span class="ml-1">${galaoEntrando.data_validade}</span>
                    </div>
                <div class="col mx-1 p-0">
                        <span class="bi bi-calendar"></span>
                        <label class="form-label">Data de Fabricação:</label>
                        <span class="ml-1">${galaoEntrando.data_fabricacao}</span>
                </div>
            <div class="col">
                <span class="bi bi-sign-in"></span>
                <label class="form-label">Tipo de entrada:</label>
                <span class="ml-1">${galaoEntrando.titulo}</span>
            </div>
            `;
            container.appendChild(divEntrada);
    
            const galaoSaindo = data_list[i];
    
            // Preencher os campos para o galão que está saindo
            const divSaida = document.createElement('div');
            divSaida.classList.add('border-dark', 'border', 'rounded', 'bg-danger', 'p-3', 'm-0', 'text-dark', 'bg-opacity-25', 'mb-2');
            divSaida.innerHTML = `
                        
                    <label class="form-label">Galão que saiu ${i + 1}.</label>
                        <div class="col mx-1 p-0">
                                <span class="bi bi-calendar"></span>
                                <label class="form-label">Data de Validade:</label>
                                <span class="ml-1">${galaoSaindo.data_validade}</span>
                        </div>
                        <div class="col mx-1 p-0">
                                <span class="bi bi-calendar"></span>
                                <label class="form-label">Data de Fabricação:</label>
                                <span class="ml-1">${galaoSaindo.data_fabricacao}</span>
                        </div>
                    </div>
                    <div class="col">
                        <span class="bi bi-sign-out"></span>
                        <label class="form-label">Tipo de saída:</label>
                        <span class="ml-1">${galaoSaindo.titulo}</span>
                    </div>
                    <div class="col">
                        <span class="bi bi-info-circle"></span>
                        <label class="form-label">Descrição:</label>
                        <span class="ml-1">${galaoSaindo.descricao || 'Nenhuma descrição disponível'}</span>
                    </div>
            `;
            container.appendChild(divSaida);
        }
    }
    
}