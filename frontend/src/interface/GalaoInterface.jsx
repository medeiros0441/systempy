// src/interface/GalaoInterface.js
import CustomInterface from './CustomInterface';

export class GalaoInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para GalaoInterface
        this.id_galao = data.id_galao || '';
        this.data_validade = data.data_validade || '';
        this.data_fabricacao = data.data_fabricacao || '';
        this.descricao = data.descricao || '';
        this.quantidade = data.quantidade || 0;
        this.titulo = data.titulo || '';
        this.loja = data.loja || null; // Assumindo que é um objeto ou ID
    }

    static fromApiResponse(data) {
        return new GalaoInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da GalaoInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_galao: this.id_galao,
            data_validade: this.data_validade,
            data_fabricacao: this.data_fabricacao,
            descricao: this.descricao,
            quantidade: this.quantidade,
            titulo: this.titulo,
            loja: this.loja, // Assumindo que é um ID ou objeto
        };
    }
}

export class GestaoGalaoInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para GestaoGalaoInterface
        this.id_gestao_galao = data.id_gestao_galao || '';
        this.galao_saiu = data.galao_saiu || null; // Assumindo que é um objeto ou ID
        this.galao_entrando = data.galao_entrando || null; // Assumindo que é um objeto ou ID
        this.venda = data.venda || null; // Assumindo que é um objeto ou ID
        this.descricao = data.descricao || '';
    }

    static fromApiResponse(data) {
        return new GestaoGalaoInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da GestaoGalaoInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_gestao_galao: this.id_gestao_galao,
            galao_saiu: this.galao_saiu, // Assumindo que é um ID ou objeto
            galao_entrando: this.galao_entrando, // Assumindo que é um ID ou objeto
            venda: this.venda, // Assumindo que é um ID ou objeto
            descricao: this.descricao,
        };
    }
}
