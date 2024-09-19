import React, { forwardRef } from 'react';
import PropTypes from 'prop-types';

const Select = forwardRef(({ id, name, options = [], value, onChange, className = '', ...props }, ref) => {
    // Verifica se options é um array e não é nulo ou indefinido
    const renderOptions = Array.isArray(options) ? options : [];

    return (
        <div className={`form-floating mb-2 ${className}`}>
            <select
                id={id}
                name={name}
                className="form-control"
                value={value}
                onChange={onChange}
                ref={ref}
                {...props}
            >
                {renderOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
            <label htmlFor={id}>{props.label}</label>
        </div>
    );
});

Select.propTypes = {
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    options: PropTypes.arrayOf(PropTypes.shape({
        value: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
    })).isRequired,
    value: PropTypes.string,
    onChange: PropTypes.func,
    className: PropTypes.string,
    label: PropTypes.string.isRequired,
};

Select.defaultProps = {
    value: '',
    onChange: () => { },
    className: '',
};

export default Select;
