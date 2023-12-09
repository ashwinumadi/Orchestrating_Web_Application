import React, { Component } from "react";
import Login from "./Login";
import SongDisplayPage from "./SongDisplayPage";
import Layout from "./Layout";
import GetQueries from "./GetQueries"
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedin: false,
      username: ''
    };

    this.handleLoggedin = this.handleLoggedin.bind(this);
    this.handleLoggedout = this.handleLoggedout.bind(this);
    this.handleUserName = this.handleUserName.bind(this);
  }

  handleLoggedin = () => {
    this.setState({ loggedin: true });
  };

  handleLoggedout = () => {
    this.setState({ loggedin: false });
  };

  handleUserName = (name) => {
    this.setState({ username: name });
  };

  render() {
    return (
      <Router>
        <Layout loggedin={this.state.loggedin}
          handleLoggedin={this.handleLoggedin}
          handleLoggedout={this.handleLoggedout}>
          <Switch>
            <Route exact path="/" render={(props) => <Login loggedin={this.state.loggedin} handleLoggedin={this.handleLoggedin} handleUserName={this.handleUserName} {...props} />} />
            <Route path="/songsdisplay/" render={(props) => <SongDisplayPage handleLoggedout={this.handleLoggedout} username={this.state.username} {...props} />} />
            <Route path="/getqueries/" render={(props) => <GetQueries username={this.state.username} {...props} />} />
          </Switch>
        </Layout>
      </Router>
    );
  }
}