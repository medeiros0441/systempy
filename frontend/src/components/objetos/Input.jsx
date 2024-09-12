// Input.js
import React, { forwardRef } from 'react';
import PropTypes from 'prop-types';

const Input = forwardRef(({ id, name, type = 'text', label, value, onChange, className = '', ...props }, ref) => {
    return (
        <div className={`form-floating mb-2 ${className}`}>
            <input
                type={type}
                className="form-control"
                id={id}
                name={name}
                value={value}
                onChange={onChange}
                ref={ref}
                {...props}
            />
            <label htmlFor={id}>{label}</label>
        </div>
    );
});

Input.propTypes = {
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    type: PropTypes.string,
    label: PropTypes.string.isRequired,
    value: PropTypes.string,
    onChange: PropTypes.func,
    className: PropTypes.string,
};

Input.defaultProps = {
    type: 'text',
    value: '',
    onChange: () => { },
    className: '',
};

export default Input;
