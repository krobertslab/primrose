
import React from 'react';
import {Navbar,Nav} from 'react-bootstrap'



export default class Home2 extends React.Component {
	constructor(props) {
		super(props);
	
    this.state = {
          hello: 'hi'
     
		}
		
	}

	render() {
	
            return (
                <div>
                 
                    <Navbar bg="light" variant="light" expand="lg">
                        <Navbar.Brand href="#home">
                        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                        {' PRIMROSE'}
                        </Navbar.Brand>
                        <Navbar.Collapse id="basic-navbar-nav">
                            <Nav className="mr-auto">
                                    <Nav.Link href="/primrose/">Home</Nav.Link>
                                    
                            </Nav>

                        </Navbar.Collapse>
                    </Navbar>
                </div>
            )
      }
	
}