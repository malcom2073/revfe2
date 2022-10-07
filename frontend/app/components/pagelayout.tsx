//import Head from 'next/head'
import Router from 'next/router';
//import Component from 'react'
//import { create } from 'apisauce'
import Link from 'next/link';
import { AuthToken } from '../lib/auth_token';
import * as React from 'react';
//import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
//import InputBase from '@mui/material/InputBase';
//import Badge from '@mui/material/Badge';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
//import SearchIcon from '@mui/icons-material/Search';
import AccountCircle from '@mui/icons-material/AccountCircle';
//import MailIcon from '@mui/icons-material/Mail';
//import NotificationsIcon from '@mui/icons-material/Notifications';
import MoreIcon from '@mui/icons-material/MoreVert';
import Button from '@mui/material/Button';
import MsApi from '../lib/msapi';
import modules from '../modules';
type Props = {
  meta: {
    title: string;
    description: string;
    keywords: string;
  };
  pathname: string;
  title: string;
  query: {
    slug: string;
  };
  auth: any;
};

const handleMenuClose = () => {
  //setAnchorEl(null);
  //handleMobileMenuClose();
};
const menuId = 'primary-search-account-menu';

export default function pageLayout(WrappedComponent: any) {
  return class extends React.Component {
    public apichecktimer: number;
    static displayName = 'Base';
    public open: boolean;
    public props: Props;
    public state: {
      navmenuopen: boolean;
      anchorEl: any;
      pathname: any;
    };
    constructor(props: any) {
      super(props);
      this.props = props;
      this.apichecktimer = 0;
      this.open = false;
      const token = AuthToken.fromNext(undefined);
      this.state = {
        navmenuopen: false,
        anchorEl: null,
        pathname: null,
        auth: token
      };
    }
    handleClick = (event: React.MouseEvent<HTMLElement>) => {
      this.setState({ navmenuopen: true });
    };
    handleClose = () => {
      this.setState({ navmenuopen: false });
    };
    render = () => {
      var renderMenu = (
        <Menu
          anchorEl={this.state.anchorEl}
          id={menuId}
          keepMounted
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'right'
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right'
          }}
          open={this.state.navmenuopen}
          onClose={this.handleClose}
        >
          <MenuItem onClick={this.handleClose}>Profile</MenuItem>
          <MenuItem>
            <Link href="/logout" passHref>
              Logout
            </Link>
          </MenuItem>
        </Menu>
      );
      const { badauth, ...propsWithoutAuth } = this.props;
      console.log('pageLayout::render');
      console.log(this.props);
      return (
        <>
          <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
              <Toolbar>
                <IconButton
                  size="large"
                  edge="start"
                  color="inherit"
                  aria-label="open drawer"
                  sx={{ mr: 2 }}
                >
                  <MenuIcon />
                </IconButton>
                <Link href="/" passHref>
                  <Typography
                    variant="h6"
                    noWrap
                    component="div"
                    sx={{ display: { xs: 'none', sm: 'block' } }}
                  >
                    MikesShop
                  </Typography>
                </Link>
                <Box sx={{ flexGrow: 0, display: { xs: 'none', md: 'flex' } }}>
                  <Link
                    key={'TopLevelPublic' + 'link'}
                    href={'/toplevelpublic'}
                    passHref
                  >
                    <Button
                      key={'TopLevelPublic'}
                      sx={{ my: 2, color: 'white', display: 'block' }}
                    >
                      {'TopLevelPublic'}
                    </Button>
                  </Link>
                </Box>
                <Box sx={{ flexGrow: 0, display: { xs: 'none', md: 'flex' } }}>
                  <Link
                    key={'TopLevelPrivate' + 'link'}
                    href={'/toplevelprivate'}
                    passHref
                  >
                    <Button
                      key={'TopLevelPrivate'}
                      sx={{ my: 2, color: 'white', display: 'block' }}
                    >
                      {'TopLevelPrivate'}
                    </Button>
                  </Link>
                </Box>

                <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                  {modules.map(module => (
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
                    </Link>
                  ))}
                </Box>

                <Box sx={{ flexGrow: 1 }} />
                <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
                  <IconButton
                    size="large"
                    edge="end"
                    aria-label="account of current user"
                    aria-controls={menuId}
                    aria-haspopup="true"
                    color="inherit"
                  >
                    <AccountCircle />
                  </IconButton>
                </Box>
                <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
                  <IconButton
                    size="large"
                    aria-label="show more"
                    aria-haspopup="true"
                    color="inherit"
                  >
                    <MoreIcon />
                  </IconButton>
                </Box>
                {this.state && this.state.auth && this.state.auth.isValid() ? (
                  <Button color="inherit" onClick={this.handleClick}>
                    {this.state.auth.decodedToken.sub.user.username}
                  </Button>
                ) : (
                  <Link href="/login" passHref>
                    <Button color="inherit">Login</Button>
                  </Link>
                )}
                {renderMenu}
              </Toolbar>
            </AppBar>
          </Box>
          <WrappedComponent auth={this.state.auth} {...propsWithoutAuth} />
        </>
      );
    };
    checkAuth = () => {
      const token = AuthToken.fromNext(undefined);
      var currdate = new Date();
      var tokendate = new Date(token.decodedToken.exp * 1000);
      if (token && currdate > tokendate) {
        //Router.push('/login?next=' + this.state.pathname);
      } else {
        if (token) {
          // if it's within 60 seconds of expiring, request a new one
          tokendate.setSeconds(tokendate.getSeconds() - 60);
          if (currdate > tokendate) {
            // Token is not yet expired, but is within 1 minute of expiring. Refresh it.
            var api = new MsApi();
            api.refreshToken();
          }
        } else {
          // TODO: Refresh the page since we're logged out?
          //Router.push('/login?next=' + this.state.pathname);
          Router.push(this.state.pathname);
        }
      }
    };
    static getInitialProps = async (ctx: any) => {
      const auth = AuthToken.fromNext(ctx.req);
      console.log('pagelayout::getInitialProps');
      //console.log(auth);
      //console.log(ctx);
      if (WrappedComponent.getInitialProps) {
        const wrappedProps = await WrappedComponent.getInitialProps(ctx);

        const initialProps = {
          auth: auth,
          user: '',
          token: auth.token,
          pathname: ctx.pathname,
          query: ctx.query
        };
        return {
          ...wrappedProps,
          auth: auth,
          query: ctx.query,
          pathname: ctx.pathname
        };
      }
      if (!auth.isExpired()) {
        return { auth: auth, query: ctx.query, pathname: ctx.pathname };
      } else {
        return { query: ctx.query, pathname: ctx.pathname };
      }
    };
    componentWillUnmount = () => {
      clearInterval(this.apichecktimer);
    };
    componentDidMount = async () => {
      //var msapi = new MsApi();
      //const navBar = await msapi.getUserNavbar(null);
      //this.setState({navBar:navBar,isLoading: false,auth: AuthToken.fromNext(null)});
      this.apichecktimer = window.setInterval(() => this.checkAuth(), 5000); //Check every 5 seconds
      //var profileobj = await msapi.getUserList();
      //This is required to turn auth into an actual AuthToken instance, for passing into the component below.
      //this.setState({ isLoading: false,auth: new AuthToken(this.props.auth.token) ,profile:profileobj })
    };
  };
}
