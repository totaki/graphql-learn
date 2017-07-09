import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import './App.css';
import TaskDialog from "./TaskDialog";
import injectTapEventPlugin from 'react-tap-event-plugin';

injectTapEventPlugin();

const ENDPOINT = 'http://localhost:9999/graphql';

const getTasks = () => {
    fetch(ENDPOINT, {
        'method': 'POST',
        'body': 'query { tasks { edges { node { id title description } } } }'
    }).then((result) => result.json()).then((data) => console.log(data));
};

getTasks();

class App extends Component {
  render() {
    return (
        <MuiThemeProvider>
            <TaskDialog/>
        </MuiThemeProvider>
    );
  }
}

export default App;
