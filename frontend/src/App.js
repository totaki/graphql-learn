import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import './App.css';
import TaskDialog from "./TaskDialog";
import injectTapEventPlugin from 'react-tap-event-plugin';

injectTapEventPlugin();


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
