FROM python:3.9.9

COPY . /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT  ["streamlit", "run", "app/Index.py", "--server.port=4000", "--server.address=0.0.0.0"]