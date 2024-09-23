import request from '@utils/api';

const UsuarioService = {
    // Método para criar um novo usuário
    async createUsuario(usuarioData) {
        const data = { usuario: usuarioData };
        const response = await request('usuarios', 'POST', data);
        return response;
    },

    // Método para obter todos os usuários
    async getAllUsuarios() {
        const response = await request('usuarios', 'GET');
        return response;
    },

    // Método para obter usuários por empresa

    async getUsuariosByEmpresa(id_empresa = null) {
        const url = id_empresa ? `usuarios/empresa/${id_empresa}` : 'usuarios/empresa';
        const response = await request(url, 'GET');
        return response;
    },


    // Método para obter um usuário por ID
    async getUsuarioById(usuarioId) {
        const response = await request(`usuarios/${usuarioId}`, 'GET');
        return response;
    },

    // Método para excluir um usuário
    async deleteUsuario(usuarioId) {
        const response = await request(`usuarios/${usuarioId}`, 'DELETE');
        return response;
    },

    // Método para atualizar um usuário
    async updateUsuario(usuarioId, usuarioData) {
        const data = { usuario: usuarioData };
        const response = await request(`usuarios/${usuarioId}`, 'PUT', data);
        return response;
    },
};

export default UsuarioService;
