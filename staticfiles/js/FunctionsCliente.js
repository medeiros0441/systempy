// Função para criar um cliente
function criarCliente(data, callback) {
    const url = '/api/cliente/create/';
    chamarFuncaoPython(url, data, 'POST', function(response) {
        if (response.success) {
            callback(response, null); // Chamando o callback com os dados do cliente e sem erro
        } else {
            console.error('Erro ao criar cliente:', response.error);
            callback(null, response.error); // Chamando o callback sem dados do cliente e com o erro
        }
    } );
}

// Função para obter um cliente por ID
function obterClientePorId(clienteId,  callback) {
    const url = `/api/cliente/${clienteId}/`;
    chamarFuncaoPython(url, null,'GET', function(response) {
        if (response.success) {
            callback(response.data, null); // Chamando o callback com os dados do cliente e sem erro
        } else {
            console.error('Erro ao obter cliente:', response.error);
            callback(null, response.error); // Chamando o callback sem dados do cliente e com o erro
        }
    });
}

// Função para atualizar um cliente
function atualizarCliente(clienteId, data, callback) {
    const url = `/api/cliente/${clienteId}/update/`;
    chamarFuncaoPython(url, data,"PUT", function(response) {
        if (response.success) {
           
            callback(response.data, null); // Chamando o callback com os dados do cliente atualizado e sem erro
        } else {
            console.error('Erro ao atualizar cliente:', response.error);
            callback(null, response.error); // Chamando o callback sem dados do cliente atualizado e com o erro
        }
    });
}

// Função para excluir um cliente
function excluirCliente(clienteId, callback) {
    const url = `/api/cliente/${clienteId}/delete/`;
    chamarFuncaoPython(url, null, function(response) {
        if (response.success) {
            console.log('Cliente excluído com sucesso');
            callback(null); // Chamando o callback sem erro
        } else {
            console.error('Erro ao excluir cliente:', response.error);
            callback(response.error); // Chamando o callback com o erro
        }
    }, 'DELETE');
}

// Função para obter clientes por empresa
function obterClientesPorEmpresa(callback) {
    const url = '/api/cliente/by_empresa/';
    chamarFuncaoPython(url, null, 'GET', function(response) {
        if (response.success) {
            
            callback(response.data, null); // Chamando o callback com os dados dos clientes e sem erro
        } else {
            console.error('Erro ao obter clientes:', response.error);
            callback(null, response.error); // Chamando o callback sem dados dos clientes e com o erro
        }
    });
}
