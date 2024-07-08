// Função para verificar e atualizar a lista de produtos
function verificarListaProdutos() {
    var listaProdutos = document.getElementById("listaProdutos").innerHTML.trim();

    // Verifica se a lista de produtos está vazia
    if (listaProdutos === "") {
        // Adiciona automaticamente o item padrão
        document.getElementById("listaProdutos").innerHTML = `
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
            document.getElementById('id_valor_pago').innerText="00,00";
            document.getElementById('txt_troco').innerText="00,00";
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
    chamarFuncaoPython( '/api/cliente/by_empresa/', null, 'GET', function(response) {
        if (response.success == true) {
            Utils.setLocalStorageItem("data_clientes",response.clientes)
            manipularPesquisaClientes(response.clientes);   

        }  
    });  
     
}

function get_data(){

try {
    chamarFuncaoPython("/api/vendas/dados", null, 'GET', function(response) {
        if (response.success === true) {
            // Armazenar os dados no localStorage
            Utils.setLocalStorageItem('data_lojas', response.lojas);
            Utils.setLocalStorageItem('data_vendas', response.vendas);
            Utils.setLocalStorageItem('data_produtos', response.produtos);
            atualizarDropdownLojas(response.lojas, "select_lojas");
            filtrarVendas(response.vendas);
        } else {
            alertCustomer(response.error);
        }
    });
} catch (error) {
    console.error("Erro ao chamar a função Python:", error);
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
    chamarFuncaoPython('/api/cliente/create/', formInputs, 'POST', function(response) {
        if (response.data) {
            alertCustomer("Cliente criado com sucesso!");
            gerencia_container_cliente(1)
            montarInfoCliente(response.data,"info_cliente");

        } else {
            alertCustomer('Ocorreu um erro ao criar o cliente: ' + response.error);
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
function limparInfoCliente(id_container) {
    var container = document.getElementById(id_container);
    // Limpar os textos dos campos no container
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
    // Exibir o container vazio
    container.classList.add("d-none");
}

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
    } else{
        container.querySelector("#info_ultima_venda_descricao").textContent ="";
        container.querySelector("#info_ultima_venda_data_venda").textContent ="";
        container.querySelector("#info_ultima_venda_forma_pagamento").textContent = "";
        container.querySelector("#info_ultima_venda_valor_total").textContent = "";
        container.querySelector("#info_ultima_venda_produtos").textContent = "";
    } 
    
    toggleResultadoPesquisa(false);
    alertCustomer(`Cliente selecionado: ${data.nome}`);
    // Exibir o container de informações
    container.classList.remove("d-none");
}
 function close_cliente(){
    document.getElementById('id_cliente').value = "0";
    document.getElementById('info_cliente').classList.add("d-none")
    toggleResultadoPesquisa(true);
    alertCustomer(`Cliente Retirado de Selecão`);
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
            option.textContent = loja.nome;
            select.appendChild(option);
        });
    });
} 

function listarMotoboys() {
        chamarFuncaoPython('/listar_motoboys_por_empresa/', null, 'GET', function(response) {
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
    if (document.getElementById('id_loja').value == "0") {
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
    var loja = document.getElementById('id_loja');
    dados['loja'] = loja.value;

    var metodoEntrega = document.getElementById('id_metodo_entrega');
    dados['metodo_entrega'] = metodoEntrega.value;

    // Taxa de Entrega (se visível)
    var containerEntrega = document.getElementById('id_container_entrega');
    if (containerEntrega.classList.contains('d-none') === false) {
        var taxaEntrega = document.getElementById('id_taxa_entrega');
        dados['taxa_entrega'] = taxaEntrega.value;
    }

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
    var valorPago = document.getElementById('id_valor_pago');
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
    var totalApagar = document.getElementById('total_apagar');
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
    chamarFuncaoPython('/vendas/criar/insert_venda_ajax/',data,'POST',function(response){
            if (response.success===true) {
                if(data.id_venda!= ""){
                    window.location.href =  "/vendas/"; 
            }else{
                    alertCustomer(response.message,1);
                    clean_form();
                    inicializarPagina();
                }

            } else {
                alertCustomer(response.error);
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

 
     


    function calcularValorTotal() {

        var itensLista = listaProdutos.querySelectorAll(".list-group-item");
        var valorTotal = 0;
        // Itera sobre os itens da lista e calcula o valor total
            itensLista.forEach(function (item) {
                var quantidade = parseInt(item.querySelector(".quantidade").textContent);
                var idProduto = item.getAttribute("data-id-produto");
                    produtos_data = Utils.getLocalStorageItem('data_produtos');

                    produtos_data.forEach(function(produto) {
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
        // Obtém o valor total
        var valorTotalInput = document.getElementById('id_valor_total');
        var valorTotalText = valorTotalInput ? valorTotalInput.textContent.trim() : '';
        var valorTotal = parseFloat(valorTotalText.replace(',', '.')) || 0;
    
        // Obtém a taxa de entrega
        var taxaEntregaInput = document.getElementById('id_taxa_entrega');
        var taxaEntregaText = taxaEntregaInput ? taxaEntregaInput.value.trim() : '';
        var taxaEntrega = parseFloat(taxaEntregaText.replace(',', '.')) || 0;
    
        // Obtém o desconto
        var descontoInput = document.getElementById('id_desconto');
        var descontoText = descontoInput ? descontoInput.value.trim() : '';
        var desconto = parseFloat(descontoText.replace(',', '.')) || 0;
    
        // Calcula o valor total considerando a taxa de entrega e o desconto
        var valorTotalComTaxaDesconto = valorTotal + taxaEntrega - desconto;
    
        // Define o valor total a ser pago
        document.getElementById('txt_valor_apagar').textContent = valorTotalComTaxaDesconto.toFixed(2).replace('.', ',');
        document.getElementById('total_apagar').value = valorTotalComTaxaDesconto.toFixed(2).replace('.', ',');
    
        // Obtém o valor pago
        var valorPagoInput = document.getElementById('id_valor_pago');
        var valorPago = valorPagoInput ? parseFloat(valorPagoInput.value.replace(',', '.')) : 0;
    
        // Calcula o troco apenas se o valor pago for maior ou igual ao total
        var troco = valorPago - valorTotalComTaxaDesconto;
    
        // Exibe a mensagem dependendo do resultado
        if (valorPago < valorTotalComTaxaDesconto) {
            // Calcula o valor que está faltando para cobrir o total da compra
            var valorFaltante = (valorTotalComTaxaDesconto - valorPago).toFixed(2);

            // Exibe a mensagem informando o valor faltante
            $('#txt_troco').text('Está Faltando: R$ ' + valorFaltante.replace('.', ',')).css('color', 'red');
        } else {
            // Exibe a mensagem informando o troco
            $('#txt_troco').text('Troco  R$ ' + troco.toFixed(2).replace('.', ',')).css('color', 'green');
        }
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
    verificarListaProdutos();

}

function toggleGestaoRetornavel(status) {
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
  
 
    // Adiciona um evento de mudança ao select de lojas
    function select_loja(){
        // Obtém o ID da loja selecionada convertendo para um número inteiro
        var selectedLoja = parseInt(this.value);
        // Obtém a lista de produtos e limpa os produtos existentes
        var produtosList = document.getElementById('produtosList');
        produtosList.innerHTML = '';

        // Adiciona produtos relevantes ao datalist
        produtos_data = Utils.getLocalStorageItem('data_produtos');

        // Verifica se há produtos na lista atual
        if (document.getElementById("listaProdutos").innerHTML !== "") {
            var itensLista = listaProdutos.querySelectorAll(".list-group-item");
            var mensagemExibida = false; // Variável de controle para verificar se a mensagem já foi exibida

            // Itera sobre os itens da lista para verificar se o produto já está na lista
            itensLista.forEach(function (item) {
                var idExistente = item.getAttribute("data-id-produto");
                var produto = produtos_data.find(item => item.id_produto == idExistente);

                // Remove o item da lista se ele não pertencer à loja selecionada
                if (produto.loja_id !== selectedLoja) {
                    item.parentNode.removeChild(item);
                    // Verifica se a mensagem já foi exibida
                    if (!mensagemExibida) {
                        alertCustomer("Não é possível vender produtos de diferentes lojas. Por isso, removemos os produtos da loja selecionada anteriormente.");
                        mensagemExibida = true; // Marca que a mensagem foi exibida
                    }
                }
            });
            calcularValorTotal();
        }

        // Itera sobre os produtos e adiciona aqueles que pertencem à loja selecionada ao datalist
        produtos_data.forEach(function(produto) {
            if (selectedLoja === '0' || produto.loja_id === selectedLoja) {
                var option = document.createElement('option');
                option.dataset.idProduto = produto.id_produto;
                option.value = produto.nome;
                produtosList.appendChild(option);
                produtoInput.setAttribute('list', 'produtosList');
            }
        });
    }
     // Função para lidar com a seleção de opção
     function OptionSelection(option) {
        // Obtém o ID do produto da opção selecionada e define o atributo de dados 'idProduto' no input do produto
        var produtoId = option.getAttribute("data-id-produto");
        produtoInput.dataset.idProduto = produtoId;
        
    }
    
    window.onload = function() {
        inicializarPagina();
    };
    
    function inicializarPagina() {
        get_data();
        listarMotoboys();
        carregarListaClientes();
        atualizarDropdownLojas(Utils.getLocalStorageItem('data_lojas'), "select_lojas");
        adicionarOuvintesDeEventos();
        preencherListaDeProdutos();
        verificarVendaExistente();
        configurarObservadorDeMutacao();
        verificarRetornaveis();
        verificarListaProdutos();
    }

function verificarVendaExistente() {
    const id_venda = document.getElementById('id_venda').value;
    if (id_venda !== "") {
        editarVenda(id_venda);
    }
}

function detectarSelecaoProduto() {
    const produtoInput = document.getElementById("produtoInput");
    const selectedOption = document.querySelector(`#produtosList option[value='${produtoInput.value}']`);
    if (selectedOption) {
        OptionSelection(selectedOption);
    }
}
function preencherListaDeProdutos() {
    const produtos_data = Utils.getLocalStorageItem('data_produtos');
    const produtosList = document.getElementById('produtosList');

    produtos_data.forEach(function(produto) {
        const option = document.createElement('option');
        option.dataset.idProduto = produto.id_produto;
        option.value = produto.nome;
        produtosList.appendChild(option);
    });
}
function adicionarOuvintesDeEventos() {
    document.getElementById('id_taxa_entrega').addEventListener('input', calcularTroco);
    document.getElementById('id_desconto').addEventListener('input', calcularTroco);
    document.getElementById('id_valor_pago').addEventListener('input', calcularTroco);
    document.getElementById('id_forma_pagamento').addEventListener('change', forma_pagamento);
    document.getElementById('id_metodo_entrega').addEventListener('change', metodo_entrega);
    document.getElementById('id_loja').addEventListener('change', select_loja);
    document.getElementById('produtoInput').addEventListener('input', detectarSelecaoProduto);
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

    const listaProdutos = document.getElementById("listaProdutos");
    const observer = new MutationObserver(observerCallback);
    observer.observe(listaProdutos, observerOptions);
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

function Ouvinte(){
    var produtoInput = document.getElementById("produtoInput");
    var produtoSelecionado = null;
    var produtoId = produtoInput.getAttribute("data-id-produto");
    // Itera sobre a lista de produtos para encontrar o produto selecionado
// Variável de controle para indicar se o loop deve continuar ou parar
    let continuarLoop = true;
    // Verificar as condições do produto
    if (produtoInput.value == "") {
        alertCustomer("Selecione um produto da lista de sugestões..");
        continuarLoop = false; // Definir para false para parar o loop
        return;
    }
    produtos_data = Utils.getLocalStorageItem('data_produtos');
    // Iterar sobre a lista de produtos
    produtos_data.forEach(function(produto) {
        // Verificar se o loop deve continuar
        if (!continuarLoop) {
            return; // Se não, saia do loop
        }
        
                if (produto.id_produto == produtoId ) {
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
    if (produtoSelecionado != null ) {
        var itensLista = listaProdutos.querySelectorAll(".list-group-item");
        var produtoExistente = false;

        
        // Itera sobre os itens da lista para verificar se o produto já está na lista
        itensLista.forEach(function (item) {
            var idExistente = item.getAttribute("data-id-produto");
                
            if (idExistente === produtoId ) {
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
            novoItemLista.classList.add("list-group-item",'item-list-carrinho',"bg-dark","text-white","fw-bold", "d-flex", "justify-content-between", "align-items-center");
            novoItemLista.setAttribute("data-id-produto", produtoSelecionado.id_produto);
            novoItemLista.setAttribute("data-retornavel", produtoSelecionado.is_retornavel); 
            novoItemLista.setAttribute("data-valor", produtoSelecionado.valor);
            // Preenche o HTML do novo item na lista de produtos
            novoItemLista.innerHTML = `
                <span class="badge text-bg-primary me-1 rounded-pill quantidade">1</span>
                <span class="text-small small my-auto " style="font-size: 0.8rem;" >${produtoSelecionado.nome} R$ ${produtoSelecionado.preco_venda} Unidade</span>
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
    verificarListaProdutos();
}
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
        setTextContent("txt_valor_apagar", parseFloat(venda.valor_total).toFixed(2));
        setElementValue("id_taxa_entrega", parseFloat(venda.valor_entrega).toFixed(2));
        setElementValue("id_valor_pago", parseFloat(venda.valor_pago).toFixed(2));
        setTextContent("txt_troco", parseFloat(venda.troco).toFixed(2));
        setElementValue("id_descricao", venda.descricao);
        setElementValue("id_loja", venda.loja_id);

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
            var ul_produtos = document.getElementById("listaProdutos");
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
                listaProdutos.appendChild(novoItemLista);
            });
            calcularValorTotal();
        }
        else {
            alertCustomer(response.message);
        }
    });
    chamarFuncaoPython("/api/cliente/by/venda/" + id_venda, {}, "GET", function(response) {
        if (response.success === true) {
            toggleGestaoCliente(1);
            montarInfoCliente(response.cliente,"info_cliente");
        }  
    });
 
    
    chamarFuncaoPython("/api/retornaveis/by/venda/" + id_venda, {}, "GET", function(response) {
        if (response.success === true) {
            if(response.list_retornaveis.length >0){
                response.list_retornaveis.forEach(obj => {
                    gerarInputs(1, obj);
                });
            } 
        } 
    });

}