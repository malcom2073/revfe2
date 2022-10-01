FROM node:12

ENV PORT 3000

# Create app directory
RUN mkdir -p /usr/src/app

# Installing dependencies
#COPY package.json /usr/src/app/
#RUN npm install

# Copying source files
WORKDIR /usr/src/app
COPY app /usr/src/app/
#RUN rm -rf node_modules
#RUN rm -rf .git
#RUN rm -rf package-lock.json
#RUN npm install
#RUN npm install express --save
# Building app
#RUN npm run build
EXPOSE 3000
#RUN npm run build

# Running the app
#CMD [ "npm", "start" ]
CMD bash -c "npm install && npm run build && npm start"
# Running the app
#CMD "npm" "run" "dev"
