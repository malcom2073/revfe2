import React, { lazy, useEffect, useState } from 'react';
//import { Button} from 'antd/dist/antd';
import pageLayout from '../../components/pagelayout';
import privateRoute from '../../components/privateroute';
import Button from '@mui/material/Button';
import Router from 'next/router';
import { CompareSharp } from '@mui/icons-material';
import { AuthToken } from '../../lib/auth_token';
import modules from '../../modules';
type Props = {
  query: any;
};

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
  props: Props;
  Components: any;
  constructor(props: any) {
    super(props);
    this.props = props;
    this.Components = {};
    for (var i = 0; i < modules.length; i++) {
      //ComponentList.push(modules[i][0])
      this.Components[modules[i][0].name] = require('../../modules/' +
        modules[i][0].name.toLowerCase()).default;
    }
    this.Components['nullmod'] = require('../../modules/nullmod').default;
    this.state = { views: undefined };
  }
  componentDidMount = () => {
    var newview = importModules('private');
    this.setState({ views: newview });
    console.log(newview);
    //Router.push('/blog');
  };

  render() {
    if (this.props.query.slug[0] in this.Components) {
      if (this.Components[this.props.query.slug[0]][1]) {
        const ComponentToRender = pageLayout(
          privateRoute(this.Components[this.props.query.slug[0]][0])
        );
        return <ComponentToRender {...this.props} />;
      } else {
        const ComponentToRender = pageLayout(
          this.Components[this.props.query.slug[0]][0]
        );
        return <ComponentToRender {...this.props} />;
      }
    } else {
      const ComponentToRender = pageLayout(this.Components['nullmod']);
      return <ComponentToRender {...this.props} />;
    }
  }
}
export default Mod;
export const getServerSideProps = async (context: any) => {
  //{server,pathname,query,req,res}
  //import modules from '../modules';
  /*modules.map((module: any) => (
                    <Link
                      key={module[0].name + 'link'}
                      href={'/mod/' + module[0].name}
                      passHref
                    >
                      <Button
                        key={module[0].name}
                        sx={{ my: 2, color: 'white', display: 'block' }}
                      >
                        {module[0].name}
                      </Button>
                    </Link>*/
  var ComponentList = [];
  for (var i = 0; i < modules.length; i++) {
    //ComponentList.push(modules[i][0])
    ComponentList.push(
      require('../../modules/' + modules[i][0].name.toLowerCase())
    );
  }
  //  ComponentList.push(require('../../modules/private'));
  //  ComponentList.push(require('../../modules/nullmod'));
  console.log('Mod slug serverside');
  console.log(context);
  const auth = AuthToken.fromNext(context.req);
  const initialProps = {
    //auth: auth.token,
    user: '',
    token: (auth.token != undefined ? auth.token : ""),
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
