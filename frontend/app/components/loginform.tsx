import React from 'react';
import { create } from 'apisauce'
import { AuthToken } from "../lib/auth_token";
import { useRouter } from 'next/router'
import Router from 'next/router'
import FormHelperText from '@mui/material/FormHelperText';
import InputLabel from '@mui/material/InputLabel';
import Input from '@mui/material/Input';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
};
const tailLayout = {
    wrapperCol: { offset: 8, span: 16 },
};
export default class LoginForm extends React.Component {
    props: { next: string, onError: any};
    nextUrl: string;
    constructor(props: any)
    {
        super(props);
        this.props = props;
        this.nextUrl = "";
    }
    onChange = (e) => {
        // Because we named the inputs to match their corresponding values in state, it's
        // super easy to update the state
        this.setState({[e.target.name]: e.target.value});
    }
    onSubmit = async e => {
        e.preventDefault();
        console.log("Login form onsubmit clicked");
        //return false;
        console.log("Login form onsubmit");
        console.log("User: " + e.target.elements.username.value);
        console.log("Pass: " + e.target.elements.password.value)
        console.log(e);
        const api = create({
            baseURL: process.env.REACT_APP_MSAPI_ENDPOINT,
            headers: { Accept: 'application/json' },
        })
        const response = await api.post('/api/auth/authenticate',{ username: e.target.elements.username.value, password: e.target.elements.password.value});
        console.log(response);
        // TODO: Handle more of these errors.
        if (response.problem) {
            switch (response.problem) {
            case 'CLIENT_ERROR':
                if (response.status == 401)
                {
                    if (response.data)
                    {
                        console.log("SADFASDFSAFDSAFD");
                        console.log(this.props);
                        if (this.props.onError)
                        {
                        this.props.onError(response.data.error);
                        }
                        else
                        {
                        alert(response.data.error);
                        }
                    }
                    else
                    {
                    alert('Invalid credentials');
                    }
                return {}
                //Bad authentication!
                }
                break;
            default:
                break;
            }
            alert('Unknown error');
        }
        console.log(response.data)
        console.log(this.props.next);    
        localStorage.setItem('jwt_auth',response.data.access_token);
        AuthToken.storeToken(response.data.access_token);
        if (this.props.next) {
            Router.push(this.props.next);
        }
        else {
            Router.push('/');
        }
        

        return false;

    }

    render() {
        this.nextUrl = this.props.next;
        return (
            <form onSubmit={this.onSubmit.bind(this)}>
            {/*onSubmit={(e) => { e.preventDefault(); alert('Submitted form!'); this.handleClose(); } }*/}
            <Grid container alignItems="center" justify="center" direction="column" rowSpacing="20px">
                <Grid item>
                    <FormControl>
                        <InputLabel htmlFor="emailinput">Email address</InputLabel>
                        <Input name="username" id="emailinput" aria-describedby="my-helper-text" />  
                    </FormControl>
                </Grid>
                <Grid item>
                    <FormControl>
                        <InputLabel htmlFor="passinput">Password</InputLabel>
                        <Input name="password" id="passinput" type="password" aria-describedby="my-helper-text2" />
                    </FormControl>
                </Grid>
                <Grid item>
                    <Button variant="contained" color="primary" type="submit">
                    Submit
                    </Button>
                </Grid>
            </Grid>
            </form>
        );
        /*return (
            <Form name="basic" onFinish={this.onSubmit.bind(this)}>
            <Form.Item
        label="Username"
        name="username"
        rules={[{ required: true, message: 'Please input your username!' }]}
        >
        <Input />
        </Form.Item>

        <Form.Item
        label="Password"
        name="password"
        rules={[{ required: true, message: 'Please input your password!' }]}
        >
        <Input.Password />
        </Form.Item>

        <Form.Item {...tailLayout} name="remember" valuePropName="checked">
        <Checkbox>Remember me</Checkbox>
        </Form.Item>

        <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
            Submit
        </Button>
        </Form.Item>
            </Form>          
        );*/
    }
}