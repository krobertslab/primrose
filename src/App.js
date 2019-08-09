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
        <Route path="/PMSE/" exact component={Pages.Home}></Route>
        <Route path="/PMSE/abstracts" exact component={Pages.Abstracts}></Route>
        <Route path="/PMSE/trials" exact component={Pages.ClinicalTrials}></Route>
        <Footer></Footer>
       </Router>
    </div>
  );
}

export default App;
