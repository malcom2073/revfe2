import React from 'react';
import pageLayout from '../../components/pagelayout'
import privateRoute from '../../components/privateroute'
import Document, { Html, Head, Main, NextScript } from 'next/document';
//import { Button} from 'antd/dist/antd';
import Button from '@mui/material/Button';

class Private extends React.Component {
  constructor(props: any)
  {
      super(props);
  }
  componentDidMount = () => {
      //Router.push('/blog');
  }
  
  render() {
      return (
          <>
<Button variant="contained">Private Page!</Button>
          </>
      )
  }

}
export default {
    routeProps: { // This gets passed straight to react-router
        path: '/private', // Where the module lives in the nav hierarchy
        component: privateRoute(pageLayout(Private)) // The actual component itself
    },
    name: 'private' // The name of the module
};