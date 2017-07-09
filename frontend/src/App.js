import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import './App.css';
import TaskDialog from "./TaskDialog";
import injectTapEventPlugin from 'react-tap-event-plugin';

injectTapEventPlugin();

const ENDPOINT = 'http://localhost:9999/graphql';

const getTasks = (callback) => {
    fetch(ENDPOINT, {
        'method': 'POST',
        'body': 'query { tasks { edges { node { id title description } } } }'
    }).then((result) => result.json()).then((data) => callback(data));
};

class Task extends Component {

    render() {
        const { title, description } = this.props;
        return (
            <div>
                <span>{title}</span>
                <span>{description}</span>
            </div>
        )
    }
}


class TaskList extends Component {

    state = {
        edgesList: []
    };

    componentWillMount() {
        getTasks((data) => this.setState({edgesList: data.tasks.edges}))
    }

    render() {
        const { edgesList } = this.state;
        return (
            <div>
                {edgesList.map((e) => <Task key={e.node.id} {...e.node}/>)}
            </div>
        )
    }
}

class TaskApp extends Component {
    render() {
        return (
            <div>
                <TaskDialog/>
                <TaskList/>
            </div>
        )
    }
}

class App extends Component {
  render() {
    return (
        <MuiThemeProvider>
            <TaskApp/>
        </MuiThemeProvider>
    );
  }
}

export default App;
