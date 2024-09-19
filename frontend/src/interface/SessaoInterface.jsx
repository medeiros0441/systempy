// src/interface/SessaoInterface.js
import CustomInterface from './CustomInterface';

class SessaoInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);

        this.id_sessao = data.id_sessao || '';
        this.id = data.id || '';
        this.ip_sessao = data.ip_sessao || '';
        this.descricao = data.descricao || '';
        this.pagina_atual = data.pagina_atual || '';
        this.time_iniciou = data.time_iniciou || null;
        this.status = data.status || true;
        this.cidade = data.cidade || '';
        this.regiao = data.regiao || '';
        this.pais = data.pais || '';
        this.codigo_postal = data.codigo_postal || '';
        this.organizacao = data.organizacao || '';
        this.usuario = data.usuario || null; // Assumindo que é um ID ou objeto
    }

    static fromApiResponse(data) {
        return new SessaoInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_sessao: this.id_sessao,
            id: this.id,
            ip_sessao: this.ip_sessao,
            descricao: this.descricao,
            pagina_atual: this.pagina_atual,
            time_iniciou: this.time_iniciou,
            status: this.status,
            cidade: this.cidade,
            regiao: this.regiao,
            pais: this.pais,
            codigo_postal: this.codigo_postal,
            organizacao: this.organizacao,
            usuario: this.usuario, // Assumindo que é um ID ou objeto
        };
    }
}

export default SessaoInterface;
