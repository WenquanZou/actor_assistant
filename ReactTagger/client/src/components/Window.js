import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Menu from './Menu';
import Content from './Content';
import { Typography } from '@material-ui/core';

export default class Window extends Component {

  state = {
    content: undefined
  }

  /**
   * Param:
   * playId
   * 
   * Returns: 
   * A function to bind to the link which gets 
   * the HTML of that play and sends it to the content.
   */
  loadPlay = playId => event => {
    event.preventDefault()
    fetch(`http://127.0.0.1:5000/play/${playId}`, {
      headers: {
        'Access-Control-Allow-Origin':'*'
      }
    })
      .then(result => result.json())
      .then(({ html }) => {
        console.log(html)
        this.setState({ content: html })
      })
      .catch(console.error)
  }

  render() {
    return (
      <Grid container spacing={8}>
        <Grid item xs={4}>
          <Menu plays={this.props.plays} loadPlay={this.loadPlay.bind(this)} />
        </Grid>
        <Grid item xs={8}>
          <Content content={this.state.content} />
        </Grid>
      </Grid>
    );
  }
}
