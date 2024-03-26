FROM python:3.10-alpine3.15
WORKDIR /watsonx
COPY . /watsonx
RUN pip install -r requirements.txt
ENV GOOGLE_API_KEY="AIzaSyBC0sqErda5UEF8AhUvsJZTSc7EH1KwZAo"
CMD python app.py



