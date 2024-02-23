###########
# BUILDER #
###########
FROM public.ecr.aws/lambda/python:3.10 as builder

RUN pip install --upgrade pip
RUN pip install opencv-python-headless --target "${LAMBDA_TASK_ROOT}"
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY natural_disaster.model /var/task

#########
# FINAL #
#########
FROM public.ecr.aws/lambda/python:3.10
RUN pip install --upgrade pip

COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

COPY . ${LAMBDA_TASK_ROOT}

CMD [ "handler.main" ]
