import React, {Component} from 'react';
import {Typography} from '@material-ui/core';
import "../App.css"
import ReactDOM from 'react-dom'
import ContextMenu from "./ContextMenu.js"

class Content extends Component {

    render() {
        let el;
        if (this.props.content) {
            el = document.createElement('html');
            el.innerHTML = this.props.content;
            let speechList = el.getElementsByClassName("speech");
            for (let i = 0; i < speechList.length; i++) {
                let s = speechList[i].getElementsByClassName("line");
                for (let j = 0; j < s.length; j++) {
                    s[j].addEventListener("contextmenu", function () {
                        console.log("rightclick")
                    })
                }
            }
        }

        return (
            <div>
                <Typography variant='h4' align='center'>{this.props.filename}</Typography>
                <div>
                    <div className="scrollable" id="script_content"
                         dangerouslySetInnerHTML={{__html: this.props.content}}/>
                </div>
            </div>
        );
    }
}

export default Content;