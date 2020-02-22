import React, {Component} from 'react';
import {List, ListItem, ListItemText, Divider} from '@material-ui/core';

class Menu extends Component {
    render() {
        return (
            <List className="scrollable">
                {this.props.plays.map((play) => (
                    <>
                        <ListItem key={play} button onClick={this.props.loadPlay(play)}>
                            <ListItemText primary={play}/>
                        </ListItem>
                        <Divider/>
                    </>
                ))}
            </List>
        );
    }
}

export default Menu;