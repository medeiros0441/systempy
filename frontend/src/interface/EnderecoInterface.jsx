// src/interface/EnderecoInterface.js
import CustomInterface from './CustomInterface';

class EnderecoInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para EnderecoInterface
        this.id_endereco = data.id_endereco || '';
        this.id = data.id || '';
        this.rua = data.rua || '';
        this.numero = data.numero || '';
        this.bairro = data.bairro || '';
        this.cidade = data.cidade || '';
        this.estado = data.estado || '';
        this.codigo_postal = data.codigo_postal || '';
        this.descricao = data.descricao || '';
    }

    static fromApiResponse(data) {
        return new EnderecoInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da EnderecoInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_endereco: this.id_endereco,
            id: this.id,
            rua: this.rua,
            numero: this.numero,
            bairro: this.bairro,
            cidade: this.cidade,
            estado: this.estado,
            codigo_postal: this.codigo_postal,
            descricao: this.descricao,
        };
    }
}

export default EnderecoInterface;
