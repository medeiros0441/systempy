// src/interface/PdvAndAssociadoInterface.js

import CustomInterface from './CustomInterface';

export class PdvInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);
        this.id_pdv = data.id_pdv || '';
        this.nome = data.nome || '';
        this.loja = data.loja || null; // Assumindo que é um objeto ou ID
        this.saldo_inicial = data.saldo_inicial || 0;
        this.status_operacao = data.status_operacao || PdvInterface.FECHADO;
    }

    static fromApiResponse(data) {
        return new PdvInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(),
            id_pdv: this.id_pdv,
            nome: this.nome,
            loja: this.loja,
            saldo_inicial: this.saldo_inicial,
            status_operacao: this.status_operacao,
        };
    }
}


export class RegistroDiarioPdvInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);
        this.id_registro_diario = data.id_registro_diario || '';
        this.pdv = data.pdv || null; // Assumindo que é um objeto ou ID
        this.dia = data.dia || '';
        this.saldo_inicial_dinheiro = data.saldo_inicial_dinheiro || 0;
        this.saldo_final_dinheiro = data.saldo_final_dinheiro || null;
        this.saldo_final_total = data.saldo_final_total || null;
        this.maquina_tipo = data.maquina_tipo || '';
        this.saldo_final_maquina = data.saldo_final_maquina || null;
        this.horario_iniciou = data.horario_iniciou || '';
        this.horario_fechamento = data.horario_fechamento || '';
        this.descricao_interna = data.descricao_interna || '';
    }

    static fromApiResponse(data) {
        return new RegistroDiarioPdvInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(),
            id_registro_diario: this.id_registro_diario,
            pdv: this.pdv,
            dia: this.dia,
            saldo_inicial_dinheiro: this.saldo_inicial_dinheiro,
            saldo_final_dinheiro: this.saldo_final_dinheiro,
            saldo_final_total: this.saldo_final_total,
            maquina_tipo: this.maquina_tipo,
            saldo_final_maquina: this.saldo_final_maquina,
            horario_iniciou: this.horario_iniciou,
            horario_fechamento: this.horario_fechamento,
            descricao_interna: this.descricao_interna,
        };
    }
}


export class TransacaoPdvInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);
        this.id_transacao = data.id_transacao || '';
        this.registro_diario = data.registro_diario || null; // Assumindo que é um objeto ou ID
        this.venda = data.venda || null; // Assumindo que é um objeto ou ID
        this.valor = data.valor || 0;
        this.descricao = data.descricao || '';
        this.tipo_operacao = data.tipo_operacao || null;
        this.tipo_pagamento = data.tipo_pagamento || null;
    }

    static fromApiResponse(data) {
        return new TransacaoPdvInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(),
            id_transacao: this.id_transacao,
            registro_diario: this.registro_diario,
            venda: this.venda,
            valor: this.valor,
            descricao: this.descricao,
            tipo_operacao: this.tipo_operacao,
            tipo_pagamento: this.tipo_pagamento,
        };
    }
}

export class AssociadoPdvInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);
        this.id_associado = data.id_associado || '';
        this.status_acesso = data.status_acesso || null;
        this.usuario = data.usuario || null; // Assumindo que é um objeto ou ID
        this.pdv = data.pdv || null; // Assumindo que é um objeto ou ID
    }

    static fromApiResponse(data) {
        return new AssociadoPdvInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(),
            id_associado: this.id_associado,
            status_acesso: this.status_acesso,
            usuario: this.usuario,
            pdv: this.pdv,
        };
    }
}
