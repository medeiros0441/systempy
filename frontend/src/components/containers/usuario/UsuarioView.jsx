import React, { useEffect, useState } from 'react';
import ClienteInterface from 'src/interface/ClienteInterface';
import ClienteService from 'src/services/ClienteService';
import alerta from 'src/utils/alerta';
import Label from 'src/components/objetos/Label';
import loading from 'src/utils/loading';

const ClienteView = ({ id_cliente }) => {
    const [cliente, setCliente] = useState({});
    const setLoadingState = (valor) => loading(valor, "formulario");

    useEffect(() => {
        const fetchCliente = async () => {
            if (!id_cliente) return;

            try {
                const response = await ClienteService.getCliente(id_cliente);
                if (response.sucesso) {
                    const clienteData = ClienteInterface.fromApiResponse(response.data);
                    setCliente(clienteData);
                } else {
                    alerta(response.message);
                }
            } catch (error) {
                alerta('Erro ao buscar cliente');
            }
        };

        fetchCliente();
    }, [id_cliente]);

    return (
        <div>
            <Label htmlFor="nome" value={`Nome do Cliente: ${cliente.nome}`} />
            <Label htmlFor="telefone" value={`Telefone: ${cliente.telefone}`} />
            <Label htmlFor="tipo_cliente" value={`Tipo de Cliente: ${cliente.tipo_cliente}`} />
            <Label htmlFor="descricao" value={`Descrição: ${cliente.descricao}`} />
            <Label htmlFor="endereco" value={`Endereço: ${cliente.endereco}`} />
        </div>
    );
};

export default ClienteView;
