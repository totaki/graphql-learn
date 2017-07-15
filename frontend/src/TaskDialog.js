import React, { Component } from 'react';
import Dialog from 'material-ui/Dialog';
import TextField from 'material-ui/TextField'
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';

const ENDPOINT = 'http://localhost:9999/graphql';

const createTask = (title, description, callback) => {
    fetch(ENDPOINT, {
        'method': 'POST',
        'body': `mutation { createTask (input: {title: "${title}", description: "${description}", clientMutationId: "test"}) { ok } } `
    }).then((result) => result.json()).then((data) => callback(data));
};

const style = {
  margin: 12,
};

class TaskDialog extends Component {
  state = {
    open: false,
    title: '',
    description: ''
  };

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = (props) => {
    this.setState({open: false});
  };

  handleSave = () => {
    const { title, description } = this.state;
    if (title.length > 0 && description.length > 0) {
        createTask(title, description, console.log)
    }
  };

  render() {
    const { title, description } = this.state;
    const actions = [
      <FlatButton
        label="Cancel"
        default={true}
        onTouchTap={this.handleClose}
      />,
      <RaisedButton label="Save" primary={true} onTouchTap={this.handleSave} style={style} />,
    ];

    return (
      <div>
        <RaisedButton label="New task" secondary={true} onTouchTap={this.handleOpen} style={style} />
        <Dialog
          title="Create new task"
          actions={actions}
          modal={true}
          open={this.state.open}
          onRequestClose={this.handleClose}
        >
          <TextField
      hintText="Enter title"
      floatingLabelText="Title"
      type="text"
      fullWidth={true}
      value={title}
      onChange={(e, v) => this.setState({title: v})}
    /><br />
    <TextField
      floatingLabelText="Description"
      underlineShow={false}
      multiLine={true}
      fullWidth={true}
      type="text"
      rows={4}
      rowsMax={4}
      value={description}
      onChange={(e, v) => this.setState({description: v})}
    /><br />
        </Dialog>
      </div>
    );
  }
}

export default TaskDialog