import { AuthToken } from '../lib/auth_token';
import { ApisauceInstance, create } from 'apisauce';
import Router from 'next/router';

export default class MsApi extends Object {
  api: ApisauceInstance;
  constructor() {
    super();
    var token = AuthToken.fromNext(undefined);
    var headers = {
      Authorization: '',
      Accept: 'application/vnd.github.v3+json'
    };
    if (token) {
      headers.Authorization = token.authorizationString();
    }
    this.api = create({
      baseURL: process.env.REACT_APP_MSAPI_ENDPOINT,
      headers: headers
    });
  }
  async refreshToken() {
    const response = await this.api.post('/api/auth/renew');
    if (response.problem) {
      switch (response.problem) {
        case 'CLIENT_ERROR':
          if (response.status == 401) {
            alert('Invalid credentials');
            return;
            //Bad authentication!
          }
          break;
        default:
          break;
      }
      alert('Unknown error');
    }
    localStorage.setItem('jwt_auth', response.data.access_token);
    AuthToken.storeToken(response.data.access_token);
  }
  // Returns a JSON of info for the currently logged in user.
  async getUserInfo() {
    var token = AuthToken.fromNext();
    const response = await this.api.get(
      '/api/users/' + token.decodedToken.sub.user_id
    );
    // TODO: Handle more of these errors.
    if (response.problem) {
      switch (response.problem) {
        case 'CLIENT_ERROR':
          if (response.status == 401) {
            // TOOD: Figure out how we want to handle this redirect.
            // Since the API is used on several pages, should it push the error response back to the page?
            // If so, need a generic way for pages to handle auth errors and redirect to login.
            Router.push('/login?next=/');
            //alert('Invalid credentials');
            return null;
            //Bad authentication!
          }
          break;
        default:
          break;
      }
      alert('Unknown error');
    }
    return response.data.users[0];
  }
  async getUserNavbar(ctx) {
    var token = AuthToken.fromNext();
    if (token && token.isValid()) {
      return {
        menuleft: [
          {
            title: 'Home',
            link: '/',
            type: 'link'
          },
          {
            title: 'Forum',
            link: '/forums',
            type: 'link'
          },
          {
            title: 'Blog',
            link: '/blog',
            type: 'link'
          },
          {
            title: 'Private',
            link: '/private',
            type: 'link'
          },
          {
            title: 'Profile',
            link: '/profile',
            type: 'link'
          },
          {
            title: 'Users',
            link: '/users',
            type: 'link'
          }
        ],
        menuright: [
          {
            title: 'User',
            type: 'dropdown',
            links: [
              {
                title: 'Login',
                type: 'link',
                link: '/login'
              },
              {
                title: '',
                type: 'divider'
              },
              {
                title: 'Sign-Up',
                type: 'link',
                link: '/create'
              }
            ]
          }
        ]
      };
    } else {
      return {
        menuleft: [
          {
            title: 'Home',
            link: '/',
            type: 'link'
          },
          {
            title: 'Forum',
            link: '/forums',
            type: 'link'
          },
          {
            title: 'Blog',
            link: '/blog',
            type: 'link'
          },
          {
            title: 'Private',
            link: '/private',
            type: 'link'
          },
          {
            title: 'Profile',
            link: '/profile',
            type: 'link'
          },
          {
            title: 'Users',
            link: '/users',
            type: 'link'
          }
        ],
        menuright: [
          {
            title: 'Guest',
            type: 'dropdown',
            links: [
              {
                title: 'Login',
                type: 'link',
                link: '/login'
              },
              {
                title: '',
                type: 'divider'
              },
              {
                title: 'Sign-Up',
                type: 'link',
                link: '/create'
              }
            ]
          }
        ]
      };
    }
    console.log(ctx);
    var token = '';
    // This can be run from server or client. Server grabs the auth token from serverside storage,
    // the browser grabs it from a cookie.
    if (ctx && 'req' in ctx) {
      token = AuthToken.fromNext(ctx.req);
    } else {
      token = AuthToken.fromNext(null);
    }

    // Call into our API, with the token
    // TODO: Wrap the apisauce stuff into a class
    var headers = { Accept: 'application/vnd.github.v3+json' };
    if (token) {
      headers.Authorization = token.authorizationString();
    }
    const api = create({
      baseURL: process.env.REACT_APP_MSAPI_ENDPOINT,
      headers: headers
    });
    const response = await api.get('/api/getNavbar');
    switch (response.problem) {
      case 'CLIENT_ERROR':
        if (response.status == 401) {
          //TODO: Handle this, it should never happen, but other errors may?
          console.log('Bad Auth');
          return {};
          //Bad authentication!
        }
        break;
      default:
        break;
    }
    return response.data;
  }
  // Returns a JSON of info for the currently logged in user.
  async getUser(uid) {
    //        var token = AuthToken.fromNext();
    const response = await this.api.get('/api/users/' + uid);
    // TODO: Handle more of these errors.
    if (response.problem) {
      switch (response.problem) {
        case 'CLIENT_ERROR':
          if (response.status == 401) {
            // TOOD: Figure out how we want to handle this redirect.
            // Since the API is used on several pages, should it push the error response back to the page?
            // If so, need a generic way for pages to handle auth errors and redirect to login.
            Router.push('/login?next=/');
            //alert('Invalid credentials');
            return null;
            //Bad authentication!
          }
          break;
        default:
          break;
      }
      alert('Unknown error');
    }
    return response.data.users[0];

    /*const response = await this.api.get('/api/getUser',{'userid' : uid});
        // TODO: Handle more of these errors.
        if (response.problem) {
            switch (response.problem) {
                case 'CLIENT_ERROR':
                    if (response.status == 401)
                    {
                        // TOOD: Figure out how we want to handle this redirect.
                        // Since the API is used on several pages, should it push the error response back to the page?
                        // If so, need a generic way for pages to handle auth errors and redirect to login.
                        Router.push('/login?next=/')
                        //alert('Invalid credentials');
                        return null
                        //Bad authentication!
                    }
                    break;
                default:
                    break;
            }
            alert('Unknown error');
        }
        return response.data.data;*/
  }
  async getUserList() {
    var token = AuthToken.fromNext();
    const response = await this.api.get('/api/users');
    // TODO: Handle more of these errors.
    if (response.problem) {
      switch (response.problem) {
        case 'CLIENT_ERROR':
          if (response.status == 401) {
            // TOOD: Figure out how we want to handle this redirect.
            // Since the API is used on several pages, should it push the error response back to the page?
            // If so, need a generic way for pages to handle auth errors and redirect to login.
            Router.push('/login?next=/');
            //alert('Invalid credentials');
            return null;
            //Bad authentication!
          }
          break;
        default:
          break;
      }
      alert('Unknown error');
    }
    return response.data.users;
    /*
        const response = await this.api.get('/api/userlist');
        // TODO: Handle more of these errors.
        if (response.problem) {
            switch (response.problem) {
                case 'CLIENT_ERROR':
                    if (response.status == 401)
                    {
                        // TOOD: Figure out how we want to handle this redirect.
                        // Since the API is used on several pages, should it push the error response back to the page?
                        // If so, need a generic way for pages to handle auth errors and redirect to login.
                        Router.push('/login?next=/')
                        //alert('Invalid credentials');
                        return null
                        //Bad authentication!
                    }
                    break;
                default:
                    break;
            }
            alert('Unknown error');
        }
        return response.data.data;*/
  }
}
