
import CustomInterface from './CustomInterface';

export default class LogInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);
        this.id_log = data.id_log || '';
        this.tipo = data.tipo || '';
        this.origem = data.origem || '';
        this.descricao = data.descricao || '';
        this.usuario = data.usuario || null; // Assumindo que é um objeto ou ID
        this.ip_usuario = data.ip_usuario || '';
    }

    static fromApiResponse(data) {
        return new LogInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(),
            id_log: this.id_log,
            tipo: this.tipo,
            origem: this.origem,
            descricao: this.descricao,
            usuario: this.usuario,
            ip_usuario: this.ip_usuario,
        };
    }
} 