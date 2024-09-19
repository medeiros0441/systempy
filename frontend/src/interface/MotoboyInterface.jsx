
import CustomInterface from './CustomInterface';

export default class MotoboyInterface extends CustomInterface {
    constructor(data = {}) {
        super(data);

        this.id_motoboy = data.id_motoboy || '';
        this.nome = data.nome || '';
        this.numero = data.numero || '';
        this.empresa = data.empresa || null; // Assumindo que é um ID ou objeto
    }

    static fromApiResponse(data) {
        return new MotoboyInterface(data);
    }

    toApiPayload() {
        return {
            ...super.toApiPayload(), // Inclui 'created' e 'updated' da classe base
            id_motoboy: this.id_motoboy,
            nome: this.nome,
            numero: this.numero,
            empresa: this.empresa, // Assumindo que é um ID ou objeto
        };
    }
}