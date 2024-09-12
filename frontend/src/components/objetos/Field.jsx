
// Componente genérico para renderizar campos com base no modo de exibição/edição
const Field = ({ icon, label, value, isViewMode, onChange, type = "text", name, textarea = false }) => (
    <div className="col-12 mb-2">
        <i className={`bi ${icon} me-1`}></i>
        <span className="fw-bold">{label}: </span>
        {isViewMode ? (
            <span>{value || "Não informado"}</span>
        ) : textarea ? (
            <textarea
                className="form-control"
                name={name}
                value={value}
                onChange={onChange}
            ></textarea>
        ) : (
            <input
                type={type}
                className="form-control"
                name={name}
                value={value}
                onChange={onChange}
            />
        )}
    </div>
);
