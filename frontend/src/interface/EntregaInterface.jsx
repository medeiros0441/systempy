// src/interface/EntregaInterface.js
import CustomInterface from './CustomInterface';

export default class EntregaInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);

        this.id_entrega = data.id_entrega || '';
        this.venda = data.venda || null; // Assumindo que é um ID ou objeto
        this.valor_entrega = data.valor_entrega || 0;
        this.time_pedido = data.time_pedido || null;
        this.time_finalizacao = data.time_finalizacao || null;
        this.motoboy = data.motoboy || null; // Assumindo que é um ID ou objeto
        this.descricao = data.descricao || '';
    }

    static fromApiResponse(data) {
        return new EntregaInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_entrega: this.id_entrega,
            venda: this.venda, // Assumindo que é um ID ou objeto
            valor_entrega: this.valor_entrega,
            time_pedido: this.time_pedido,
            time_finalizacao: this.time_finalizacao,
            motoboy: this.motoboy, // Assumindo que é um ID ou objeto
            descricao: this.descricao,
        };
    }
}

