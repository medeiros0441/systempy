// src/interface/UsuarioInterface.js
import CustomInterface from './CustomInterface';

export default class UsuarioInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para UsuarioInterface
        this.id_usuario = data.id_usuario || '';
        this.nome_completo = data.nome_completo || '';
        this.nome_usuario = data.nome_usuario || '';
        this.senha = data.senha || '';
        this.nivel_usuario = data.nivel_usuario || 0;
        this.status_acesso = data.status_acesso || false;
        this.email = data.email || '';
        this.ultimo_login = data.ultimo_login || null;
        this.empresa = data.empresa || ''; // Presumivelmente um ID ou objeto
    }

    static fromApiResponse(data) {
        return new UsuarioInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da UsuarioInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_usuario: this.id_usuario,
            nome_completo: this.nome_completo,
            nome_usuario: this.nome_usuario,
            senha: this.senha,
            nivel_usuario: this.nivel_usuario,
            status_acesso: this.status_acesso,
            email: this.email,
            ultimo_login: this.ultimo_login,
            empresa: this.empresa, // Presumivelmente um ID ou objeto
        };
    }
}

