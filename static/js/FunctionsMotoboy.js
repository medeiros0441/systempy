
function listarMotoboysPorEmpresa() {
    return fetch('/listar_motoboys_por_empresa/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // Se você estiver usando autenticação, adicione os cabeçalhos necessários aqui.
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            return { success: true, data: data.motoboys };
        } else {
            throw new Error(data.message);
        }
    })
    .catch(error => {
        throw new Error('Ocorreu um erro ao listar motoboys: ' + error.message);
    });
}

// Função para criar um motoboy
function createMotoboy(nome, numero) {
    return fetch('/create_motoboy/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            // Se você estiver usando autenticação, adicione os cabeçalhos necessários aqui.
        },
        body: new URLSearchParams({
            'nome': nome,
            'numero': numero
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alertCustomer('Motoboy criado com sucesso. ');
            return { success: true, data: data };
        } else if (data.status === 'error') {
            alertCustomer(data.message);
            return { success: false, data: data };
        }
    })
    .catch(error => {
        alertCustomer('Ocorreu um erro ao criar o motoboy: ' + error.message);
        return { success: false, data: null };
    });
}

// Função para atualizar um motoboy
function updateMotoboy(idMotoboy, nome, numero) {
    return fetch(`/update_motoboy/${idMotoboy}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            // Se você estiver usando autenticação, adicione os cabeçalhos necessários aqui.
        },
        body: new URLSearchParams({
            'nome': nome,
            'numero': numero
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alertCustomer('Motoboy atualizado com sucesso.');
            return { success: true, data: data };
        } else if (data.status === 'error') {
            alertCustomer(data.message);
            return { success: false, data: data };
        }
    })
    .catch(error => {
        alertCustomer('Ocorreu um erro ao atualizar o motoboy: ' + error.message);
        return { success: false, data: null };
    });
}

// Função para excluir um motoboy
function deleteMotoboy(idMotoboy) {
    return fetch(`/delete_motoboy/${idMotoboy}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            // Se você estiver usando autenticação, adicione os cabeçalhos necessários aqui.
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alertCustomer('Motoboy excluído com sucesso.');
            return { success: true, data: data };
        } else if (data.status === 'error') {
            alertCustomer(data.message);
            return { success: false, data: data };
        }
    })
    .catch(error => {
        alertCustomer('Ocorreu um erro ao excluir o motoboy: ' + error.message);
        return { success: false, data: null };
    });
}