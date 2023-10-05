# 1. Inherit FROM a suitable base image, for example, python 3.7-alpine
FROM python:3.7-alpine

# 2. Create the folder /app for our app
RUN mkdir /app

# 3. Change working directory in the image to /app
WORKDIR /app

# 4. Expose API port (TCP/5000) to the outside
EXPOSE 5000

# 5. Copy requirements file to /app
COPY requirements.txt /app

# 6. Install dependencies by running pip install
RUN pip install -r requirements.txt

# 7. Copy source code from the filesystem (app.py) to the container (/app)
COPY app.py /app

# 8. Add two labels, namely, maintainer and version
LABEL maintainer = "Jevon van Dijk"
LABEL version = "v1"

# 9. Add an entrypoint and command to the image
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]