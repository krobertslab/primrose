import React from 'react';
import JSONPretty from 'react-json-pretty';
const trials = '{"query": { "bool": {"must": [{"multi_match": {"query": "{{Disease}}","fields": ["brief_title","brief_summary","mesh_term","keyword","condition","eligibility"],"tie_breaker": 0.4,"type": "best_fields","boost": 1.5}},{"bool": {"should": [{"multi_match": {"query": "{{Gene}}","fields": ["brief_title","brief_summary","mesh_term","keyword","condition", "eligibility"],"tie_breaker": 0.4, "type": "cross_fields", "boost": 1 }}]}},{"match_all": {"boost": 0.001}},{"range": {"minimum_age": {"lte": "{{Age}}","boost": 2 }}},{"range": {"maximum_age": {"gte": "{{Age}}","boost": 2}}}, {"bool": {"should": [{"match": {"gender": "{{gender}}"}},{ "match": {"gender": "ALL"}}]}}]}}}'
const abs  = {
    "query": {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": "{{Disease}}",
                        "fields": [
                            "text",
                            "mesh_terms"
                        ],
                        "tie_breaker": 0.4,
                        "type": "best_fields",
                        "boost": 1.5
                    }
                },
                {
                    "bool": {
                        "should": [
                            {
                                "multi_match": {
                                    "query": "{{Gene}}",
                                    "fields": [
                                        "text",
                                        "mesh_terms"
                                    ],
                                    "tie_breaker": 0.4,
                                    "type": "cross_fields",
                                    "boost": 1
                                }
                            }
                        ]
                    }
                }
            ],
            "should": [
                {
                    "multi_match": {
                        "query": "{{gender}}",
                        "fields": [
                            "mesh_terms"
                        ],
                        "tie_breaker": 0.4,
                        "type": "best_fields",
                        "boost": 1
                    }
                }
            ]
        }
    }
}
export default class JViewer extends React.Component {
	constructor(props) {
        super(props);
        this.state ={
            data : ''

        }
        if(this.props.type ===1){
            this.state.data = trials
        }
        else{
            this.state.data = abs
        }
    }
    render(){
        return(
            <div>
                <JSONPretty space="10" data={this.state.data} ></JSONPretty>
            </div>
        )
    }

}