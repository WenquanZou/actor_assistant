import React, { Component } from 'react';
import { Typography } from '@material-ui/core';

class Content extends Component {
  render() {
    return (
      <div>
        <Typography variant='h4' align='center'>Content</Typography>
        <div>
          {this.props.content}
        </div>
      </div>
    );
  }
}

export default Content;