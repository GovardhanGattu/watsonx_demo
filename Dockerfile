FROM python:3.11
RUN pip install --upgrade pip setuptools
WORKDIR /watsonx
COPY . /watsonx
RUN pip install -r requirements.txt
ENV FLASK_ENV production
EXPOSE 3000
CMD ["python","-u","app.py"]



