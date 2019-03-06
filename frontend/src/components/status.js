import React from "react";
import "./status.css";
import PropTypes from "prop-types";

function status(props) {
    return (
        <div className="status">
            <span>{props.name}</span>
        </div>
    );
}
status.propTypes = {
    name: PropTypes.string.isRequired
};

export default status;