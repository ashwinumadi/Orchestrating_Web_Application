/*import React from 'react';
import './index.css';
import App from './App';
import { render } from "react-dom";
import "./index.css";

const root = document.getElementById("root");
render(<App />, root);
*/
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);