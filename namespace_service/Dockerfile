FROM python:3.11-slim as stage0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update ; \
    apt-get install -y --no-install-recommends \
        vim

# ------------ dependencies -----------------------

FROM stage0 as stage1

COPY requirements.txt /python_requirements/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /python_requirements/requirements.txt

ENV ROOT_DIR /app

WORKDIR $ROOT_DIR

COPY namespace_service $ROOT_DIR/namespace_service
COPY alembic.ini $ROOT_DIR/namespace_service

# ------------ tests -----------------------

FROM stage1 as tests

COPY requirements.dev.txt /python_requirements/requirements.dev.txt

RUN set -ex ; \
    apt-get update ; \
    apt-get install --no-install-recommends -y \
        gcc \
        make; \
    pip3 install -r /python_requirements/requirements.dev.txt

COPY setup.cfg pylintrc $ROOT_DIR/
COPY Makefile $ROOT_DIR/Makefile
COPY namespace_service_tests $ROOT_DIR/namespace_service_tests

RUN make -f $ROOT_DIR/Makefile \
      ROOT_DIR=$ROOT_DIR \
      PYTHON_DIR=/usr/local/bin \
      ci

# ------------ final -----------------------

FROM stage1 as final

CMD ["python3", "-m", "namespace_service.main"]