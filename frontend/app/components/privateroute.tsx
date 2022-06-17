import React, { Component } from "react";
import { AuthToken } from "../lib/auth_token";
import Router from 'next/router'
//import MsApi from '../lib/msapi'

export default function privateRoute(WrappedComponent: JSX.IntrinsicAttributes) {
    return class extends Component {
        state = {
            auth: new AuthToken(this.props.token)
        };
        props = {};
        apichecktimer = null;
        static getInitialProps = async ({server,pathname,query,req,res}) => {
            // Grab the auth token from the cookies. req only exists on server
            // TODO: Make this work on client for <Link> redirects.
            const auth = AuthToken.fromNext(req);
            const initialProps = {auth: auth, user:"",token: auth.token, pathname: pathname, query: query};
            //console.log(initialProps);
            //Check for expired auth. This should likely be replaced with valid
            //We can do some logic here for refresh tokens if we want to handle "remember me" boxes.
            if (auth.isExpired()) {
                console.log("Auth is expired");
                if (res)
                {
                    console.log("Rewriteing head on server");
                    if (typeof res.writeHead === 'function')
                    {
                        res.writeHead(302, {location: '/login?next=' + req.url});
                        res.end()
                    }

                    return {}; // Return nothing, since we should be redirecting.
                }
                else
                {
                    console.log("Rewriting head on client");
                    //We're on client
                    if (typeof document !== 'undefined')
                    {
                        Router.push('/login?next=' + pathname);
                    }
                }
            }
            else {
                console.log("Auth is NOT expired");
                initialProps.user = auth.decodedToken.sub;
            }
            //if (WrappedComponent.getInitialProps) {
            //  const wrappedProps = await WrappedComponent.getInitialProps(initialProps);
            //  return { ...wrappedProps, auth };
            //}
            return initialProps;
        }

        componentDidMount = () => {
            //This is required to turn auth into an actual AuthToken instance, for passing into the component below.
            this.setState({ auth: new AuthToken(this.props.auth.token) })
        }
        
        render = () => {
            //Grab auth from this.state instead of from props, this ensures we get an actual instance of AuthToken instead of a JSON representation of it
            //We may not need to do this...
            const { auth, ...propsWithoutAuth } = this.props;
            return <WrappedComponent auth={this.state.auth} {...propsWithoutAuth} />;
        }
    };
}
