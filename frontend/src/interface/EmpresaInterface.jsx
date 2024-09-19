// src/interface/EmpresaInterface.js
import CustomInterface from './CustomInterface';


export default class EmpresaInterface extends CustomInterface {
    constructor(data = {}) {
        // Chamando o construtor da classe base para inicializar 'created' e 'updated'
        super(data);

        // Inicializações específicas para EmpresaInterface
        this.id_empresa = data.id_empresa || '';
        this.nome_empresa = data.nome_empresa || '';
        this.nro_cnpj = data.nro_cnpj || '';
        this.razao_social = data.razao_social || '';
        this.descricao = data.descricao || '';
        this.nome_responsavel = data.nome_responsavel || '';
        this.cargo = data.cargo || '';
        this.email = data.email || '';
        this.nro_cpf = data.nro_cpf || '';
        this.telefone = data.telefone || '';
    }

    static fromApiResponse(data) {
        return new EmpresaInterface(data);
    }

    toApiPayload() {
        // Retorna tanto os dados da classe base quanto os da EmpresaInterface
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_empresa: this.id_empresa,
            nome_empresa: this.nome_empresa,
            nro_cnpj: this.nro_cnpj,
            razao_social: this.razao_social,
            descricao: this.descricao,
            nome_responsavel: this.nome_responsavel,
            cargo: this.cargo,
            email: this.email,
            nro_cpf: this.nro_cpf,
            telefone: this.telefone,
        };
    }
}
