FROM python:3.11.6

RUN apt-get update && \
    apt-get install locales -y\
    && echo "LC_TIME=fr_FR.UTF-8" > /etc/locale.gen\
    && locale-gen fr_FR.UTF-8\
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY requirements.txt .

RUN pip install -r requirements.txt



COPY . /app
COPY ./.streamlit /app

ENV LANG fr_FR.ISO-8859-15
ENV LANGUAGE fr_FR:fr  
# ENV LC_ALL fr_FR.ISO-8859-15 
ENV LC_TIME fr_FR.UTF-8

ENV NVIDIA_VISIBLE_DEVICES all

ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# RUN ldconfig

CMD streamlit run app/Index.py --server.port=8501 --server.address=0.0.0.0