import React from 'react';
import LoginForm from '../components/loginform'
import Router from 'next/router'
import { create } from 'apisauce'

import { AuthToken } from "../lib/auth_token";

class Logout extends React.Component {
    render() {
        return (
        <>
        </>
        )
    }
    componentDidMount = async () => {
        //AuthToken.clearToken();
        AuthToken.clearToken();
        
        Router.push('/');
    }
};
  

export default Logout;