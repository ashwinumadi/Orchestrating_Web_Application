#FROM node:15.13-alpine as build

# Set the working directory in the container
#WORKDIR /react

# Copy the package.json and package-lock.json files to the container
#COPY package*.json ./

# Install the dependencies
#RUN npm install

# Copy the entire application to the container
#COPY . .

# Build the React app
#RUN npm run build

#CMD ["npm", "start"]
# Use a smaller base image for the production image
#FROM nginx:alpine

# Copy the built files from the build image to the NGINX web server directory
#COPY --from=build /react/build /usr/share/nginx/html

# Expose port 80 for the NGINX web server
#EXPOSE 80

# The default command to start NGINX when the container starts
#CMD ["nginx", "-g", "daemon off;"]
FROM node:15.13-alpine
WORKDIR /react
COPY . .
RUN npm install
RUN npm run build
