// Função para listar motoboys por empresa
function listarMotoboysPorEmpresa() {
    $.ajax({
        url: '/api/motoboys/empresa/', // URL da view que lista motoboys por empresa
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log(data); // Manipular os dados retornados, por exemplo, renderizar uma tabela com os motoboys
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText); // Manipular erros, por exemplo, exibir uma mensagem de erro
        }
    });
}

// Função para criar um novo motoboy
function criarMotoboy(data) {
    $.ajax({
        url: '/api/motoboy/create/', // URL da view para criar um motoboy
        type: 'POST',
        dataType: 'json',
        data: data,
        success: function(response) {
            console.log(response); // Manipular a resposta, por exemplo, exibir uma mensagem de sucesso
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText); // Manipular erros, por exemplo, exibir uma mensagem de erro
        }
    });
}

// Função para atualizar um motoboy existente
function atualizarMotoboy(id, data) {
    $.ajax({
        url: `/api/motoboy/${id}/update/`, // URL da view para atualizar um motoboy
        type: 'PUT',
        dataType: 'json',
        data: data,
        success: function(response) {
            console.log(response); // Manipular a resposta, por exemplo, exibir uma mensagem de sucesso
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText); // Manipular erros, por exemplo, exibir uma mensagem de erro
        }
    });
}

// Função para excluir um motoboy
function excluirMotoboy(id) {
    $.ajax({
        url: `/api/motoboy/${id}/delete/`, // URL da view para excluir um motoboy
        type: 'DELETE',
        dataType: 'json',
        success: function(response) {
            console.log(response); // Manipular a resposta, por exemplo, exibir uma mensagem de sucesso
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText); // Manipular erros, por exemplo, exibir uma mensagem de erro
        }
    });
}
