const express = require('express');
const next = require('next');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const port = process.env.PORT || 3000;
const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

const apiPaths = {
  '/api': {
    //        target: 'http://backend:5000',
    //        target: 'https://api.mikesshop.net',
    //          target: process.env.NEXT_PUBLIC_MSAPI_ENDPOINT,
    target: 'http://localhost:5000/',
    //pathRewrite: {
    //    '^/api': '/api'
    //},
    changeOrigin: true
  }
};

const isDevelopment = process.env.NODE_ENV !== 'production';

app
  .prepare()
  .then(() => {
    const server = express();
    server.set('trust proxy', true);

    server.use('/api', createProxyMiddleware(apiPaths['/api']));
    server.use(
      '/upload',
      express.static(path.join(__dirname, 'uploads/upload'))
    );

    server.all('*', (req: any, res: any) => {
      return handle(req, res);
    });

    server.listen(port, (err: any) => {
      if (err) throw err;
      console.log(`> Ready on http://localhost:${port}`);
    });
  })
  .catch((err: any) => {
    console.log('Error:::::', err);
  });
export {} // Needed to make typescript treat this file like a module