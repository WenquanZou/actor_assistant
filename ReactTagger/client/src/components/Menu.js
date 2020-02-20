import React, { Component } from 'react';
import { List, ListItem, ListItemText, Divider } from '@material-ui/core';

class Menu extends Component {
  render() {
    return (
      <List>
        {this.props.plays.map((play, key) => (
          <>
          <ListItem key={key} button onClick={this.props.loadPlay(key)}>
            <ListItemText primary={play} />
          </ListItem>
          <Divider />
          </>
        ))}
      </List>
    );
  }
}

export default Menu;