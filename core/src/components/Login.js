import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import axios from 'axios';


export default class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      showResults: true,
      showTextField: false,
    };
    this.handlePassword = this.handlePassword.bind(this);
    this.handleUsername = this.handleUsername.bind(this);
    this.handleLoginPressed = this.handleLoginPressed.bind(this);
    this.handleCreateUserPressed = this.handleCreateUserPressed.bind(this);
  }

  handleUsername(e) {
    this.setState({
      username: e.target.value,
    });
  }

  handlePassword(e) {
    this.setState({
      password: e.target.value,
    });
    
  }
  handleLoginPressed= async () => {
    const { handleLoggedin, handleUserName, history } = this.props;
    const response = await axios.post('http://34.16.65.113/api/login/', {
        username: this.state.username,
        password: this.state.password,
      });
      if (!response.status===200)  {
        throw new Error('Login Failed')
      } else {
        const token = response.data.access;
        localStorage.setItem('token', token);
        handleLoggedin();
        handleUserName(this.state.username);
        history.push(`/songsdisplay/`);
      }   
  }

  handleCreateUserPressed= async () => {
    /*const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: this.state.username,
        password: this.state.password,
      }),
    };*/
    const response = await axios.post("http://34.16.65.113/api/create-user/", {
        username: this.state.username,
        password: this.state.password,
      });

        if (!response.status===201)  {
            throw new Error('User creation failed')
        }
        else{
          this.setState({ showTextField: true });
          // Set a timer to hide the text field after 5 seconds
          setTimeout(() => {
            this.setState({ showTextField: false });
          }, 5000);
        }
  }

  componentWillUnmount() {
    // Clear the timer when the component is unmounted
    clearTimeout();
  }

  render() {
    return (
      <Grid container spacing={1} >
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            JurassicJams 
          </Typography>
          <Typography component="h6" variant="h4">
            Login to witness the Beast of suggestions. 
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              id="text-field-username"
              required={true}
              type="string"
              label="Username"
              onChange={this.handleUsername}
              variant="outlined"
              inputProps={{
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText>
              <div align="center">Enter Username</div>
            </FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center"> 
          <FormControl>
            <TextField
              id="text-field-password"
              required={true}
              type="password"
              label="Pasword"
              onChange={this.handlePassword}
              variant="outlined"
              inputProps={{
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText>
              <div align="center">Enter password</div>
            </FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={this.handleLoginPressed}
          >
            Login
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" 
           onClick={this.handleCreateUserPressed}>
            Signup
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          {this.state.showTextField && (
            <TextField
              label={`  Your account has been created : ${this.state.username}`}   
              variant="standard" 
              InputProps={{
                style: { color: 'lightgreen', width: '300px', textAlign: 'center'},
              }}
            />
          )}
        </Grid>
      </Grid>
    );
  }
}




















