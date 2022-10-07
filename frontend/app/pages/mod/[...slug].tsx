import React, { lazy, useEffect, useState } from 'react';
//import { Button} from 'antd/dist/antd';
import pageLayout from '../../components/pagelayout';
import privateRoute from '../../components/privateroute';
import Button from '@mui/material/Button';
import Router from 'next/router';
import { CompareSharp } from '@mui/icons-material';
import { AuthToken } from '../../lib/auth_token';

const importModules = (module: any) =>
  lazy(() =>
    import(`../../modules/${module}`).catch(
      () => import(`../../modules/nullmod`)
    )
  );
class Mod extends React.Component {
  state: {
    views: any;
  };
  Components: any;
  constructor(props: any) {
    super(props);
    this.Components = {};

    var privatereq = require('../../modules/private');

    this.Components['Private'] = privatereq.default;
    console.log('*********************');
    console.log(privatereq);
    this.Components['nullmod'] = require('../../modules/nullmod').default;
    //this.Components['Component2'] = require('./Component2').default;
    //this.Components['Component3'] = require('./Component3').default;
    this.state = { views: undefined };
  }
  componentDidMount = () => {
    var newview = importModules('private');
    this.setState({ views: newview });
    console.log(newview);
    //Router.push('/blog');
  };

  render() {
    if (this.props.query.slug[0] == 'Private') {
      if (this.Components['Private'][1]) {
        const ComponentToRender = pageLayout(
          privateRoute(this.Components['Private'][0])
        );
        return <ComponentToRender {...this.props} />;
      } else {
        const ComponentToRender = pageLayout(this.Components['Private'][0]);
        return <ComponentToRender {...this.props} />;
      }
    } else {
      const ComponentToRender = pageLayout(this.Components['nullmod']);
      return <ComponentToRender {...this.props} />;
    }
    return (
      <>
        {this.state.views ? (
          <div className="container">{this.state.views}</div>
        ) : (
          <div>Loading</div>
        )}
      </>
    );
    if (this.props.context.slug[0] == 'test') {
      return <>Testing</>;
    }
    return (
      <>
        {JSON.stringify(this.props.context.slug)}
        <Button variant="contained">Private Page!</Button>
      </>
    );
  }
}
export default Mod;
export const getServerSideProps = async context => {
  //{server,pathname,query,req,res}
  var ComponentList = [];
  ComponentList.push(require('../../modules/private'));
  ComponentList.push(require('../../modules/nullmod'));
  console.log('Mod slug serverside');
  console.log(context);
  const auth = AuthToken.fromNext(context.req);
  const initialProps = {
    //auth: auth.token,
    user: '',
    token: auth.token,
    pathname: '',
    query: context.query
  };
  console.log(initialProps);
  var foundcomponent = undefined;
  for (var i = 0; i < ComponentList.length; i++) {
    console.log(ComponentList[i].default);
    console.log(
      'Checking component: ' +
        ComponentList[i].default[0].name +
        ' against slug: ' +
        context.query.slug[0]
    );
    if (ComponentList[i].default[0].name == context.query.slug[0]) {
      console.log('Found proper component');
      foundcomponent = ComponentList[i].default;
    }
  }
  if (foundcomponent && foundcomponent[1]) {
    //Private route
    if (auth.isExpired()) {
      console.log('Auth is expired');
      if (context.res) {
        console.log('Rewriteing head on server');
        if (typeof context.res.writeHead === 'function') {
          context.res.writeHead(302, {
            location: '/login?next=' + context.req.url
          });
          context.res.end();
        }

        return {}; // Return nothing, since we should be redirecting.
      } else {
        console.log('Rewriting head on client');
        //We're on client
        if (typeof document !== 'undefined') {
          Router.push('/login?next=' + context.pathname);
        }
      }
    } else {
      console.log('Auth is NOT expired');
      initialProps.user = auth.decodedToken.sub;
    }
    //if (WrappedComponent.getInitialProps) {
    //  const wrappedProps = await WrappedComponent.getInitialProps(initialProps);
    //  return { ...wrappedProps, auth };
    //}
    return { props: initialProps };
  } else {
    return { props: initialProps };
  }

  return {
    props: { context: context.query } // will be passed to the page component as props
  };
};
