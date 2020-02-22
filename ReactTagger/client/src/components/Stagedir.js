import React, {Component} from "react";

export default class Stagedir extends Component{
    render () {
        return (
            <p className="Stagedir">
                {this.props.dir}
            </p>
        );
    }
}