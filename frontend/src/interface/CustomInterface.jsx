

export default class CustomInterface {
    constructor(data = {}) {
        this.created = data.created_at || null;
        this.updated = data.updated_at || null;
    }

    static fromApiResponse(data) {
        return new this(data);
    }

    toApiPayload() {
        return {
            created: this.created,
            updated: this.updated,
        };
    }
}
