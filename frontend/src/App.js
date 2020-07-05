import React, { Component } from 'react';
import Distributor from './Distributor';
import Amplify from 'aws-amplify';
import { amplify_config } from './config';

Amplify.configure(amplify_config);

class App extends Component {
  render() {

    return (
      <div className="container">
          <div className="jumbotron" >
            <Distributor {... this.props}  />
          </div>
      </div>
    );
  }
}

export default App

