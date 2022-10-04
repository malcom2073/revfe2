import Head from 'next/head'
//import Layout, { siteTitle } from '../components/layout'
//import utilStyles from '../styles/utils.module.css'
import Router from 'next/router'
import Component from 'react'
//import Date from '../components/date'
import { create } from 'apisauce'
//import MSNavBar from '../components/navbar'
//import MSAdminSideBar from '../components/adminsidebar'
import Link from 'next/link'
//import MsApi from '../lib/msapi'
import { AuthToken } from "../lib/auth_token";
//import { Container, Row, Col } from '@nextui-org/react';
//const { SubMenu } = Menu;
//const { Header, Content, Sider } = Layout;
import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import Badge from '@mui/material/Badge';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MailIcon from '@mui/icons-material/Mail';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MoreIcon from '@mui/icons-material/MoreVert';
import Button from '@mui/material/Button';
import MsApi from '../lib/msapi'
import modules from '../modules';
type Props = {
    meta: {
        title: string,
        description: string,
        keywords:string,

    },
    pathname: string,
    title: string,
    query: {
        slug:string
    },
    auth: any
  };

  const Search = styled('div')(({ theme }) => ({
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginRight: theme.spacing(2),
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      marginLeft: theme.spacing(3),
      width: 'auto',
    },
  }));
  
  const SearchIconWrapper = styled('div')(({ theme  }) => ({
    padding: theme.spacing(0, 2),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  }));
  
  const StyledInputBase = styled(InputBase)(({ theme }) => ({
    color: 'inherit',
    '& .MuiInputBase-input': {
      padding: theme.spacing(1, 1, 1, 0),
      // vertical padding + font size from searchIcon
      paddingLeft: `calc(1em + ${theme.spacing(4)})`,
      transition: theme.transitions.create('width'),
      width: '100%',
      [theme.breakpoints.up('md')]: {
        width: '20ch',
      },
    },
  }));
  const handleMenuClose = () => {
    //setAnchorEl(null);
    //handleMobileMenuClose();
  };
  const menuId = 'primary-search-account-menu';
  

  export default function pageLayout(WrappedComponent: any) {
    return class extends React.Component {
        public apichecktimer: number;
        public open: boolean;
        public props: Props;
        public state: {
            navmenuopen: boolean,
            anchorEl: any,
            pathname: any
        }
        constructor(props:any) {
            super(props);
            this.props = props;
            this.apichecktimer = 0;
            this.open = false;
            this.state = {navmenuopen:false,anchorEl:null,pathname: null}
            
        }
        handleClick = (event: React.MouseEvent<HTMLElement>) => {
            this.setState({navmenuopen:true})
          };
          handleClose = () => {
            this.setState({navmenuopen:false})
          };
        render = () => {
            var renderMenu = (
                <Menu
                  anchorEl={this.state.anchorEl}
                  id={menuId}
                  keepMounted
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={this.state.navmenuopen}
                  onClose={this.handleClose}
                >
                  <MenuItem onClick={this.handleClose}>Profile</MenuItem>
                  <MenuItem><Link href="/logout"passHref>Logout</Link></MenuItem>
                </Menu>
              )
            console.log("pageLayout::render");
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
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ display: { xs: 'none', sm: 'block' } }}
          >
            MikesShop
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
          {modules.map((module) => (
              <Button
                key={module.name}
                href={"/mod/"+module.name}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                    {module.name}
              </Button>      
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
          {(this.props.auth) ? (
              <Button color="inherit" onClick={this.handleClick}>{this.props.auth.decodedToken.sub.user.username}</Button>
          ) : ( <Link href="/login"passHref><Button color="inherit">Login</Button></Link> )}
           {renderMenu}
        </Toolbar>
      </AppBar>
      {/*renderMobileMenu*/}
     
    </Box>
                            <WrappedComponent {...this.props} />
                </>
            )
        }
        checkAuth = () => {
            //{/*<Link href="/logout"passHref><Button color="inherit">{this.props.auth.decodedToken.sub.user.username}</Button></Link> */}
          // calling fromNext with undefined only returns the token on the client.
            const token = AuthToken.fromNext(undefined);
            var currdate = new Date();
            var tokendate = new Date(token.decodedToken.exp * 1000)
            if (token &&  currdate > tokendate) {
                //Router.push('/login?next=' + this.state.pathname);
            }
            else {
                if (token) {
                    // if it's within 60 seconds of expiring, request a new one 
                    tokendate.setSeconds(tokendate.getSeconds() - 60);
                    if (currdate > tokendate) {
                        // Token is not yet expired, but is within 1 minute of expiring. Refresh it.
                        var api = new MsApi();
                        api.refreshToken();
                    }
                }
                else {
                    // TODO: Refresh the page since we're logged out?
                    //Router.push('/login?next=' + this.state.pathname);
                    Router.push(this.state.pathname);
                }
            }
        }
        static getInitialProps = async(ctx: any) => {
            const auth = AuthToken.fromNext(ctx.req);
            console.log("pagelayout::getInitialProps");
            console.log(auth);
            console.log(ctx);
            if (WrappedComponent.getInitialProps) {
              const wrappedProps = await WrappedComponent.getInitialProps(ctx);
              
              const initialProps = {auth: auth, user:"",token: auth.token, pathname: ctx.pathname, query: ctx.query};
              return { ...wrappedProps, auth:auth, query:ctx.query,pathname:ctx.pathname };
            }
            if (!auth.isExpired()) {
            return {auth:auth,query:ctx.query,pathname:ctx.pathname};
            }
            else
            {
                return {query:ctx.query,pathname:ctx.pathname};
            }
        }
        componentWillUnmount = () => {
            clearInterval(this.apichecktimer);
        }
        componentDidMount = async () => {
            //var msapi = new MsApi();
            //const navBar = await msapi.getUserNavbar(null);
            //this.setState({navBar:navBar,isLoading: false,auth: AuthToken.fromNext(null)});
            this.apichecktimer = window.setInterval(() => this.checkAuth(),5000); //Check every 5 seconds
            //var profileobj = await msapi.getUserList();
            //This is required to turn auth into an actual AuthToken instance, for passing into the component below.
            //this.setState({ isLoading: false,auth: new AuthToken(this.props.auth.token) ,profile:profileobj })
        }
    }    
}