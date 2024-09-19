import React from 'react';

// Refatorando o Input com React.memo e forwardRef para otimizar a renderização
const Input = (({ id, name, type = 'text', label, value, onChange }) => {
    return (
        <div className={`form-floating mb-2 `}>
            <input
                type={type}
                className="form-control"
                id={id}
                name={name}
                value={value}
                onChange={onChange} // Certifique-se de que onChange está sendo usado corretamente
            />
            <label htmlFor={id}>{label}</label>
        </div>
    );
});

export default Input
