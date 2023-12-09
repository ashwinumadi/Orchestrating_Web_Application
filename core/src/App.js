/*import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./components/HomePage";

export default class App extends Component {

  render() {
    return (
      <div>
        <HomePage />
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);

import React, { Component } from "react";
import Login from "./components/Login";
import SongDisplayPage from "./components/SongDisplayPage";
import Layout from "./components/Layout";
import GetQueries from "./components/GetQueries"
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
}*/


import React, { Component } from "react";
import HomePage from "./components/HomePage";

export default class App extends Component {

  render() {
    return (
      <div>
        <HomePage />
      </div>
    );
  }
}