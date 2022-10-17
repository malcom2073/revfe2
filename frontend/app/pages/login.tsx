import Head from 'next/head';
import React from 'react';
import pageLayout from '../components/pagelayout';
import LoginForm from '../components/loginform';

class LoginPage extends React.Component {
  props: { query: any };
  state: { alertmsg: string; alerttype: any };
  constructor(props: any) {
    super(props);
    this.props = props;
    this.state = { alertmsg: '', alerttype: undefined };
  }

  onLoginError = (msg: any) => {
    this.setState({ alertmsg: msg, alerttype: 'error' });
  };
  render = () => {
    console.log('Query');
    console.log(this.props.query);
    return (
      <>
        <Head>
          <meta name="pathname" content="/login"></meta>
        </Head>
        <div
          className="App"
          style={{
            height: '100vh',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center'
          }}
        >
          <header className="App-header">
            <div className="Login">
              {this.props.query && this.props.query.next ? (
                <LoginForm
                  next={this.props.query.next}
                  onError={this.onLoginError.bind(this)}
                ></LoginForm>
              ) : (
                <LoginForm
                  next={'/'}
                  onError={this.onLoginError.bind(this)}
                ></LoginForm>
              )}
            </div>
          </header>
        </div>
      </>
    );
  };
}
export default LoginPage;
