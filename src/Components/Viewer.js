
import React from 'react';
import Highlighter from 'react-highlight-words'
import {Button} from 'react-bootstrap'

export default class Viewer extends React.Component {
	constructor(props) {
		super(props);
	
    this.state = {
          title: this.props.title,
          brsum: this.props.brsum,
          arr: this.props.arr,
          condition: this.props.condition,
          color: this.props.color
     
        }
        console.log(this.props.arr)
		
	}

	render() {
	
            return (
                <div>               
                   <h5 style={{textAlign:'left'}}><Highlighter searchWords={this.state.arr} autoEscape={true} textToHighlight={this.state.title}/></h5>
                     <p style={{textAlign:'left'}}><Highlighter  searchWords={this.state.arr} autoEscape={true} textToHighlight={this.state.brsum.substring(0, 200)}/> </p>
                    <span style={{display:'flex',flexDirection:'row'}}>
                       
                        <Button style={{marginLeft:'auto'}} disabled variant={this.state.color}>{this.state.condition}</Button>
            </span>
                </div>
            )
      }
	
}