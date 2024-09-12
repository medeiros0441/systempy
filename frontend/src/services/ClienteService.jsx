import request from '../utils/api';

const ClienteService = {
    // Método para criar um novo cliente
    async createCliente(clienteData) {
        const data = {
            cliente: clienteData
        };
        const response = await request('clientes', 'POST', data);
        return response;
    },

    // Método para atualizar um cliente existente
    async updateCliente(id_cliente, clienteData) {
        const data = {
            cliente: clienteData
        };
        const response = await request(`clientes/${id_cliente}`, 'PUT', data);
        return response;
    },

    // Método para buscar os detalhes de um cliente pelo ID
    async getCliente(id_cliente) {
        const response = await request(`clientes/${id_cliente}/detalhes`, 'GET');
        return response;
    },

    // Método para excluir um cliente
    async deleteCliente(id_cliente) {
        const response = await request(`clientes/${id_cliente}/excluir`, 'DELETE');
        return response;
    },

    // Método para buscar todos os clientes de uma empresa
    async getClientesByEmpresa() {
        const response = await request(`clientes/clientes-empresa`, 'GET');
        return response;
    },

    // Método para buscar todas as vendas de um cliente pelo ID
    async getVendasByCliente(id_cliente) {
        const response = await request(`clientes/${id_cliente}/vendas`, 'GET');
        return response;
    }
};

export default ClienteService;
