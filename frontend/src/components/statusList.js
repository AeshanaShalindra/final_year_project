import React from "react";
import Status from "./status";


function statusList(props) {
    return (
        <div>
            {props.status.map(c => <Status name={c.name} key={c.key} />)}
        </div>
    );
}

export default statusList;