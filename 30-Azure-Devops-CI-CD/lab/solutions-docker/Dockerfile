# From https://docs.microsoft.com/en-us/azure/devops/pipelines/process/container-phases?view=azure-devops#linux-based-containers
# Images based on Alpine Linux, don't satisfy minimum requirements for Azure Devops as container jobs.
FROM python:3.7

RUN mkdir /app

WORKDIR /app 

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app/* app/

COPY tests/* tests/ 

EXPOSE 5000

LABEL maintainer = "Angel Sevilla Camins"

# Linux based container should not define an ENTRYPOINT
CMD ["python", "app/app.py"]