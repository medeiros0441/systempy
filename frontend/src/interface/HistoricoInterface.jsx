// src/interface/HistoricoInterface.js
import CustomInterface from './CustomInterface';

export class HistoricoInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para HistoricoInterface
        this.id_historico = data.id_historico || '';
        this.descricao = data.descricao || '';
        this.usuario = data.usuario || null; // Assumindo que é um ID ou objeto
    }

    static fromApiResponse(data) {
        return new HistoricoInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da HistoricoInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_historico: this.id_historico,
            descricao: this.descricao,
            usuario: this.usuario, // Assumindo que é um ID ou objeto
        };
    }
}


export class HistoricoAlteracoesInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para HistoricoAlteracoesInterface
        this.id_historico = data.id_historico || '';
        this.entidade = data.entidade || '';
        this.entidade_id = data.entidade_id || '';
        this.tipo_alteracao = data.tipo_alteracao || '';
        this.campo_alterado = data.campo_alterado || '';
        this.valor_antigo = data.valor_antigo || '';
        this.valor_novo = data.valor_novo || '';
        this.usuario = data.usuario || null; // Assumindo que é um ID ou objeto
        this.data_alteracao = data.data_alteracao || '';
    }

    static fromApiResponse(data) {
        return new HistoricoAlteracoesInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da HistoricoAlteracoesInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_historico: this.id_historico,
            entidade: this.entidade,
            entidade_id: this.entidade_id,
            tipo_alteracao: this.tipo_alteracao,
            campo_alterado: this.campo_alterado,
            valor_antigo: this.valor_antigo,
            valor_novo: this.valor_novo,
            usuario: this.usuario, // Assumindo que é um ID ou objeto
            data_alteracao: this.data_alteracao,
        };
    }
}
