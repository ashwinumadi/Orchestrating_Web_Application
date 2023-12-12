// Layout.js
import React, { Component } from 'react';
import { AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import { Link, withRouter } from 'react-router-dom';
import axios from 'axios';


class Layout extends Component {
    constructor(props) {
        super(props);
        this.state = {
          loggedin: false
        };
    
        this.handleButtonClick = this.handleButtonClick.bind(this);
        this.handleGetSongsClick = this.handleGetSongsClick.bind(this);
      };

      handleButtonClick() {
        const { loggedin, handleLoggedin, handleLoggedout, history } = this.props;
        const instance = axios.create({
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
            }
          });
          
          // Now use 'instance' for your requests instead of 'axios'
          instance.post(`http://34.171.144.89/api/logout/`).then(response => {
              // Handle the response

            if (!response.state===200) {
                
                throw new Error('This is a custom error message')
            }
            else {
                localStorage.removeItem('token');
                if (loggedin) {
                    handleLoggedout();
                  } else {
                    handleLoggedin();
                  }
                history.push(`/`);
            }
            })
            .catch(error => {
                console.error('Layout fetch failed:', error.message);
            });
      };
      handleGetSongsClick() {
        const { loggedin, handleLoggedin, handleLoggedout, history } = this.props;
        console.log('Inside')
        console.log(loggedin, handleLoggedin, handleLoggedout, history)
        if (loggedin) {
            console.log('Inside loggedin')
            history.push(`/songsdisplay/`);
        }
        
      };
  render() {
    const { loggedin } = this.props;
    return (
        <div>
            <>
                <AppBar position="sticky">
                <Toolbar>
                    <Typography variant="h6" component="div" style={{ flexGrow: 1 }}>
                    <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                        Jurassic Jams
                    </Link>
                    </Typography>
                    {loggedin && (
                        <Button color="inherit" onClick={this.handleGetSongsClick}>Get Songs</Button>)
                    }
                    {loggedin && (
                        <Button color="inherit" onClick={this.handleButtonClick}>Logout</Button>)
                    }
                </Toolbar>
                </AppBar>
                <Container style={{ marginTop: '80px' }}>
                    {this.props.children}
                </Container>
            </>
      </div>
    );
  }
}

export default withRouter(Layout);
