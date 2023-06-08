import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';


export default class Applogin extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      resp: null,
      user: null,
      pass: null
    };
  }

  doEditUser = (e) => {
    this.setState({
      user: e.target.value,
    });
  }

  doEditPass = (e) => {
    this.setState({
      pass: e.target.value,
    });
  }


  doLogin = (e) => {
    const url = "/login"
    const data = {
      user: this.state.user,
      pass: this.state.pass
    }
    axios.post(url, data)
    .then((res) => {
      this.setState({
        data: [],
        resp: "Welcome!"
      });
    })
      .catch((err) => {
        this.setState({
          data: [],
          resp: "Error!"
        });
      });
  }
  


  render() {
    // const { data } = this.state;
    return (
        <div>
          <div>
          Username: <input type="text" onChange={this.doEditUser}></input><br/>
          Password: <input type="text" onChange={this.doEditPass}></input><br/>
          <button onClick={this.doLogin}>Login</button><br/><br/>
          <Link to="/signup">Signup</Link><br /><br />
          </div>


        
          <div>
            {this.state.resp?this.state.resp:null}
          </div>

          
        </div>
    );
  }
}