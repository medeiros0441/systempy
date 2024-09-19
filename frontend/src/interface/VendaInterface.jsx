// src/interface/ItemCompraInterface.js
import CustomInterface from './CustomInterface';
export
    class VendaInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);

        this.id_venda = data.id_venda || '';
        this.data_venda = data.data_venda || '';
        this.tipo_pagamento = data.tipo_pagamento || null;
        this.forma_pagamento = data.forma_pagamento || '';
        this.estado_transacao = data.estado_transacao || '';
        this.metodo_entrega = data.metodo_entrega || '';
        this.desconto = data.desconto || '';
        this.valor_total = data.valor_total || 0;
        this.valor_entrega = data.valor_entrega || '';
        this.valor_pago = data.valor_pago || null;
        this.troco = data.troco || null;
        this.descricao = data.descricao || '';
        this.usuario = data.usuario || null; // Assumindo que é um ID ou objeto
        this.loja = data.loja || null; // Assumindo que é um ID ou objeto
        this.cliente = data.cliente || null; // Assumindo que é um ID ou objeto
        this.produtos = data.produtos || []; // Assumindo que é uma lista de IDs ou objetos
        this.nota_fiscal = data.nota_fiscal || null;
    }

    static fromApiResponse(data) {
        return new VendaInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_venda: this.id_venda,
            data_venda: this.data_venda,
            tipo_pagamento: this.tipo_pagamento,
            forma_pagamento: this.forma_pagamento,
            estado_transacao: this.estado_transacao,
            metodo_entrega: this.metodo_entrega,
            desconto: this.desconto,
            valor_total: this.valor_total,
            valor_entrega: this.valor_entrega,
            valor_pago: this.valor_pago,
            troco: this.troco,
            descricao: this.descricao,
            usuario: this.usuario, // Assumindo que é um ID ou objeto
            loja: this.loja, // Assumindo que é um ID ou objeto
            cliente: this.cliente, // Assumindo que é um ID ou objeto
            produtos: this.produtos, // Assumindo que é uma lista de IDs ou objetos
            nota_fiscal: this.nota_fiscal,
        };
    }

    getTipoPagamentoDisplay() {
        const tipoPagamentoChoices = {
            1: "Dinheiro",
            2: "Máquina de Crédito",
            3: "Máquina de Débito",
            4: "PIX",
            5: "Fiado",
            6: "Boleto",
        };
        return tipoPagamentoChoices[this.tipo_pagamento] || "Desconhecido";
    }
}
export class ItemCompraInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);

        this.id_item_compra = data.id_item_compra || '';
        this.venda = data.venda || null; // Assumindo que é um ID ou objeto
        this.produto = data.produto || null; // Assumindo que é um ID ou objeto
        this.quantidade = data.quantidade || 0;
        this.valor_unidade = data.valor_unidade || 0;
    }

    static fromApiResponse(data) {
        return new ItemCompraInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_item_compra: this.id_item_compra,
            venda: this.venda, // Assumindo que é um ID ou objeto
            produto: this.produto, // Assumindo que é um ID ou objeto
            quantidade: this.quantidade,
            valor_unidade: this.valor_unidade,
        };
    }
}

