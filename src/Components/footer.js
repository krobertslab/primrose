import React from 'react';
var style = {
    backgroundColor: "#F8F8F8",
    borderTop: "1px solid #E7E7E7",
    textAlign: "center",
    padding: "20px",
    position: "fixed",
    left: "0",
    bottom: "0",
    height: "80px",
    width: "100%",
}

var phantom = {
  display: 'block',
  padding: '20px',
  height: '60px',
  width: '100%',
}
export default class Footer extends React.Component {
	constructor(props) {
		super(props);
	
    this.state = {
          hello: 'hi'
     
		}
		
	}

	render() {
	
            return (
                <div>
                    <div style={phantom} />
                <div style={style}>
                <p>Acknowledgements: UTHealth Innovation for Cancer Prevention Research Summer Undergraduate Fellowship [Cancer Prevention and Research Insitute of Texas (CPRIT) grant # RP160015]</p>
                </div>
                </div>
                
               
            )
      }
	
}