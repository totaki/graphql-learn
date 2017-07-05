import React, { Component } from 'react';
import Dialog from 'material-ui/Dialog';
import TextField from 'material-ui/TextField'
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';

const style = {
  margin: 12,
};

class TaskDialog extends Component {
  state = {
    open: false,
  };

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  render() {
    const actions = [
      <FlatButton
        label="Cancel"
        default={true}
        onTouchTap={this.handleClose}
      />,
      <RaisedButton label="Save" primary={true} onTouchTap={this.handleClose} style={style} />,
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
    /><br />
    <TextField
      floatingLabelText="Description"
      underlineShow={false}
      multiLine={true}
      fullWidth={true}
      type="text"
      rows={4}
      rowsMax={4}
    /><br />
        </Dialog>
      </div>
    );
  }
}

export default TaskDialog