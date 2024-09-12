import React from 'react';

import Input from 'src/components/objetos/Input';
import Label from 'src/components/objetos/Label';

// Classe ClienteInterface
class ClienteInterface {
    constructor(data) {
        this.id_cliente = data.id_cliente || '';
        this.nome = data.nome || '';
        this.telefone = data.telefone || '';
        this.ultima_compra = data.ultima_compra || '';
        this.tipo_cliente = data.tipo_cliente || '';
        this.descricao = data.descricao || '';
        this.endereco = data.endereco || '';
        this.empresa = data.empresa || '';

        // Criando refs para os inputs
        this.refs = {
            id_cliente: React.createRef(),
            nome: React.createRef(),
            telefone: React.createRef(),
            ultima_compra: React.createRef(),
            tipo_cliente: React.createRef(),
            descricao: React.createRef(),
            endereco: React.createRef(),
            empresa: React.createRef(),
        };
    }

    static fromApiResponse(data) {
        return new ClienteInterface(data);
    }

    toApiPayload() {
        return {
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

    // Método para capturar os valores dos inputs
    getInputsValue() {
        return new ClienteInterface({
            id_cliente: this.refs.id_cliente.current.value,
            nome: this.refs.nome.current.value,
            telefone: this.refs.telefone.current.value,
            ultima_compra: this.refs.ultima_compra.current.value,
            tipo_cliente: this.refs.tipo_cliente.current.value,
            descricao: this.refs.descricao.current.value,
            endereco: this.refs.endereco.current.value,
            empresa: this.refs.empresa.current.value,
        });
    }

    // Método para gerar labels
    generateLabels() {
        return (
            <>
                <Label htmlFor="id_cliente" value="ID Cliente" iconClass="info-circle" />
                <Label htmlFor="nome" value="Nome do Cliente" iconClass="person-circle" />
                <Label htmlFor="telefone" value="Telefone" iconClass="phone" />
                <Label htmlFor="ultima_compra" value="Última Compra" iconClass="calendar" />
                <Label htmlFor="tipo_cliente" value="Tipo de Cliente" iconClass="card-checklist" />
                <Label htmlFor="descricao" value="Descrição" iconClass="file-text" />
                <Label htmlFor="endereco" value="Endereço" iconClass="geo-alt" />
                <Label htmlFor="empresa" value="Empresa" iconClass="building" />
            </>
        );
    }

    // Método para gerar inputs
    generateInputs() {
        return (
            <>
                <Input id="id_cliente" name="id_cliente" value={this.id_cliente} ref={this.refs.id_cliente} />
                <Input id="nome" name="nome" value={this.nome} ref={this.refs.nome} />
                <Input id="telefone" name="telefone" type="tel" value={this.telefone} ref={this.refs.telefone} />
                <Input id="ultima_compra" name="ultima_compra" type="datetime-local" value={this.ultima_compra} ref={this.refs.ultima_compra} />
                <Input id="tipo_cliente" name="tipo_cliente" value={this.tipo_cliente} ref={this.refs.tipo_cliente} />
                <Input id="descricao" name="descricao" value={this.descricao} ref={this.refs.descricao} />
                <Input id="endereco" name="endereco" value={this.endereco} ref={this.refs.endereco} />
                <Input id="empresa" name="empresa" value={this.empresa} ref={this.refs.empresa} />
            </>
        );
    }
}

export default ClienteInterface;
