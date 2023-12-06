FROM python:3.11.6

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY requirements.txt .

RUN pip install -r requirements.txt



COPY . ./app
COPY .streamlit/config.toml ./app/.streamlit/config.toml
COPY .streamlit/config.toml ./.streamlit/config.toml

# Set the locale
RUN apt-get update && apt-get install -y locales \
    locales-all 
RUN locale-gen fr_FR.UTF-8  
ENV LANG fr_FR.UTF-8  
ENV LANGUAGE fr_FR:nl 
ENV LC_ALL fr_FR.UTF-8  
RUN update-locale LANG=fr_FR.UTF-8

# RUN ldconfig

CMD streamlit run app/Index.py --server.port=8501 --server.address=0.0.0.0