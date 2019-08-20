import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom'
import './App.css';
import * as Pages from './Pages.js';
import Nav from "./Components/Nav"
import Footer from "./Components/footer"

function App() {
  return (
    <div className="App">
      <Router>
        <Nav></Nav>
        <Route path="/primrose/" exact component={Pages.Home}></Route>
        <Route path="/primrose/jsonabstracts/" exact component={Pages.JSONABS}></Route>
        <Route path="/primrose/jsontrials/" exact component={Pages.JSONTRIALS}></Route>
       
        <Footer></Footer>
       </Router>
    </div>
  );
}

export default App;
