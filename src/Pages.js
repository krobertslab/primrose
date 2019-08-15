import React from 'react';
import Abs from "./Components/Abs"
import Trials from "./Components/Trials"
import Home2 from "./Components/Home"
import JViewer from "./Components/jsonviewer"

export class JSONABS extends React.Component{
    render() {
		return (
			<div >
			   <JViewer type={0}></JViewer>
			</div>
		);
	}
}
export class JSONTRIALS extends React.Component{
    render() {
		return (
			<div >
			   <JViewer type={1}></JViewer>
			</div>
		);
	}
}
export class Abstracts extends React.Component{
    render() {
		return (
			<div className="container padded">
			   <Abs></Abs>
			</div>
		);
	}
}
export class ClinicalTrials extends React.Component{
    render() {
		return (
			<div className="container padded">
			   <Trials></Trials>
			</div>
		);
	}
}
export class Home extends React.Component{
    render() {
		return (
			<div className="container padded">
			   <Home2></Home2>
			</div>
		);
	}
}