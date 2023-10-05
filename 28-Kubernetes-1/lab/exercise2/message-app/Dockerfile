# 1. Inherit FROM a suitable base image
FROM node:11-stretch-slim

# 2. Copy source code from the filesystem (messageApp) to the container (/messageApp)
COPY messageApp/ ./messageApp

# 3. Change working directory in the image to /messageApp
WORKDIR /messageApp

# 4. Install dependencies by running npm install
RUN npm install

# 5. Define PORT as an environment variable and set it to default to port 80
ENV PORT=80/tcp

# 6. Expose API port (TCP/80) to the outside
EXPOSE ${PORT}

# 7. Add an entrypoint (npm) and command (start) to the image (together this runs npm start by default)
ENTRYPOINT ["npm"]
CMD ["start"]
