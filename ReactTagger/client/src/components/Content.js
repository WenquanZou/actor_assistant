import React, {Component} from 'react';
import {Typography} from '@material-ui/core';
import "../App.css"
import Act from "./Act.js"

class Content extends Component {

    state = {
        annotations: [],
        start: undefined,
        end: undefined,
    };

    storeLineNum = key => (lineNum, speaker, speechKey) => event => {
        if (event.button === 2) return;
        this.setState({[key]: [lineNum, speaker, speechKey]})
    };

    onRightClick = (rightClickLineNum, speaker, content) => (event) => {
        event.preventDefault();

        const {start, end} = this.state;
        let lineStart, lineEnd, lineSpeaker, lineContent;
        if (!start || !end) {
            // just right-click, no text selection
            lineStart = lineEnd = rightClickLineNum;
            lineSpeaker = speaker;
            lineContent = content
        } else {
            if (start[2] !== end[2]) return;

            lineStart = start[0];
            lineEnd = end[0];
            lineSpeaker = start[1];

            // window.getSelection()
            lineContent = 'foo'
        }

        let actionVerb = undefined;
        while (!actionVerb) {
            actionVerb = prompt('Annotate the action verb:').trim()
        }

        this.setState(prevState => {
            const {annotations} = prevState;
            annotations.push({
                lineStart: lineStart,
                lineEnd: lineEnd,
                content: lineContent,
                speaker: lineSpeaker,
                actionVerb: actionVerb
            });

            return {
                start: undefined,
                end: undefined,
                annotations
            }
        })
    };

    showState(event) {
        console.log(this.state.annotations);
        console.log(JSON.stringify(this.state.annotations))
    }

    render() {
        // console.log(this.props.acts[0]);
        return (
            this.props.acts !== undefined && <div>
                <Typography component='h2' variant='h3' align='center'>{this.props.filename}</Typography>
                <div style={{
                    border: '1px solid black',
                    padding: '10px',
                }} onClick={this.showState.bind(this)}>Show state in console log
                </div>
                <div className="scrollable">
                    {this.props.acts.map((act, key) => (
                        <Act key={key} act_num={act.act_num} scenes={act.scenes}
                             recordStart={this.storeLineNum('start').bind(this)}
                             recordEnd={this.storeLineNum('end').bind(this)}
                             onRightClick={this.onRightClick.bind(this)}/>
                    ))}
                </div>
            </div>
        );
    }
}

export default Content;