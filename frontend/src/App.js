import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import socketIOClient from "socket.io-client";
import { BrowserRouter, Route, Redirect,withRouter } from "react-router-dom";
import {Tree} from 'react-d3-tree';
//import createHistory from 'history/createBrowserHistory';
import StatusList from "./components/statusList";

//const history = createHistory()
const svgSquare = {
    shape: 'rect',
    shapeProps: {
        width: 20,
        height: 20,
        x: -15,
        y: -15,
    }
}
const scaleExtent={
min: 0.1, max: 1
}

const trans = {
    x: 900,
    y: 150
}
const separation={siblings: 5, nonSiblings: 5}

const textLayout={textAnchor: "start", x: -80, y: 15, transform: undefined }

class App extends Component {
    constructor () {
        super();
        this.state = {
            file: null,
            title:"please upload your file",
            items: [],
            show:"home",
            Cname:null,
            BODDependency:"1",
            ESTATEDependency:"1",
            PRODUCTependency:"0",
            PARTNERDependency:"1",
            LAWDependency:"0",
            NORPDependency:"0",
            EXPORTDependency:"1",
            BANKDependency:"1",
            BODindex:"1",
            ESTATEindex:"1",
            PRODUCTindex:"3",
            PARTNERindex:"1",
            LAWindex:"2",
            NORPindex:"2",
            EXPORTindex:"1",
            BANKindex:"1",
            directory:"E:/L4/FYP/FYP_repo/FYP/NLP/test/all",
            data:[{
                name: 'waiting for company',
                attributes: {
                    industry: 'val A',
                    since: 'val B',
                    until: 'val C'
                }
            }]
        };
        this.addItem = this.addItem.bind(this);
        this.updateInputOne = this.updateInputOne.bind(this);
        this.updateInputTwo = this.updateInputTwo.bind(this);
        this.updateBODDependency = this.updateBODDependency.bind(this);
        this.updateESTATEDependency = this.updateESTATEDependency.bind(this);
        this.updatePRODUCTependency = this.updatePRODUCTependency.bind(this);
        this.updatePARTNERDependency = this.updatePARTNERDependency.bind(this);
        this.updateLAWDependency = this.updateLAWDependency.bind(this);
        this.updateNORPDependency = this.updateNORPDependency.bind(this);
        this.updateEXPORTDependency = this.updateEXPORTDependency.bind(this);
        this.updateBANKDependency = this.updateBANKDependency.bind(this);
        this.updateBODindex = this.updateBODindex.bind(this);
        this.updateESTATEindex = this.updateESTATEindex.bind(this);
        this.updatePRODUCTindex = this.updatePRODUCTindex.bind(this);
        this.updatePARTNERindex = this.updatePARTNERindex.bind(this);
        this.updateLAWindex = this.updateLAWindex.bind(this);
        this.updateNORPindex = this.updateNORPindex.bind(this);
        this.updateEXPORTindex = this.updateEXPORTindex.bind(this);
        this.updateBANKindex = this.updateBANKindex.bind(this);
    }
    addItem = (_inputElement) => {
        if (_inputElement !== "") {
            var newItem = {
                name: _inputElement,
                key: Date.now()
            };
            console.log( _inputElement)
            this.setState((prevState) => {
                return {
                    items: prevState.items.concat(newItem)
                };
            });

        }

    }
    updateInputOne(event){
        this.setState({Cname : event.target.value})
        console.log(this.state.Cname)
    }
    updateInputTwo(event){
        this.setState({directory : event.target.value})
        console.log(this.state.directory)
    }
    updateBODDependency(event){
        this.setState({BODDependency : event.target.value})
        console.log(this.state.BODDependency)
    }
    updateESTATEDependency(event){
        this.setState({ESTATEDependency : event.target.value})
        console.log(this.state.ESTATEDependency)
    }
    updatePRODUCTependency(event){
        this.setState({PRODUCTependency : event.target.value})
        console.log(this.state.PRODUCTependency)
    }
    updatePARTNERDependency(event){
        this.setState({PARTNERDependency : event.target.value})
        console.log(this.state.PARTNERDependency)
    }
    updateLAWDependency(event){
        this.setState({LAWDependency : event.target.value})
        console.log(this.state.LAWDependency)
    }
    updateNORPDependency(event){
        this.setState({NORPDependency : event.target.value})
        console.log(this.state.NORPDependency)
    }
    updateEXPORTDependency(event){
        this.setState({EXPORTDependency : event.target.value})
        console.log(this.state.EXPORTDependency)
    }
    updateBANKDependency(event){
        this.setState({BANKDependency : event.target.value})
        console.log(this.state.BANKDependency)
    }
    updateBODindex(event){
        this.setState({BODindex : event.target.value})
        console.log(this.state.BODindex)
    }
    updateESTATEindex(event){
        this.setState({ESTATEindex : event.target.value})
        console.log(this.state.ESTATEindex)
    }
    updatePRODUCTindex(event){
        this.setState({PRODUCTindex : event.target.value})
        console.log(this.state.PRODUCTindex)
    }
    updatePARTNERindex(event){
        this.setState({PARTNERindex : event.target.value})
        console.log(this.state.PARTNERindex)
    }
    updateLAWindex(event){
        this.setState({LAWindex : event.target.value})
        console.log(this.state.LAWindex)
    }
    updateNORPindex(event){
        this.setState({NORPindex : event.target.value})
        console.log(this.state.NORPindex)
    }
    updateEXPORTindex(event){
        this.setState({EXPORTindex : event.target.value})
        console.log(this.state.EXPORTindex)
    }
    updateBANKindex(event){
        this.setState({BANKindex : event.target.value})
        console.log(this.state.BANKindex)
    }


    submitFile = (event) => {
        event.preventDefault();
        const formData = new FormData();
        const socket = socketIOClient("http://127.0.0.1:5000");
        socket.on("message", data => this.changeTitle(data));

        formData.append('file', this.state.file[0]);
        axios.post(`http://localhost:3001/test-upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(response => {
            this.changeTitle("done uploading")
            this.setState({show:"loaded"})
            console.log(response.data.Location)
            const dir=this.state.directory
            const comp=this.state.Cname
            const BANKDependency=this.state.BANKDependency
            const BANKindex=this.state.BANKindex
            const BODDependency=this.state.BODDependency
            const BODindex=this.state.BODindex
            const ESTATEDependency=this.state.ESTATEDependency
            const ESTATEindex=this.state.ESTATEindex
            const EXPORTDependency=this.state.EXPORTDependency
            const EXPORTindex=this.state.EXPORTindex
            const LAWDependency=this.state.LAWDependency
            const LAWindex=this.state.LAWindex
            const NORPDependency=this.state.NORPDependency
            const NORPindex=this.state.NORPindex
            const PARTNERDependency=this.state.PARTNERDependency
            const PARTNERindex=this.state.PARTNERindex
            const PRODUCTependency=this.state.PRODUCTependency
            const PRODUCTindex=this.state.PRODUCTindex

            const url="http://127.0.0.1:5000/run?dir="+dir+"&copm="+comp+"&pdf="+response.data.Location+"&BANKDependency="+BANKDependency+"&BANKindex="+BANKindex+"&BODDependency="+BODDependency+"&BODindex="+BODindex+"&ESTATEDependency="+ESTATEDependency+"&ESTATEindex="+ESTATEindex+"&EXPORTDependency="+EXPORTDependency+"&EXPORTindex="+EXPORTindex+"&LAWDependency="+LAWDependency+"&LAWindex="+LAWindex+"&NORPDependency="+NORPDependency+"&NORPindex="+NORPindex+"&PARTNERDependency="+PARTNERDependency+"&PARTNERindex="+PARTNERindex+"&PRODUCTependency="+PRODUCTependency+"&PRODUCTindex="+PRODUCTindex
            axios.post(url , {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Access-Control-Allow-Origin': '*'
                }
            }).then(response => {
                const jj ='https://s3.eu-west-2.amazonaws.com/finalyearprojectresources/front_end_data.json';
                console.log("hey");
                fetch(jj)
                    .then(response => response.json())
                    .then(responce =>{
                        const data=this.state.data;
                        data.push(responce[0])
                        console.log(data)
                        console.log(data[1])
                        this.setState({data:data[1]})
                        this.setState({show:"graph"})
                        this.changeTitle("Annual Report Summery of the company")

                        //this.props.history.push("/graph")

                    })
                    .catch((err) => console.error(err));
            }).catch(error => {
                // handle your error
            });
        }).catch(error => {
            // handle your error
        });
    }

    handleFileUpload = (event) => {
        this.setState({file: event.target.files});
        this.setState({show:"paras"})
    }

    changeTitle = (message) => {
        this.setState({ title:message });
        this.addItem(message)
    };


  render() {
        var partial;
        if(this.state.show ==="home"){
            partial=<div>
                <img src={logo} className="App-logo" alt="logo" />
                <StatusList status={this.state.items}/>
                <p>
                    {this.state.title}

                </p>
                <label style={{fontSize:18}}>please enter company ref name  :  </label><input style={{width:300}}  type="text" onChange={this.updateInputOne} placeholder={"Enter company name"}></input>
                <br/>
                <label style={{fontSize:18}}>please enter file save directory  :             </label>
                <input  style={{width:300}}  type="text"  onChange={this.updateInputTwo} placeholder={"E:/L4/FYP/FYP_repo/FYP/NLP/test/all"}></input>
                <br/>
                <br/>
                <form onSubmit={this.submitFile}>
                    <input label='upload file' type='file' onChange={this.handleFileUpload} />
                    <button type='submit'>Send</button>
                </form>
            </div>
        }
        else if(this.state.show ==="paras"){
            partial=<div>
                <img src={logo} className="App-logo" alt="logo" />
                <StatusList status={this.state.items}/>
                <p>
                    {this.state.title}

                </p>
                <label style={{fontSize:18}}>please enter company ref name  :  </label><input style={{width:300}}  type="text" onChange={this.updateInputOne} placeholder={"Enter company name"}></input>
                <br/>
                <label style={{fontSize:18}}>please enter file save directory  :             </label>
                <input  style={{width:300}}  type="text"  onChange={this.updateInputTwo} placeholder={"E:/L4/FYP/FYP_repo/FYP/NLP/test/all"}></input>
                <br/>
                <br/>
                <form onSubmit={this.submitFile}>
                    <input label='upload file' type='file' onChange={this.handleFileUpload} />
                    <button type='submit'>Send</button>
                </form>
                <br/>
                <label style={{fontSize:12, marginLeft:130}}>Board of Directors  </label>
                <label style={{fontSize:12, marginLeft:30}}>Estates  </label>
                <label style={{fontSize:12, marginLeft:45}}>Products  </label>
                <label style={{fontSize:12, marginLeft:50}}>Partners  </label>
                <label style={{fontSize:12, marginLeft:50}}>Laws  </label>
                <label style={{fontSize:12, marginLeft:40}}>governing bodies  </label>
                <label style={{fontSize:12, marginLeft:10}}>export entities  </label>
                <label style={{fontSize:12, marginLeft:10}}>relevant banks </label>
                <br/>
                <div>
                <label style={{fontSize:15}}>Dependency Parser  :  </label>
                <input style={{width:50, margin:20}}  type="number"  onChange={this.updateBODDependency} placeholder={"1"} ></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateESTATEDependency}placeholder={"1"} ></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updatePRODUCTependency}placeholder={"0"} ></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updatePARTNERDependency}placeholder={"1"} ></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateLAWDependency}placeholder={"0"} ></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateNORPDependency} placeholder={"0"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateEXPORTDependency} placeholder={"1"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateBANKDependency}placeholder={"1"} ></input>
                </div>
                <div>
                <label style={{fontSize:15,marginLeft:23}}>Clustering Index     :  </label>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateBODindex} placeholder={"1"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateESTATEindex} placeholder={"1"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updatePRODUCTindex} placeholder={"3"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updatePARTNERindex} placeholder={"1"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateLAWindex} placeholder={"2"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateNORPindex} placeholder={"2"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateEXPORTindex} placeholder={"1"}></input>
                <input style={{width:50, margin:20}}  type="number" onChange={this.updateBANKindex} placeholder={"1"}></input>
                </div>
                <div>
                    <label style={{fontSize:15}}>Parsing Depth  :  </label>
                    <label style={{fontSize:12, marginLeft:45}}>0  </label>
                    <label style={{fontSize:12, marginLeft:84}}>2  </label>
                    <label style={{fontSize:12, marginLeft:84}}>0  </label>
                    <label style={{fontSize:12, marginLeft:84}}>2  </label>
                    <label style={{fontSize:12, marginLeft:84}}>0  </label>
                    <label style={{fontSize:12, marginLeft:84}}>0  </label>
                    <label style={{fontSize:12, marginLeft:84}}>4  </label>
                    <label style={{fontSize:12, marginLeft:84}}>0 </label>
                </div>
                <div>
                    <label style={{fontSize:15}}>Similarity Index  :  </label>
                    <label style={{fontSize:12, marginLeft:40}}>0.6  </label>
                    <label style={{fontSize:12, marginLeft:78}}>0.6  </label>
                    <label style={{fontSize:12, marginLeft:78}}>0.8</label>
                    <label style={{fontSize:12, marginLeft:78}}>0.9</label>
                    <label style={{fontSize:12, marginLeft:78}}>0.4</label>
                    <label style={{fontSize:12, marginLeft:78}}>0.6</label>
                    <label style={{fontSize:12, marginLeft:78}}>0.6</label>
                    <label style={{fontSize:12, marginLeft:78}}>0.8</label>
                </div>
            </div>

        }
      else if(this.state.show ==="loaded"){
          partial=<div>
              <img src={logo} className="App-logo" alt="logo" />
              <StatusList status={this.state.items}/>
              <p>
                  {this.state.title}
              </p>
          </div>
      }
        else{
            partial=
                <div style={{backgroundColor:'#f6f7ff'}}>
                    <p style={{color:'#030302'}}>
                        {this.state.title}
                    </p>
                <div id="treeWrapper" style={{width: '70em', height: '30em'}} className="treeWrapper" >
                <Tree data={this.state.data} nodeSvgShape={svgSquare} translate={trans} zoom={0.6} scaleExtent={scaleExtent} separation={separation} transitionDurartion={1000} orientation={""} textLayout={textLayout} />
                </div>
                </div>
        }
    return (
        <BrowserRouter>
            <div className="App">
            <div className="main-content">
                <Route  path="/" exact={true} render={() => (
                    <Redirect to="/start"/>
                )}/>
                <Route  path="/start"exact={true} render={()=>{
                    return(
                <header className="App-header">

                    {partial}

                </header>
                    )
                }
                }/>
                <Route  path="/graph" exact={true} render={()=>{
                    return(
                        <div id="treeWrapper" style={{width: '50em', height: '50em'}} className="treeWrapper" >
                            <Tree data={this.state.data} nodeSvgShape={svgSquare} translate={trans}   />
                        </div>
                    )
                }
                }/>
            </div>
            </div>
        </BrowserRouter>


    );
  }
}

export default withRouter (App);
