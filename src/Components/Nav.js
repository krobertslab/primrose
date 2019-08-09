
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
                        {' Precision Medicine Search Engine'}
                        </Navbar.Brand>
                        <Navbar.Collapse id="basic-navbar-nav">
                            <Nav className="mr-auto">
                                    <Nav.Link href="/primrose/">Home</Nav.Link>
                                    <Nav.Link href="/primrose/abstracts">Abstracts</Nav.Link>
                                    <Nav.Link href="/primrose/trials">Clinical Trials</Nav.Link>
                            </Nav>

                        </Navbar.Collapse>
                    </Navbar>
                </div>
            )
      }
	
}