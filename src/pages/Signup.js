import React from 'react';
import axios from 'axios'
import { Link } from 'react-router-dom';

export default class Signup extends React.Component {
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
  
    doSignup = (e) => {
      const url = "/signup";
      const data = {
        username: this.state.user,
        password: this.state.pass
      };
      axios.post(url, data)
        .then((res) => {
          this.setState({
            data: [],
            resp: "Signup successful!"
          });
        })
        .catch((err) => {
          this.setState({
            data: [],
            resp: "Error in signup!"
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
            <button onClick={this.doSignup}>Signup</button><br /><br />
            <Link to="/login">Back to Login</Link><br /><br />

            </div>
  
  
          
            <div>
              {this.state.resp?this.state.resp:null}
            </div>
  
            
          </div>
      );
    }
  }