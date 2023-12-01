FROM python:3.9.9

COPY . /app/

COPY requirements.txt .

COPY Missions.csv .

EXPOSE 8501

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app/Index.py", "--server.port=8501", "--server.address=0.0.0.0"]