

        
window.onload = inicializarPagina;


function getData() {
    try {
        chamarFuncaoPython("/api/vendas/dados", null, 'GET', handleResponse);
    } catch (error) {
        console.error("Erro ao chamar a função Python:", error);
    }
}

function handleResponse(response) {
    if (response.success === true) {
        // Armazenar os dados no localStorage
        Utils.setLocalStorageItem('data_lojas', response.lojas);
        Utils.setLocalStorageItem('data_vendas', response.vendas);
        Utils.setLocalStorageItem('data_produtos', response.produtos);
        // Atualizar dropdown e filtrar vendas
        atualizarDropdownLojas(response.lojas, "select_lojas");
    } else {
        alertCustomer(response.error);
    }
}
function inicializarPagina() {
    Promise.all([
        getData(),
        listarMotoboys(),
        carregarListaClientes(),
        atualizarDropdownLojas(Utils.getLocalStorageItem('data_lojas'), "select_lojas"),
        preencherListaDeProdutos(),
        verificarVendaExistente(),
        verificarRetornaveis(),
        verificarListaProdutos()
    ]).then(() => {
        adicionarOuvintesDeEventos();
        configurarObservadorDeMutacao();
        applyAutocomplete();
    }).catch((error) => {
        console.error("Erro ao inicializar a página:", error);
    });
}
/**
 * Função principal para calcular o resumo dos valores e atualizar a interface.
 */
function calcularResumo() {
    var valorTotalItens = calcularValorItens();
    var valorTaxaEntrega = obterValorInput('id_taxa_entrega');
    var valorDesconto = obterValorInput('id_desconto');
    var valorPago = obterValorInput('id_valor_pago_dinheiro');

    var valorTotalComTaxaDesconto = valorTotalItens + valorTaxaEntrega - valorDesconto;
    var troco = calcularTroco(valorTotalComTaxaDesconto, valorPago);

    atualizarResumo(valorTotalItens, valorTaxaEntrega, valorDesconto, valorTotalComTaxaDesconto, troco);
}

/**
 * Obtém o valor de um input específico da interface.
 * @param {string} id - ID do input no DOM.
 * @returns {number} - Valor do input.
 */
function obterValorInput(id) {
    var input = document.getElementById(id);
    var valorText = input ? input.value.trim() : '';
    return parseFloat(valorText.replace(',', '.')) || 0;
}

/**
 * Calcula o valor total dos itens na lista.
 * @returns {number} - Valor total dos itens.
 */
function calcularValorItens() {
    var ul_produtos = document.getElementById("ul_produtos");
    var itensLista = ul_produtos.querySelectorAll(".list-group-item");
    var valorTotal = 0;
    var produtosData = Utils.getLocalStorageItem('data_produtos');

    itensLista.forEach(function(item) {
        var quantidade = parseInt(item.querySelector(".quantidade").textContent);
        var idProduto = item.getAttribute("data-id-produto");

        produtosData.forEach(function(produto) {
            if (produto.id_produto == idProduto) {
                var valorUnitario = parseFloat(produto.preco_venda);
                valorTotal += quantidade * valorUnitario;
            }
        });
    });

    var labelValorTotal = document.getElementById("txt_valor_total_produtos");
    if (labelValorTotal) {
        labelValorTotal.textContent = valorTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    }

    return valorTotal;
}

/**
 * Calcula o troco a ser devolvido.
 * @param {number} valorTotalComTaxaDesconto - Valor total com taxa de entrega e desconto.
 * @param {number} valorPago - Valor pago pelo cliente.
 * @returns {number} - Valor do troco.
 */
function calcularTroco(valorTotalComTaxaDesconto, valorPago) {
    return valorPago - valorTotalComTaxaDesconto;
}

/**
 * Atualiza o resumo dos valores na interface.
 * @param {number} valorTotalItens - Valor total dos itens.
 * @param {number} valorTaxaEntrega - Valor da taxa de entrega.
 * @param {number} valorDesconto - Valor do desconto.
 * @param {number} valorTotalComTaxaDesconto - Valor total com taxa de entrega e desconto.
 * @param {number} troco - Valor do troco.
 */
function atualizarResumo(valorTotalItens, valorTaxaEntrega, valorDesconto, valorTotalComTaxaDesconto, troco) {
    document.getElementById('txt_taxa_entrega').textContent = valorTaxaEntrega.toFixed(2).replace('.', ',');
    document.getElementById('txt_desconto').textContent = valorDesconto.toFixed(2).replace('.', ',');
    document.getElementById('txt_valor_total_apagar').textContent = valorTotalComTaxaDesconto.toFixed(2).replace('.', ',');
    document.getElementById('txt_troco').textContent =  troco.toFixed(2).replace('.', ',');
}



 
function toggleCliente(selecionado = false) {
    const titleHeader = document.getElementById('title_header_cliente');
    const iconBtnToggle = document.getElementById('icon_btn_toggle');
    const containerBuscarCliente = document.getElementById('container_buscar_cliente');
    const containerSelecionarCliente = document.getElementById('container_selecionar_cliente');
    const containerCriarCliente = document.getElementById('container_cria_cliente');

    if (selecionado) {
        titleHeader.textContent = 'Cliente Selecionado';
        iconBtnToggle.className = 'bi bi-x-circle';
        containerBuscarCliente.classList.add('d-none');
        containerSelecionarCliente.classList.remove('d-none');
        containerCriarCliente.classList.add('d-none');
        document.getElementById('btn_toggle').setAttribute('onclick', 'toggleCliente(false);limparInfoCliente(); ');
    } else {
        switch (titleHeader.textContent.trim()) {
            case 'Cliente Selecionado':
                titleHeader.textContent = 'Buscar Cliente';
                iconBtnToggle.className = 'bi bi-person-plus';
                containerBuscarCliente.classList.remove('d-none');
                containerSelecionarCliente.classList.add('d-none');
                containerCriarCliente.classList.add('d-none');
                document.getElementById('btn_toggle').setAttribute('onclick', 'toggleCliente()');
                break;
            case 'Buscar Cliente':
                titleHeader.textContent = 'Cadastrar Cliente';
                iconBtnToggle.className = 'bi bi-search';
                containerBuscarCliente.classList.add('d-none');
                containerSelecionarCliente.classList.add('d-none');
                containerCriarCliente.classList.remove('d-none');
                break;
            case 'Cadastrar Cliente':
                titleHeader.textContent = 'Buscar Cliente';
                iconBtnToggle.className = 'bi bi-person-plus';
                containerBuscarCliente.classList.remove('d-none');
                containerSelecionarCliente.classList.add('d-none');
                containerCriarCliente.classList.add('d-none');
                break;
        }
    }
}
// Função para verificar e atualizar a lista de produtos
function verificarListaProdutos() {
    var ul_produtos = document.getElementById("ul_produtos").innerHTML.trim();

    // Verifica se a lista de produtos está vazia
    if (ul_produtos === "") {
        // Adiciona automaticamente o item padrão
        document.getElementById("ul_produtos").innerHTML = `
            <li id="info_carrinho" class=" bg-dark text-white fw-bold d-flex justify-content-center align-items-center">
                Nada adicionado
            </li>`;
    }else{
        var infoCarrinho = document.getElementById("info_carrinho");
        if (infoCarrinho) {
            infoCarrinho.remove();
        }
    }
}
// Adiciona um ouvinte de evento para verificar a lista de produtos sempre que houver uma mudança

function forma_pagamento() {
    var selectedOption = this.options[this.selectedIndex];
    var selectedValue = selectedOption.value;
    if (selectedValue === "dinheiro") {
        document.querySelector(".gestaotroco").classList.remove("d-none"); // Remove a classe que oculta o container
    } else {
        document.querySelector(".gestaotroco").classList.add("d-none"); // Adiciona a classe que oculta o container
        document.getElementById('id_valor_pago_dinheiro').value="00,00";
        calcularResumo();
    }
} 
function metodo_entrega() {
    var selectedOption = this.value; // Obtém o valor selecionado
    var containerEntrega = document.getElementById('id_container_entrega');

    // Verifica se a opção selecionada é "entrega_no_local"
    if (selectedOption === 'entrega no local') {
      containerEntrega.classList.remove('d-none'); // Remove a classe d-none
    } else {
      containerEntrega.classList.add('d-none'); // Adiciona a classe d-none
    }

    var selectedOption = this.options[this.selectedIndex];
    var selectedValue = selectedOption.value;
    if (selectedValue === "retirado na loja") {
        document.getElementById("id_estado_transacao").value = "finalizado";
    }
    if (selectedValue === "entrega no local") {
        document.getElementById("id_estado_transacao").value = "processando";
        toggleGestaoEntrega();
    }
    
}
 
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
        data_clientes = Utils.getLocalStorageItem('data_clientes');
        manipularPesquisaClientes(data_clientes);  
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

// Função para carregar e manipular a lista de clientes
function carregarListaClientes() {
    chamarFuncaoPython( '/api/cliente/by_empresa', null, 'GET', function(response) {
        if (response.success == true) {
            Utils.setLocalStorageItem("data_clientes",response.clientes)
        }  
    });  
     
} 


function submitCadastroCliente() {
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
    chamarFuncaoPython('/api/cliente/create', formInputs, 'POST', function(response) {
        if (response.data) {
            alertCustomer("Cliente criado com sucesso!");
            montarInfoCliente(response.data,true);
            toggleCliente(true);

        } else {
            alertCustomer('Ocorreu um erro ao criar o cliente: ' + response.error);
        }
    } );
     
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
function limparInfoCliente() {
    var container = document.getElementById("container_selecionar_cliente");
    // Limpar os textos dos campos no containerx
    container.querySelector("#info_nome_cliente").textContent = "";
    container.querySelector("#info_telefone_cliente").textContent = "";
    container.querySelector("#info_tipo_cliente").textContent = "";
    container.querySelector("#info_descricao_cliente").textContent = "";
    container.querySelector("#info_codigo_postal").textContent = "";
    container.querySelector("#info_rua").textContent = "";
    container.querySelector("#info_numero").textContent = "";
    container.querySelector("#info_bairro").textContent = "";
    container.querySelector("#info_cidade").textContent = "";
    container.querySelector("#info_estado").textContent = "";
    container.querySelector("#info_descricao_endereco").textContent = "";
    container.querySelector("#info_ultima_venda_descricao").textContent = "";
    container.querySelector("#info_ultima_venda_data_venda").textContent = "";
    container.querySelector("#info_ultima_venda_forma_pagamento").textContent = "";
    container.querySelector("#info_ultima_venda_valor_total").textContent = "";
    container.querySelector("#info_ultima_venda_produtos").textContent = "";
    document.getElementById('id_cliente').value = "0"; 
}

function montarInfoCliente(cliente, isData = false) {
    // Se isData for falso, buscar o cliente pelo ID
    if (!isData) {
        const data_clientes = Utils.getLocalStorageItem('data_clientes');
        cliente = data_clientes.find(c => c.id_cliente == cliente);
    }

    if (!cliente) {
        console.error(`Cliente não encontrado`);
        return;
    }

    const container = document.getElementById("container_selecionar_cliente");

    // Função auxiliar para atualizar o conteúdo de um campo
    function updateField(selector, value) {
        container.querySelector(selector).textContent = value || "N/A";
    }

    // Atualizar os valores dos campos com os dados do cliente
    const clienteFields = [
        { selector: "#info_nome_cliente", value: cliente.nome },
        { selector: "#info_telefone_cliente", value: cliente.telefone },
        { selector: "#info_tipo_cliente", value: cliente.tipo_cliente },
        { selector: "#info_descricao_cliente", value: cliente.descricao },
        { selector: "#info_codigo_postal", value: cliente.codigo_postal },
        { selector: "#info_rua", value: cliente.rua },
        { selector: "#info_numero", value: cliente.numero },
        { selector: "#info_bairro", value: cliente.bairro },
        { selector: "#info_cidade", value: cliente.cidade },
        { selector: "#info_estado", value: cliente.estado },
        { selector: "#info_descricao_endereco", value: cliente.descricao_endereco }
    ];

    clienteFields.forEach(field => updateField(field.selector, field.value));

    // Verificar se há informações da última venda
    if (cliente.ultima_venda) {
        const vendaFields = [
            { selector: "#info_ultima_venda_descricao", value: cliente.ultima_venda.descricao },
            { selector: "#info_ultima_venda_data_venda", value: cliente.ultima_venda.data_venda },
            { selector: "#info_ultima_venda_forma_pagamento", value: cliente.ultima_venda.forma_pagamento },
            { selector: "#info_ultima_venda_valor_total", value: cliente.ultima_venda.valor_total },
            { selector: "#info_ultima_venda_produtos", value: cliente.ultima_venda.produtos ? cliente.ultima_venda.produtos.join(", ") : "N/A" }
        ];

        vendaFields.forEach(field => updateField(field.selector, field.value));
    } else {
        const emptyVendaFields = [
            "#info_ultima_venda_descricao",
            "#info_ultima_venda_data_venda",
            "#info_ultima_venda_forma_pagamento",
            "#info_ultima_venda_valor_total",
            "#info_ultima_venda_produtos"
        ];

        emptyVendaFields.forEach(selector => updateField(selector, ""));
    }

    alertCustomer(`Cliente selecionado: ${cliente.nome}`);
    toggleCliente(true);
}

 
function clean_form() {
    document.getElementById('id_taxa_entrega').innerText= "";
    document.getElementById('id_desconto').innerText= "";
    document.getElementById('id_valor_pago_dinheiro').innerText="";
    document.getElementById('id_descricao_venda').innerText= "";
    //resumo
    document.getElementById("txt_valor_total_apagar").textContent = "00,00";
    document.getElementById("txt_troco").textContent = "00,00";
    document.getElementById("txt_taxa_entrega").textContent = "00,00";
    document.getElementById("txt_desconto").textContent = "00,00";
    //carrinho
    document.getElementById("txt_valor_total_produtos").textContent = "00,00";
    document.getElementById("ul_produtos").innerHTML = "";

    document.getElementById("id_motoboy").value= "0";

    document.getElementById('id_forma_pagamento').selectedIndex= 0;
    document.getElementById('id_estado_transacao').selectedIndex= 0;
    document.getElementById('id_metodo_entrega').selectedIndex = 0;
    document.getElementById('id_motoboy').selectedIndex = 0;
    document.getElementById("select_loja").selectedIndex = 0

    document.getElementById("select_loja").dispatchEvent(new Event('change'));
    document.getElementById("id_metodo_entrega").dispatchEvent(new Event('change'));
    document.getElementById("id_forma_pagamento").dispatchEvent(new Event('change'));
    document.getElementById('id_cliente').value = "0";
    toggleCliente(false);
    alertCustomer("Formulario Limpado.");
}
 

// Função para atualizar o dropdown com as lojas
function atualizarDropdownLojas(list_lojas, classe_select_lojas) {
    // Seleciona todos os elementos select com a classe especificada
    const selects = document.querySelectorAll('.' + classe_select_lojas);

    // Itera sobre cada select encontrado
    selects.forEach(function(select) {
        // Limpa as opções existentes
        select.innerHTML = '';

        // Adiciona a opção padrão, se houver mais de uma loja na lista
        if (list_lojas.length > 1) {
            const optionDefault = document.createElement('option');
            optionDefault.value = '0';
            optionDefault.textContent = 'Selecione';
            select.appendChild(optionDefault);
        }

        // Adiciona as opções de lojas
        list_lojas.forEach(function(loja) {
            const option = document.createElement('option');
            option.value = loja.id_loja;
            option.textContent = loja.nome_loja;
            select.appendChild(option);
        });
    });
} 

function listarMotoboys() {
        chamarFuncaoPython('/listar_motoboys_por_empresa', null, 'GET', function(response) {
            if (response.motoboys) {
                var selectMotoboy = document.getElementById('id_motoboy');
                selectMotoboy.innerHTML = ''; // Limpar as opções existentes
                // Adicionar as opções dos motoboys
                if(response.motoboys.length > 0){
                    var option = document.createElement('option');
                    option.value = 0;
                    option.text = "Selecione";
                    selectMotoboy.appendChild(option);
                    response.motoboys.forEach(motoboy => {
                        var option = document.createElement('option');
                        option.value = motoboy.id_motoboy;
                        option.text = motoboy.nome;
                        selectMotoboy.appendChild(option);
                    });
    
                }  
        }
    });
}
function toggleGestaoEntrega() {
    var container = document.getElementById("container_gestao_entrega");
    var iconeOpen = document.getElementById("icone_entrega_open");
    var iconeClose = document.getElementById("icone_entrega_close");

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
    } else  {
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
function insertMotoboy() {
    var nome  = document.getElementById('nome_motoboy').value.trim();
    var telefone  = document.getElementById('telefone_motoboy').value.trim();
    manageLoading(true,"cadastrar_motoboy"); 
    // Validar se os campos não estão vazios
    if (nome === '') {
        alertCustomer('insira o nome do motoboy.');
            manageLoading(false,"cadastrar_motoboy");
            return false;
    }
    if (telefone === '') {
        alertCustomer('insira o telefone do motoboy.');
            manageLoading(false,"cadastrar_motoboy");
            return false;
    }
    chamarFuncaoPython('/create_motoboy/', {nome, telefone}, 'POST', function(response) {
        if (response.status === 'success') {
            // Limpar os campos após a criação bem-sucedida
            document.getElementById('nome_motoboy').value = '';
            document.getElementById('telefone_motoboy').value = '';
            toggleMotoboyFields();
            listarMotoboys();
        } else {
            alertCustomer('Erro ao cadastrar motoboy');
        }
    });
    manageLoading(false,"cadastrar_motoboy");
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
 

// Defina sua função de verificação
function verificarAntesDoSubmit() {
   // Verifica se uma loja foi selecionada
    if (document.getElementById('select_loja').value == "0") {
        alertCustomer('selecione uma loja antes de enviar o formulário.');
        return false;  
    }
    // Verifica se há itens no carrinho
    var carrinho = atualizarCamposCarrinho();
    if (carrinho === false) {
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
    else if (metodoEntrega == "entrega no local") {
        var taxaEntrega = document.getElementById('id_taxa_entrega').value;
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

function obterValores() {
    var dados = {}; // Objeto para armazenar os dados

    // Método de Entrega
    var loja = document.getElementById('select_loja');
    dados['loja'] = loja.value;

    var metodoEntrega = document.getElementById('id_metodo_entrega');
    dados['metodo_entrega'] = metodoEntrega.value;

    // Taxa de Entrega (se visível)
    var taxaEntrega = document.getElementById('id_taxa_entrega');
    dados['taxa_entrega'] = taxaEntrega.value;

    // Estado da Transação
    var estadoTransacao = document.getElementById('id_estado_transacao');
    dados['estado_transacao'] = estadoTransacao.value;

    // Forma de Pagamento
    var formaPagamento = document.getElementById('id_forma_pagamento');
    dados['forma_pagamento'] = formaPagamento.value;

    // Desconto
    var desconto = document.getElementById('id_desconto');
    dados['desconto'] = desconto.value;

    // Valor Pago (se visível)
    var valorPago = document.getElementById('id_valor_pago_dinheiro');
    dados['valor_pago'] = valorPago.value;

    // Descrição da Venda
    var descricaoVenda = document.getElementById('id_descricao_venda');
    dados['descricao_venda'] = descricaoVenda.value;

    // Motoboy
    var motoboy = document.getElementById('id_motoboy');
    dados['motoboy'] = motoboy.value;

    // Troco
    var trocoElemento = document.getElementById('txt_troco');
    var trocoTexto = trocoElemento.innerText;

    // Verifica se trocoTexto é uma string antes de tentar substituir
    if (typeof trocoTexto === 'string') {
        var trocoLimpo = trocoTexto.replace(/[^\d,]/g, '');
        dados['troco'] = trocoLimpo;
    } else {
        dados['troco'] = 0; 
    }
    // Total a Pagar
    var totalApagar = document.getElementById('input_total_apagar');
    dados['total_apagar'] = totalApagar.value;

    // ID do Cliente
    var idCliente = document.getElementById('id_cliente');
    dados['id_cliente'] = idCliente.value;


    var formGestaoGalao = document.getElementById("form_galaoGestao");
    var inputsContainers = formGestaoGalao.querySelectorAll('.container_galao_troca');
    var list = {};
    inputsContainers.forEach((container, index) => {
        var inputs = container.querySelectorAll('input, select');
        var troca = {};

        inputs.forEach(input => {
            troca[input.name] = input.value;
        });

        list['obj' + (index + 1)] = troca;
    });
    dados["galoes_troca"] = list

    // Obter valores do carrinho
    var carrinho = atualizarCamposCarrinho();
    if (carrinho !== false) {
        dados['carrinho'] = carrinho;
    }

     
    dados["id_venda"]= document.getElementById("id_venda").value;
      
    return dados
}

// Exemplo de como usar a função para obter os valores

function enviarDadosVenda() {
    data= obterValores();
    chamarFuncaoPython('/vendas/criar/processar_venda',data,'POST',function(response){
            if (response.success===true) {
                if(data.id_venda!= ""){
                    window.location.href =  "/vendas"; 
            }else{
                    alertCustomer(response.message,1);
                    clean_form();
                    inicializarPagina();
                }

            } else {
                if(data.id_venda!= ""){
                    window.location.href =  "/vendas/"; }
                clean_form();
                alertCustomer(response.error);
            }
            btnSubmit.disabled = false;
    }); 
     

} 

document.getElementById("btnSubmit").addEventListener("click", function(event) {
    var btnSubmit = document.getElementById("btnSubmit");
    
    // Desabilita o botão para evitar cliques repetidos
    btnSubmit.disabled = true;

    // Chama a função de verificação antes de permitir o envio do formulário
    if (!verificarAntesDoSubmit()) {
        event.preventDefault(); // Impede o envio do formulário se a verificação falhar
        btnSubmit.disabled = false; // Reabilita o botão se a verificação falhar
    } else {
        enviarDadosVenda();
    } 
});

function atualizarCamposCarrinho() {
    var itensLista = document.querySelectorAll('.item-list-carrinho');

    // Verificar se há itens na lista de produtos
    if (itensLista.length === 0) {
        return false; // Retorna false se não houver itens
    }

    var carrinho = [];
    
    itensLista.forEach(function(item) {
        var idProduto = item.getAttribute('data-id-produto');
        var quantidade = parseInt(item.querySelector(".quantidade").textContent);
        var produto = {
            "id_produto": idProduto,
            "quantidade": quantidade
        };
        carrinho.push(produto);
    });

    var data = { "carrinho": carrinho };
    return data; // Retorna os itens do carrinho dentro de um objeto data
}


function aumentarQuantidade(elemento) {
    // Encontra o elemento pai do elemento atual
    var pai = elemento.closest(".list-group-item");
    // Obtém o ID do produto do atributo data-id-produto do elemento pai
    var idProduto = pai.getAttribute("data-id-produto");
    produtos_data = Utils.getLocalStorageItem('data_produtos');

    produtos_data.forEach(function(produto) {
        if(produto.id_produto == idProduto) {
            var quantidadeSpan = pai.querySelector(".quantidade");
            var quantidadeAtual = parseInt(quantidadeSpan.textContent);
                if(produto.quantidade_atual_estoque >= quantidadeAtual) {
                    quantidadeSpan.textContent = quantidadeAtual + 1;
                    calcularResumo();
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
    calcularResumo();
    verificarListaProdutos();

}

function toggleGestaoRetornavel(status) {
    var container = document.getElementById("body_gestaoRetornavel");
    var icone = document.getElementById("icone_produto");
    var botao = document.getElementById("btn_gestao_retornaveis");

    if (status) {
        botao.setAttribute("onclick", "toggleGestaoRetornavel(false);");
        container.classList.remove("d-none");
        icone.classList.remove("bi-eye-slash");
        icone.classList.add("bi-eye");
    } else {
        botao.setAttribute("onclick", "toggleGestaoRetornavel(true);");
        container.classList.add("d-none");
        icone.classList.remove("bi-eye");
        icone.classList.add("bi-eye-slash");
    }
}

  

function select_loja() {
    // Obtém o ID da loja selecionada convertendo para um número inteiro
    const selectedLoja = parseInt(this.value);

    const produtosUl = document.getElementById("ul_produtos");

    // Verifica se há produtos na lista atual
    if (produtosUl.innerHTML !== "") {
        const itensLista = produtosUl.querySelectorAll(".list-group-item");

        // Verifica se há itens na lista
        if (itensLista.length > 0) {
            let mensagemExibida = false; // Variável de controle para verificar se a mensagem já foi exibida

            const produtosData = Utils.getLocalStorageItem('data_produtos');

            // Obtém o loja_id do primeiro produto no carrinho
            const idExistente = itensLista[0].getAttribute("data-id-produto");
            const primeiroProduto = produtosData.find(prod => prod.id_produto === idExistente);
            const lojaIdCarrinho = primeiroProduto ? primeiroProduto.loja_id : null;

            // Itera sobre os itens da lista para verificar se o produto já está na lista
            itensLista.forEach(item => {
                const idExistente = item.getAttribute("data-id-produto");
                const produto = produtosData.find(prod => prod.id_produto === idExistente);

                // Verifica se o produto existe e se ele não pertence à loja selecionada
                if (produto && produto.loja_id !== selectedLoja) {
                    // Exibe a mensagem apenas uma vez
                    if (!mensagemExibida) {
                        alertCustomer("Não é possível vender produtos de diferentes lojas. Limpe o carrinho caso queira alterar a loja.", 4);
                        mensagemExibida = true; // Marca que a mensagem foi exibida
                        // Restaura o valor do select para o loja_id do carrinho
                        this.value = lojaIdCarrinho;
                    }
                }
            });
            calcularResumo();
        }
    }
    preencherListaDeProdutos();
}

          
function verificarVendaExistente() {
    const id_venda = document.getElementById('id_venda').value;
    if (id_venda !== "") {
        editarVenda(id_venda);
    }
}
 
function preencherListaDeProdutos() {
    const select_produto = document.getElementById('select_produto');
    select_produto.innerHTML = ''; // Limpa opções existentes
    const select_loja = document.getElementById('select_loja');
    const loja_selecionada = parseInt(select_loja.value); // Obtém o valor da loja selecionada
    produtos_data = Utils.getLocalStorageItem('data_produtos').filter(produto => produto.loja_id === loja_selecionada);

    const defaultOption = document.createElement('option');
    defaultOption.text = "Selecione";
    defaultOption.value = "0";
    select_produto.appendChild(defaultOption);

    produtos_data.forEach(function(produto) {
        const option = document.createElement('option');
        option.dataset.idProduto = produto.id_produto;
        option.text = produto.nome;
        option.value = produto.id_produto;
        select_produto.appendChild(option);
    });
}

function adicionarOuvintesDeEventos() {
    document.getElementById('id_taxa_entrega').addEventListener('input', calcularResumo);
    document.getElementById('id_desconto').addEventListener('input', calcularResumo);
    document.getElementById('id_valor_pago_dinheiro').addEventListener('input', calcularResumo);
    document.getElementById('id_forma_pagamento').addEventListener('change', forma_pagamento);
    document.getElementById('id_metodo_entrega').addEventListener('change', metodo_entrega);
    document.getElementById('select_loja').addEventListener('change', select_loja);
}


function configurarObservadorDeMutacao() {
    const observerOptions = {
        childList: true,
        subtree: true
    };

    const observerCallback = function(mutationsList) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                verificarRetornaveis();
                configurarMascarasEValidacoes();
                break;
            }
        }
    };

    const ul_produtos = document.getElementById("ul_produtos");
    const observer = new MutationObserver(observerCallback);
    observer.observe(ul_produtos, observerOptions);
}

function configurarMascarasEValidacoes() {
    $('.data-mes-ano-mask').mask('00/0000');
    document.querySelectorAll(".data-validade").forEach(function(input) {
        input.addEventListener("input", function() {
            clearTimeout(input.timeoutId);
            input.timeoutId = setTimeout(function() {
                validarEAtualizarData(input);
            }, 500);
        });
    });
}

function validarEAtualizarData(input) {
    const dataValidade = input.value.trim();
    if (dataValidade === "") return;

    const regex = /^(0[1-9]|1[0-2])\/\d{4}$/;
    if (!regex.test(dataValidade)) return;

    const [mes, ano] = dataValidade.split("/").map(Number);
    const dataFabricacao = ("0" + mes).slice(-2) + "/" + (ano - 3);

    const dataFabricacaoField = input.closest('.row').querySelector(".data-fabricacao");
    if (dataFabricacaoField) {
        dataFabricacaoField.value = dataFabricacao;
    }
}

document.getElementById('select_produto').addEventListener('change', function() {
    const adicionarProdutoBtn = document.getElementById('adicionarProdutoBtn');
    const selectedOption = this.options[this.selectedIndex];
    adicionarProdutoBtn.dataset.idProduto = selectedOption.value;
    adicionarProdutoBtn.dataset.nomeProduto = selectedOption.text;
});

document.getElementById('adicionarProdutoBtn').addEventListener('click', function() {
    const produtoId = this.dataset.idProduto;
    const produtoNome = this.dataset.nomeProduto;
    if (produtoId && produtoId !== "0") {
        Ouvinte(produtoId);
    } else {
        alertCustomer("Selecione um produto da lista de sugestões.");
    }
});

function Ouvinte(produtoId) {
    var produtos_data = Utils.getLocalStorageItem('data_produtos');
    var produtoSelecionado = null;

    produtos_data.forEach(function(produto) {
        if (produto.id_produto == produtoId) {
            if (produto.quantidade_atual_estoque >= 1) {
                produtoSelecionado = produto;
            } else {
                alertCustomer("Não há mais produto disponível no estoque.");
            }
        }
    });

    if (produtoSelecionado != null) {
        var ul_produtos = document.getElementById("ul_produtos")
        var itensLista = ul_produtos.querySelectorAll(".list-group-item");
        var produtoExistente = false;

        itensLista.forEach(function (item) {
            var idExistente = item.getAttribute("data-id-produto");
                
            if (idExistente === produtoId) {
                var quantidadeSpan = item.querySelector(".quantidade");
                var quantidadeAtual = parseInt(quantidadeSpan.textContent);
                quantidadeSpan.textContent = quantidadeAtual + 1;
                produtoExistente = true;
            }
        });

        if (!produtoExistente) {
            var novoItemLista = document.createElement("li");
            novoItemLista.classList.add("list-group-item", "item-list-carrinho", "bg-dark", "text-white", "fw-bold", "d-flex", "justify-content-between", "align-items-center");
            novoItemLista.setAttribute("data-id-produto", produtoSelecionado.id_produto);
            novoItemLista.setAttribute("data-retornavel", produtoSelecionado.is_retornavel);
            novoItemLista.setAttribute("data-valor", produtoSelecionado.valor);

            novoItemLista.innerHTML = `
                <span class="badge text-bg-primary me-1 rounded-pill quantidade">1</span>
                <span class="text-small small my-auto" style="font-size: 0.8rem;">${produtoSelecionado.nome} R$ ${produtoSelecionado.preco_venda} Unidade</span>
                <span class="btn btn-sm btn-outline-primary bi-plus ms-auto" data-id-produto="${produtoSelecionado.id_produto}" onclick="aumentarQuantidade(this)"></span>
                <span class="btn btn-sm btn-outline-danger bi-dash ms-1" onclick="diminuirQuantidade(this)"></span>
            `;
            ul_produtos.appendChild(novoItemLista);
        }

        calcularResumo();
    }

    verificarListaProdutos();
}
// Função para verificar os produtos retornáveis
function verificarRetornaveis() {
    
    var itensLista = document.getElementById("ul_produtos").querySelectorAll(".list-group-item");
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
        document.getElementById("form_galaoGestao").innerHTML= "";
        
        toggleGestaoRetornavel(false);
    }
}


// Função para gerar os inputs dinamicamente com base no número de galões que estão saindo
function gerarInputs(numeroGaloes,obj={}) {
     var formGestaoGalao = document.getElementById("form_galaoGestao");
        // Encontra o número de formulários já existentes
        var numFormulariosExistentes = formGestaoGalao.querySelectorAll('.container_galao_troca').length;

        // Calcula quantos novos formulários precisam ser adicionados
        var numNovosFormularios = numeroGaloes - numFormulariosExistentes;
        var i  = numFormulariosExistentes;
        
        // Adiciona apenas os novos formulários que faltam
        for (var o = 0; o < numNovosFormularios; o++) {
            // Inputs para os galões que estão entrando
            // Verificando e preenchendo os campos para o galão que está entrando
            container_galao_troca = `
            <div class=" container_galao_troca">
            <div class="border-dark border rounded    bg-success p-3 m-0 text-dark bg-opacity-25 mb-1">
                <div class="row">
                    <label class="form-label" style="font-size: 1rem">Galão que está entrando ${i + 1}.</label>
                    <div class="col mx-1 p-0">
                        <div class="form-floating mb-2">
                            <input type="text" id="data_validade_entrada" name="data_validade_entrada" value="${obj.validade_entrada ? obj.validade_entrada : ''}" class="form-control data-validade data-mes-ano-mask">
                            <label for="data_validade_entrada" style="font-size: 0.6rem" class="form-label">Data de Validade: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                        </div>
                    </div>
                    <div class="col mx-1 p-0">
                        <div class="form-floating mb-2">
                            <input type="text" id="data_fabricacao_entrada" name="data_fabricacao_entrada" value="${obj.fabricacao_entrada ? obj.fabricacao_entrada : ''}" class="form-control data-fabricacao data-mes-ano-mask">
                            <label for="data_fabricacao_entrada" style="font-size: 0.6rem" class="form-label">Data de Fabricação: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                        </div>
                    </div>
                </div>
                <div class="form-floating mb-2">
                    <select id="tipo_entrada" name="tipo_entrada" class="form-select">
                        <option value="Não Selecionado" disabled>Selecione</option>
                        ${obj.tipo_entrada ? `<option value="${obj.tipo_entrada}" selected>${obj.tipo_entrada}</option>` : ''}
                        <option value="Galão 20 Litros">Galão 20 Litros</option>
                        <option value="Galão 10 Litros">Galão 10 Litros</option>
                        <option value="Galão 5 Litros">Galão 5 Litros</option>
                        <option value="outro">Outro</option>
                    </select>
                    <label for="tipo_entrada" style="font-size: 0.7rem" class="form-label">Tipo de entrada:</label>
                </div>
            </div> 
            <div class="border-dark border rounded bg-danger p-3 m-0 text-dark bg-opacity-25 mb-2">
                <div class="row">
                    <label class="form-label" style="font-size: 1rem">Galão que está saindo ${i + 1}.</label>
                    <div class="col mx-1 p-0">
                        <div class="form-floating mb-2">
                            <input type="text" id="data_validade_saida" name="data_validade_saida" value="${obj.validade_saida ? obj.validade_saida : ''}" class="form-control data-validade data-mes-ano-mask">
                            <label for="data_validade_saida" style="font-size: 0.6rem" class="form-label">Data de Validade: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                        </div>
                    </div>
                    <div class="col mx-1 p-0">
                        <div class="form-floating mb-2">
                            <input type="text" id="data_fabricacao_saida" name="data_fabricacao_saida" value="${obj.fabricacao_saida ? obj.fabricacao_saida : ''}" class="form-control data-fabricacao data-mes-ano-mask">
                            <label for="data_fabricacao_saida" style="font-size: 0.6rem" class="form-label">Data de Fabricação: <span style="font-size: 0.5rem;">(mes/ano)</span></label>
                        </div>
                    </div>
                </div>
                <div class="form-floating mb-2">
                    <select id="tipo_saida" name="tipo_saida" class="form-select">
                        ${obj.tipo_saida ? `<option value="${obj.tipo_saida}" selected>${obj.tipo_saida}</option>` : ''}
                        <option value="Não Selecionado" disabled>Selecione</option>
                        <option value="Galão 20 Litros">Galão 20 Litros</option>
                        <option value="Galão 10 Litros">Galão 10 Litros</option>
                        <option value="Galão 5 Litros">Galão 5 Litros</option>
                        <option value="outro">Outro</option>
                    </select>
                    <label for="tipo_saida" style="font-size: 0.7rem" class="form-label">Tipo de saída:</label>
                </div>
                <div class="form-floating mb-2">
                    <input type="text" id="id_descricao_gestão_galao" value="${obj.descricao_gestao ? obj.descricao_gestao : ''}" name="id_descricao_gestão_galao" class="form-control">
                    <label for="id_descricao_gestão_galao" style="font-size: 0.7rem" class="form-label">Descrição: <span style="font-size: 0.6rem;">(Opcional)</span></label>
                </div>
            </div>
            </div>
            `;

            formGestaoGalao.insertAdjacentHTML('beforeend', container_galao_troca);
        }

        // Se houver mais formulários do que galões especificados, remova o último container
        if (numFormulariosExistentes > numeroGaloes) {
            for (var j = 0; j < numFormulariosExistentes - numeroGaloes; j++) {
                // Encontra os containers de entrada e saída
                var container_galao_troca = formGestaoGalao.querySelector('.container_galao_troca:last-child');

                // Remove os containers do formulário
                container_galao_troca.remove();
            }
        }
        
}

         

 
function editarVenda(id_venda) {
    // Busca os dados de vendas do armazenamento local
    const vendas = Utils.getLocalStorageItem("data_vendas");
    // Encontra a venda correspondente com base no idVenda fornecido
    const venda = vendas.find(venda => venda.id_venda === id_venda);


    const container_pay = document.getElementById("body_gestao_pay");
    // Verifica se a venda foi encontrada
    if (venda) {
        function setElementValue(id, value) {
            document.getElementById(id).value = value;
            document.getElementById(id).dispatchEvent(new Event('change'));
        }
        
        function setTextContent(id, text) {
            document.getElementById(id).textContent = text;
        }
        
        setElementValue("id_metodo_entrega", venda.metodo_entrega);
        setElementValue("id_estado_transacao", venda.estado_transacao);
        setElementValue("id_forma_pagamento", venda.forma_pagamento);
        setElementValue("id_desconto", parseFloat(venda.desconto).toFixed(2));
        setTextContent("txt_valor_total_apagar", parseFloat(venda.valor_total).toFixed(2));
        setElementValue("id_taxa_entrega", parseFloat(venda.valor_entrega).toFixed(2));
        setElementValue("id_valor_pago_dinheiro", parseFloat(venda.valor_pago).toFixed(2));
        setTextContent("txt_troco", parseFloat(venda.troco).toFixed(2));
        setElementValue("id_descricao", venda.descricao);
        setElementValue("select_loja", venda.loja_id);

        chamarFuncaoPython('/get_motoboy_by_venda/'+venda.id_venda+"/", null, 'GET', function(response) {
            if (response.motoboy) {
                 setElementValue("id_motoboy", response.motoboy.id_motoboy);
            }
        });
    } else {
        console.log("Venda não encontrada.");
        return alertCustomer("Venda não encontrada.",2);
    }
    chamarFuncaoPython("/api/produtos/by/venda/" + id_venda, {}, "GET", function(response) {
        // Verifica se a resposta foi bem-sucedida
        if (response.success === true) {
            // Obtém a lista de produtos da resposta
            var produtos = response.list_produtos;
            var ul_produtos = document.getElementById("ul_produtos");
            ul_produtos.innerHTML = ""
            // Itera sobre os produtos e os exibe
            produtos.forEach(function(produto) {
                    var novoItemLista = document.createElement("li");
                    novoItemLista.classList.add("list-group-item",'item-list-carrinho',"bg-dark","text-white","fw-bold", "d-flex", "justify-content-between", "align-items-center");
                    novoItemLista.setAttribute("data-id-produto", produto.id_produto);
                    novoItemLista.setAttribute("data-retornavel", produto.is_retornavel); 
                    novoItemLista.setAttribute("data-valor", produto.valor);
                    // Preenche o HTML do novo item na lista de produtos
                    novoItemLista.innerHTML = `
                        <span class="badge text-bg-primary me-1 rounded-pill quantidade">${produto.quantidade}</span>
                        <span class="text-small small " style="font-size: 0.8rem;" >${produto.nome} R$ ${produto.preco_venda} Unidade</span>
                        <span class="btn btn-sm btn-outline-primary bi-plus ms-auto" data-id-produto="${produto.id_produto}" onclick="aumentarQuantidade(this)"></span>
                        <span class="btn btn-sm btn-outline-danger bi-dash ms-1" onclick="diminuirQuantidade(this)"></span>
                    `;
                    ul_produtos.appendChild(novoItemLista);
            });
            calcularResumo();
        }
        else {
            alertCustomer(response.message);
        }
    });
    chamarFuncaoPython("/api/cliente/by/venda" + id_venda, {}, "GET", function(response) {
        if (response.success === true) {
            montarInfoCliente(response.cliente,true);
            toggleCliente(true);
        }  
    });
 
    
    chamarFuncaoPython("/api/retornaveis/by/venda" + id_venda, {}, "GET", function(response) {
        if (response.success === true) {
            if(response.list_retornaveis.length >0){
                response.list_retornaveis.forEach(obj => {
                    gerarInputs(1, obj);
                });
            } 
        } 
    });

}