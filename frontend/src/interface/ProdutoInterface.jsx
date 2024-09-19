// src/interface/ProdutoInterface.js
import CustomInterface from './CustomInterface';

class ProdutoInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);

        this.id_produto = data.id_produto || '';
        this.nome = data.nome || '';
        this.quantidade_atual_estoque = data.quantidade_atual_estoque || 0;
        this.quantidade_minima_estoque = data.quantidade_minima_estoque || 0;
        this.codigo = data.codigo || 0;
        this.is_retornavel = data.is_retornavel || null;
        this.status = data.status || null;
        this.data_validade = data.data_validade || '';
        this.preco_compra = data.preco_compra || 0;
        this.preco_venda = data.preco_venda || 0;
        this.fabricante = data.fabricante || '';
        this.descricao = data.descricao || '';
        this.loja = data.loja || null; // Assumindo que é um ID ou objeto
    }

    static fromApiResponse(data) {
        return new ProdutoInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_produto: this.id_produto,
            nome: this.nome,
            quantidade_atual_estoque: this.quantidade_atual_estoque,
            quantidade_minima_estoque: this.quantidade_minima_estoque,
            codigo: this.codigo,
            is_retornavel: this.is_retornavel,
            status: this.status,
            data_validade: this.data_validade,
            preco_compra: this.preco_compra,
            preco_venda: this.preco_venda,
            fabricante: this.fabricante,
            descricao: this.descricao,
            loja: this.loja, // Assumindo que é um ID ou objeto
        };
    }
}

export default ProdutoInterface;

