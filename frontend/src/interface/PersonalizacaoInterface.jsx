// src/interface/PersonalizacaoInterface.js
import CustomInterface from './CustomInterface';


export default class PersonalizacaoInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para PersonalizacaoInterface
        this.id_personalizacao = data.id_personalizacao || '';
        this.usuario = data.usuario || ''; // Presumivelmente um ID ou objeto
        this.chave = data.chave || '';
        this.valor = data.valor || '';
        this.descricao = data.descricao || '';
        this.descricao_interna = data.descricao_interna || '';
        this.codigo = data.codigo || '';
    }

    static fromApiResponse(data) {
        return new PersonalizacaoInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da PersonalizacaoInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_personalizacao: this.id_personalizacao,
            usuario: this.usuario, // Presumivelmente um ID ou objeto
            chave: this.chave,
            valor: this.valor,
            descricao: this.descricao,
            descricao_interna: this.descricao_interna,
            codigo: this.codigo,
        };
    }
}

