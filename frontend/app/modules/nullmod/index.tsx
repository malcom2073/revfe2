import React from 'react';
import pageLayout from '../../components/pagelayout'
import privateRoute from '../../components/privateroute'
import Document, { Html, Head, Main, NextScript } from 'next/document';
//import { Button} from 'antd/dist/antd';
import Button from '@mui/material/Button';

class NullMod extends React.Component {
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
NullMod
          </>
      )
  }

}
export default NullMod