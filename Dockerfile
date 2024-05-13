FROM python:3.10.8
EXPOSE 5000
WORKDIR /Flasks
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask","run","--host","0.0.0.0"]