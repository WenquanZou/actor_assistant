import React, {Component} from 'react';
import {TextField, Typography} from '@material-ui/core';
import "../App.css"
import Act from "./Act.js"
import Modal from 'react-modal';
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";

const customStyles = {
    content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
        width: '30vh',
        height: '25vh'
    }
};

class Content extends Component {

    state = {
        annotations: [],
        start: undefined,
        end: undefined,
        modalOpen: false,

        annotation: undefined,
        actionVerb: ''
    };

    storeLineNum = key => (lineNum, speaker, speechKey) => event => {
        if (event.button === 2) return;
        this.setState({[key]: [lineNum, speaker, speechKey]})
    };

    recordActionVerb = event => {
        this.setState({actionVerb: event.target.value})
    };

    saveActionVerb = event => {
        this.setState(prevState => {
            const {annotations} = prevState;
            annotations.push({
                ...this.state.annotation,
                actionVerb: prevState.actionVerb
            });

            return {
                ...prevState,
                annotations,
                actionVerb: '',
                modalOpen: false
            }
        })
    };

    onRightClick = (rightClickLineNum, speaker, content) => (event) => {
        event.preventDefault();

        const {start, end} = this.state;
        let lineStart, lineEnd, lineSpeaker, lineContent;
        if (!start || !end) {
            // just right-click, no text selection
            lineStart = lineEnd = rightClickLineNum;
            lineSpeaker = speaker;
            lineContent = content;
        } else {
            if (start[2] !== end[2]) return;

            lineStart = start[0];
            lineEnd = end[0];
            lineSpeaker = start[1];
            lineContent = window.getSelection().toString();
            if (lineContent.length === 0) {
                lineContent = content;
            }
        }

        const annotation = {
            lineStart: lineStart,
            lineEnd: lineEnd,
            content: lineContent,
            speaker: lineSpeaker,
        };

        this.setState({
            start: undefined,
            end: undefined,
            annotation,
            modalOpen: true
        })
    };

    showState(event) {
        console.log(this.state.annotations);
        console.log(JSON.stringify(this.state.annotations))
    }

    closeModal = event => {
        this.setState({modalOpen: false})
    };

    render() {
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

                <Modal
                    isOpen={this.state.modalOpen}
                    style={customStyles}>
                    <p>You selected:</p>
                    {this.state.annotation && <p>{this.state.annotation.content}</p>}
                    <TextField id="standard-full-width" placeholder="Annotate" onChange={this.recordActionVerb.bind(this)}/>
                    <Grid container spacing={1}>
                        <Grid item xs={4}>
                            <Button disabled={this.state.actionVerb.trim().length === 0}
                                    onClick={this.saveActionVerb.bind(this)}>Submit</Button>
                        </Grid>
                        <Grid item xs={4}>
                            <Button onClick={this.closeModal.bind(this)}>Dismiss</Button>
                        </Grid>
                    </Grid>
                </Modal>
            </div>
        );
    }
}

Modal.setAppElement('#root');


export default Content;