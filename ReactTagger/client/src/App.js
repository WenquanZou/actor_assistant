import React, { Component } from 'react';
import './App.css';
import Window from './components/Window';
import { Typography, Container } from '@material-ui/core';

class App extends Component {

  state = {
    plays: undefined,
    error: undefined
  }

  componentDidMount() {
    fetch('http://127.0.0.1:5000/plays', {
      headers: {
        'Access-Control-Allow-Origin':'*'
      }
    })
      .then(result => result.json())
      .then(result => this.setState({ plays: result.plays }))
      .catch(error => {
        console.error(error)
        this.setState({ error: error.message })
      })
  }

  render() {
    return (
      <Container>
        <Typography component='h1' variant='h3' align='center' gutterBottom>Tagging Tool</Typography>
        {
          this.state.plays === undefined && <p>Loading plays...</p>
        }
        {
          this.state.error && <p>{this.state.error}</p>
        }
        {
          this.state.plays !== undefined && <Window plays={this.state.plays}></Window>
        }
      </Container>
    );
  }
}

export default App;
