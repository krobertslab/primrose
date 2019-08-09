import React from 'react';
import { APICALL,TrialsCALL } from '../utils/APICall';
import {Pagination,Table,Button,Spinner,InputGroup,FormControl,Form, Row, Col} from 'react-bootstrap'
import { RadioGroup, RadioButton } from 'react-radio-buttons';
import {Typeahead} from 'react-bootstrap-typeahead'; // ES2015
import 'react-bootstrap-typeahead/css/Typeahead.css';
import Toggle from 'react-toggle'

import Viewer from "./Viewer"

const items = ["CDK4 Amplification", "KRAS (G13D","BRAF (V600E)","NF2 (K322)",
"AKT1(E17K)","FGFR1 Amplification","PTEN (Q171)","CDKN2A Deletion","NRAS (Q61K)","EGFR (L858R)",
"EML4-ALK Fusion transcript","KIT Exon 9 (A502_Y503dup)","KRAS (G12C)","PIK3CA (E545K)","BRCA2",
"IDH1 (R132H)","STK11","CDKN2A","PTEN Inactivating","CDK6 Amplification","MDM2 Amplification","ALK Fusion",
"ERBB2 Amplification","PTEN Loss","NTRK1","MET Amplification","NRAS Amplification","KRAS"," TP53","ERBB3",
"RB1","TP53"];

const obj = {"Availiable":"success","Temporarily not availiable":"danger","No longer availiable":"danger","Recruiting":"success", "Not yet recruiting": "success","Available for expanded access":"success","Active, not recruiting": "danger","Completed":"danger","Terminated":"danger","Suspended":"danger","Withdrawn":"danger","Enrolling by invitation":"danger","Temporarily not available for expanded access":"danger","No longer available for expanded access":"danger","Approved for marketing":"danger","Unknown":"warning","Unknown status":"warning"}
export default class Trials extends React.Component {
	constructor(props) {
		super(props);
    this.state = {
      id:'',
            doc: [],
            currentDoc:[],
            disease: "",
            gene: [],
            dem: "",
            loading:false,
            type : this.props.type,
            age : null, 
            gender: null ,
            totalPages : 10,
            currentPage: 1,
            a : false,
            temp: []
    }
    this.onChange = this.onChange.bind(this);
    this.viewOpen = this.viewOpen.bind(this);
		this.onSubmit = this.onSubmit.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handlePageChange  = this.handlePageChange.bind(this)
  }
  viewOpen(){
    this.setState({a:!this.state.a})
    console.log(this.state.a)
    if (this.state.a){
      this.setState({currentDoc:this.state.doc.slice(0, 100)})
    }else{
      var cDoc = this.state.doc.filter(e =>  obj[e._source["overall_status"]] !== "danger");
      var w = cDoc.slice(0, 100)
      this.setState({temp:cDoc,currentDoc:w})
     
    }
    


  }
  handlePageChange(event) {
    this.setState({ currentPage:event.target.text });
    var z; 
    if(!this.state.a){
    
      z = this.state.doc.slice((this.state.doc.length/this.state.totalPages) * (event.target.text-1), (this.state.doc.length/this.state.totalPages) * (event.target.text))
      
    }else{
      z = this.state.temp.slice((this.state.temp.length/this.state.totalPages) * (event.target.text-1), (this.state.temp.length/this.state.totalPages) * (event.target.text))
    }
    this.setState({currentDoc:z})


    

  }
	handleInputChange(event) {
		const target = event.target;
		const value = target.value;
		const name = target.name;
    this.setState({
      [name]: value
    });
  }
  rowClicked(e){
      window.location.href = "https://clinicaltrials.gov/ct2/show/" + e
  }
  onChange(e){
    
    this.setState({gender:e})
  }
  // When the form is being submitted
	async onSubmit (event) {
        event.preventDefault();
        this.setState({loading:true})
        var end = "/trials/" + this.state.disease +"/" + this.state.gene + "/" + this.state.age + "-year-old " + this.state.gender 
        alert("Due to security reasons we are unable to connect to our REST service at this time. Please enjoy some sample data.")
        var data = TrialsCALL()//JSON.parse(await APICALL(end))
        
        var currentD = data.slice(0, 100)
      
        console.log(data)
        this.setState({doc: data,loading:false,currentDoc:currentD})
 
    }
	render() {
            var i = []
            for (let number = 1; number <= this.state.totalPages; number++) {
              i.push(
                <Pagination.Item onClick={this.handlePageChange} name={number} onkey={number} id={number} active={false}>
                  {number}
                </Pagination.Item>,
                
              );
            }

            var arr = [this.state.disease,this.state.age,this.state.gender] 
            if (this.state.gene.length){
            
              arr  = arr.concat(this.state.gene)
            }
            console.log(arr)
            return (

                <div>
                    <h3 style={{margin:'.5%'}}>Query Clinical Trials</h3>
                    <form name="form" onSubmit={this.onSubmit}>
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
                      
                            onChange={(selected) => {
                              this.setState({gene:selected})
                            }}
                            options={items} align="left" />
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
                    </form>
                

                    
                 
                    {this.state.doc.length > 0 &&<Row style={{padding:'2%'}}>
                      <Col xs={5}>
                      <label> 
                        <span style={{padding:'2%'}}>Filter by year range</span>
                         <div>
                            <input placeholder=" Start Year"></input>
                            <span style={{}}> - </span>
                            <input placeholder="End Year"></input>
                         </div>
                        </label>
                      </Col>
                      <Col>
        
                      <label> 
                      <span style={{padding:'2%'}}>Toggle Open Trials</span>
                      <Toggle
                        defaultChecked={this.state.a}
                        onChange={this.viewOpen}  />
                     
                    </label>
                     
                      </Col>

                      <Pagination style={{marginLeft: 'auto'}} className="float-right"  >{i}</Pagination>
                    </Row>}
                    
                       <Table>
                 
                    {this.state.currentDoc.map(e => (
                            <tbody>
                                 <tr key={e["_id"]} onClick={(z) => this.rowClicked(e["_id"])}>
                                   <td>
                                    <Viewer color={obj[e._source["overall_status"]]} condition={e._source["overall_status"]} title={e._source["brief_title"]} brsum={e._source["brief_summary"]} arr={arr} ></Viewer>
               
                                   </td>
                                  
                                   
                          
                                 </tr> 
                            </tbody>
                        ))}
                        </Table> 
                </div>
                );
      }
}