import React from 'react';
import Abs from "./Abs"
import Trials from "./Trials"
//import ReactLoading from 'react-loading';
import Toggle from 'react-toggle'

import "react-toggle/style.css" 

export default class Home2 extends React.Component {
	constructor(props) {
		super(props);
	
    this.state = {
          a: true
     
		}
		
	}


	

	render() {
	
            return (
                <div>
                  <label style={{paddingTop:'2%'}}>
                   
                    <Toggle
                        defaultChecked={this.state.a}
                        onChange={()=>{this.setState({a: !this.state.a})}} />
                   
                  </label>
                  {this.state.a && <Abs></Abs>}
                  {!this.state.a && <Trials></Trials>}
                 
                    
                </div>
            )
      }
	
}
