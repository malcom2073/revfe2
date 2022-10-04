import React, { lazy, useEffect, useState } from 'react';
//import { Button} from 'antd/dist/antd';
import pageLayout from '../../components/pagelayout'
import Button from '@mui/material/Button';
import Router from 'next/router'

const importModules = (module: any) =>
  lazy(() =>
    import(`../../modules/${module}`).catch(() =>
    import(`../../modules/nullmod`)
    )
  );

class Mod extends React.Component {
    state: {
        views: any
    }
    Components: any;
  constructor(props: any)
  {
      super(props);
      this.Components = {};

      this.Components['Private'] = require('../../modules/private').default;
      this.Components['nullmod'] = require('../../modules/nullmod').default;
      //this.Components['Component2'] = require('./Component2').default;
      //this.Components['Component3'] = require('./Component3').default;
      this.state = {views: undefined}
  }
  componentDidMount = () => {
      var newview = importModules('private');
    this.setState({views: newview});
    console.log(newview);
      //Router.push('/blog');
  }
  
  render() {
    if (this.props.context.slug[0] == "Private") {
        const ComponentToRender = pageLayout(this.Components["Private"]);
        return <ComponentToRender/>
        }
        else {
            const ComponentToRender = this.Components["nullmod"];
            return <ComponentToRender/>
            }
      return (
          <>
          {(this.state.views) ? (
        <div className='container'>{this.state.views}</div>

          ) : (
              <div>Loading</div>
          )}
          </>
      )
      if (this.props.context.slug[0] == "test") {
          return (
              <>Testing</>
          )
      }
      return (
          <>
          {JSON.stringify(this.props.context.slug)}
            <Button variant="contained">Private Page!</Button>
          </>
      )
  }

  

}
export default Mod
export const getServerSideProps = async (context: any) => {
    //console.log(context);
  return {
    props: {context: context.query}, // will be passed to the page component as props
  }
}