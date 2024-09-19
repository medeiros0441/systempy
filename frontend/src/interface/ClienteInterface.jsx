// src/interface/ClienteInterface.js
import CustomInterface from './CustomInterface';


export default class ClienteInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para ClienteInterface
        this.id_cliente = data.id_cliente || '';
        this.nome = data.nome || '';
        this.telefone = data.telefone || '';
        this.ultima_compra = data.ultima_compra || '';
        this.tipo_cliente = data.tipo_cliente || '';
        this.descricao = data.descricao || '';
        this.endereco = data.endereco || '';
        this.empresa = data.empresa || '';
    }

    static fromApiResponse(data) {
        return new ClienteInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da ClienteInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_cliente: this.id_cliente,
            nome: this.nome,
            telefone: this.telefone,
            ultima_compra: this.ultima_compra,
            tipo_cliente: this.tipo_cliente,
            descricao: this.descricao,
            endereco: this.endereco,
            empresa: this.empresa,
        };
    }
}

