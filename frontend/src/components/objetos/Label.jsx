import React from 'react';

const Label = ({ htmlFor, title, value, iconClass }) => (
    <div className="form-group">
        <label className="col-auto fw-bolder col-form-label fw-bold pe-1" htmlFor={htmlFor}>
            {iconClass && <i className={`bi me-2 bi-${iconClass}`}></i>}
            {title}
        </label>
        {value && <span id={htmlFor}>{value}</span>}
    </div>
);

export default Label;
