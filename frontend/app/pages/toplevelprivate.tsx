import React from 'react';
import pageLayout from '../components/pagelayout';
import { Props } from '../components/pagelayout';
import privateRoute from '../components/privateroute';
//import Document, { Html, Head, Main, NextScript } from 'next/document';
//import { Button} from 'antd/dist/antd';
import Button from '@mui/material/Button';

class TopLevelPrivate extends React.Component {
  props: Props;
  constructor(props: any) {
    super(props);
    this.props = props;
  }
  componentDidMount = () => {
    //Router.push('/blog');
  };

  render() {
    return (
      <>
        This is a PRIVATE page! Login will be required
        <br />
        {this.props.auth.isValid() && 'Auth is good'}
        {!this.props.auth.isValid() &&
          'Auth is invalid, this should not be possible'}
      </>
    );
  }
}
export default pageLayout(privateRoute(TopLevelPrivate));
