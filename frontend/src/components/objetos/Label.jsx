// Label.js
import React from 'react';
import PropTypes from 'prop-types';

const Label = ({ htmlFor, value, iconClass }) => {
    return (
        <div className="form-group">
            <label className="col-auto col-form-label fw-bold pe-1" htmlFor={htmlFor}>
                {iconClass && <i className={`bi me-2 bi-${iconClass}`}></i>}
                {value}
            </label>
            <span id={htmlFor}>{value}</span>
        </div>
    );
};

Label.propTypes = {
    htmlFor: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    iconClass: PropTypes.string,
};

Label.defaultProps = {
    iconClass: '',
};

export default Label;
