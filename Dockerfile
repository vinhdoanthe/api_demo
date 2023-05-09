FROM --platform=$BUILDPLATFORM python:3.10 AS builder
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as dev-envs
RUN <<EOF
apt-get update && apt-get install

apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

EOF

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
