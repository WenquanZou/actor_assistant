import React, {Component} from "react";
import Stagedir from "./Stagedir";
import {Typography} from "@material-ui/core";

export default class Speech extends Component {
    render() {
        return (
                <div className="speech">
                    <span className="speaker">{this.props.speaker}</span>
                    {this.props.content
                        .map((line, key) => {
                            if (line.type === "stagedir") {
                                return <Stagedir key={key} dir={line.dir}/>
                            } else {
                                return (
                                    <div className="line" key={key}
                                        onMouseDown={this.props.recordStart(line.line_num, this.props.speaker, this.props.publicKey)}
                                        onMouseUp={this.props.recordEnd(line.line_num, this.props.speaker, this.props.publicKey)}
                                        onContextMenu={
                                            this.props.onRightClick(line.line_num, this.props.speaker, line.text)
                                        }>{line.text}
                                    </div>
                                )
                            }
                        })
                    }
                </div>
        );
    }
}