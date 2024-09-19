

import CustomInterface from './CustomInterface';
export class LojaInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);
        this.id_loja = data.id_loja || '';
        this.nome = data.nome || '';
        this.numero_telefone = data.numero_telefone || '';
        this.horario_operacao_inicio = data.horario_operacao_inicio || null;
        this.horario_operacao_fim = data.horario_operacao_fim || null;
        this.segunda = data.segunda || false;
        this.terca = data.terca || false;
        this.quarta = data.quarta || false;
        this.quinta = data.quinta || false;
        this.sexta = data.sexta || false;
        this.sabado = data.sabado || false;
        this.domingo = data.domingo || false;
        this.empresa = data.empresa || null; // Assumindo que é um objeto ou ID
        this.endereco = data.endereco || null; // Assumindo que é um objeto ou ID
    }

    static fromApiResponse(data) {
        return new LojaInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(),
            id_loja: this.id_loja,
            nome: this.nome,
            numero_telefone: this.numero_telefone,
            horario_operacao_inicio: this.horario_operacao_inicio,
            horario_operacao_fim: this.horario_operacao_fim,
            segunda: this.segunda,
            terca: this.terca,
            quarta: this.quarta,
            quinta: this.quinta,
            sexta: this.sexta,
            sabado: this.sabado,
            domingo: this.domingo,
            empresa: this.empresa,
            endereco: this.endereco,
        };
    }
}

export class AssociadoInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);
        this.id_associado = data.id_associado || '';
        this.status_acesso = data.status_acesso || null;
        this.usuario = data.usuario || null; // Assumindo que é um objeto ou ID
        this.loja = data.loja || null; // Assumindo que é um objeto ou ID
    }

    static fromApiResponse(data) {
        return new AssociadoInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(),
            id_associado: this.id_associado,
            status_acesso: this.status_acesso,
            usuario: this.usuario,
            loja: this.loja,
        };
    }
}
