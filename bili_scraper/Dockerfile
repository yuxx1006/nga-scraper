FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5020

CMD ["python", "./bli_search.py"]


