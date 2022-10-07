import React from 'react';
import pageLayout from '../components/pagelayout';
import privateRoute from '../components/privateroute';
//import Document, { Html, Head, Main, NextScript } from 'next/document';
//import { Button} from 'antd/dist/antd';
import Button from '@mui/material/Button';

class TopLevelPublic extends React.Component {
  constructor(props: any) {
    super(props);
  }
  componentDidMount = () => {
    //Router.push('/blog');
  };

  render() {
    return (
      <>
        This is a public page, no login required.
        <br />
        {this.props.auth.isValid() && 'Auth is good'}
        {!this.props.auth.isValid() && 'Auth is invalid'}
      </>
    );
  }
}
export default pageLayout(TopLevelPublic);
