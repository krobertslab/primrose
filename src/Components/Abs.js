import React from 'react';
import { APICALL,ABSCALL } from '../utils/APICall';
import {Row,Col,Form,Table,Button,Spinner,InputGroup,FormControl,Pagination} from 'react-bootstrap'
import { RadioGroup, RadioButton } from 'react-radio-buttons';
import {Typeahead} from 'react-bootstrap-typeahead'; 
import Viewer from "./Viewer"

const i = ["CDK4 Amplification", "KRAS (G13D","BRAF (V600E)","NF2 (K322)",
"AKT1(E17K)","FGFR1 Amplification","PTEN (Q171)","CDKN2A Deletion","NRAS (Q61K)","EGFR (L858R)",
"EML4-ALK Fusion transcript","KIT Exon 9 (A502_Y503dup)","KRAS (G12C)","PIK3CA (E545K)","BRCA2",
"IDH1 (R132H)","STK11","CDKN2A","PTEN Inactivating","CDK6 Amplification","MDM2 Amplification","ALK Fusion",
"ERBB2 Amplification","PTEN Loss","NTRK1","MET Amplification","NRAS Amplification","KRAS"," TP53","ERBB3",
"RB1","TP53"];
export default class Abs extends React.Component {
	constructor(props) {
		super(props);
	
    this.state = {
      id:'',
            doc: [],
            currentDoc:[],
            disease: "",
            gene: "",
            dem: "",
            loading:false,
            type : this.props.type,
            totalPages : 10,
            currentPage: 1,
            gender: null,
            age:50
		}
    this.onSubmit = this.onSubmit.bind(this);
    this.onChange = this.onChange.bind(this)
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handlePageChange = this.handlePageChange.bind(this)
	}
 
  onChange(e){
    this.setState({gender:e})
  }

	handleInputChange(event) {
		const target = event.target;
		const value = target.value;
		const name = target.name;
    this.setState({
      [name]: value
    });
  }

  // When the form is being submitted
	async onSubmit (event) {
        event.preventDefault();
        this.setState({loading:true})
        
        var end = "/abstracts/" + this.state.disease +"/" + this.state.gene + "/" + this.state.age + "-year-old " + this.state.gender 
        alert("Due to security reasons we are unable to connect to our REST service at this time. Please enjoy some sample data.")
        var data = ABSCALL()//JSON.parse(await APICALL(end))
        var currentD = data.slice(0, 100)

      
      
        this.setState({doc: data,loading:false,currentDoc:currentD,disease:"Breast Cancer",gene:"BRCA2",gender:"female"})
        
       

    }
  rowClicked(e){
    if(!e.includes("A")){
      window.location.href = "https://www.ncbi.nlm.nih.gov/pubmed/" + e
    }

  }
  handlePageChange(event) {
    
    this.setState({ currentPage:event.target.text });
    var c  = this.state.doc.slice((this.state.doc.length/this.state.totalPages) * (event.target.text-1), (this.state.doc.length/this.state.totalPages) * (event.target.text))
    this.setState({currentDoc:c})

    

  }
  


	render() {
            var items = []
            for (let number = 1; number <= this.state.totalPages; number++) {
              items.push(
                <Pagination.Item onClick={this.handlePageChange} name={number} onkey={number} id={number} active={false}>
                  {number}
                </Pagination.Item>,
                
              );
            }
            var arr = [this.state.disease,this.state.age.toString(),this.state.gender] 
            if (this.state.gene.length){
            
              arr  = arr.concat(this.state.gene)
            }
            console.log(arr)

            return (
                <div>
                    
                     <Form  noValidate name="form" style={{padding:'.5%'}} onSubmit={this.onSubmit} >
                     <h3 >Query Abstracts</h3>
                    <InputGroup className="mb-3">
                          <InputGroup.Prepend>
                              <InputGroup.Text>Disease</InputGroup.Text>
                          </InputGroup.Prepend>
                          <FormControl
                            placeholder="Disease"
                            aria-label="Disease"
                            aria-describedby="basic-addon1"
                            id="disease"
                            name="disease"
                            onChange={this.handleInputChange} 
                            value={this.state.disease}
                            required
                          />
                    </InputGroup>
                    <InputGroup className="mb-3">
                            <InputGroup.Prepend>
                            <InputGroup.Text>Genes</InputGroup.Text>
                        </InputGroup.Prepend>
                        <Typeahead
                            multiple
                            id='selectorQ'
                      
                            onChange={(selected) => {
                              this.setState({gene:selected})
                            }}
                            options={i} align="left" />
        
                    </InputGroup>
                   
                    <Form.Row>
                      <Col>
                      <InputGroup className="mb-3" >
                          <InputGroup.Prepend>
                              <InputGroup.Text>Age</InputGroup.Text>
                          </InputGroup.Prepend>
                          <FormControl
                            placeholder="Age"
                            aria-label="Age"
                            aria-describedby="basic-addon1"
                            id="age"
                            name="age"
                            onChange={this.handleInputChange} 
                            value={this.state.age}
                            type="number"
                            required
                          />
                    </InputGroup>
                      </Col>
                      <Col  md={{ span: 5, offset: 0 }}>
                      <RadioGroup onChange={ this.onChange } horizontal>
                        <RadioButton iconSize={20} padding={5} value="male">
                          Male
                        </RadioButton>
                        <RadioButton iconSize={20}  padding={5} value="female">
                          Female
                        </RadioButton>
                  
                 
                      </RadioGroup>
                      </Col>
                      </Form.Row>
                   
                    

                         
                   
                    {this.state.loading && <Spinner animation="border" role="status"><span className="sr-only">Loading...</span></Spinner>}
                    {!this.state.loading &&<Button type='submit'>Submit!</Button>}
                    </Form>
                    
                    {this.state.doc.length > 0 && <Row>
                      <Col >
                         <input placeholder=" Start Year"></input>
                         <span style={{padding:'2%'}}> - </span>
                         <input placeholder="End Year"></input>
                      </Col>
                      <Col >
                         <Pagination className="float-right"  >{items}</Pagination>
                      </Col>
              
                       
                    </Row>}
                   
                    <Table >

                          {this.state.currentDoc.map(e => (
                                  <tbody>
                                      <tr key={e["_id"]} onClick={(z) => this.rowClicked(e["_id"])}>
                                       <Viewer color={"light"} condition={"Journal Title"} title={e._source.text.split(".")[0]} brsum={e._source.text} arr={arr} ></Viewer>
                  
                                      </tr> 
                                  </tbody>
                              ))}
                              </Table> 
                </div>
            )
      }
	
}
