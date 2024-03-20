###########
# BUILDER #
###########
FROM public.ecr.aws/lambda/python:3.11 as builder

RUN pip3 install --upgrade pip

RUN pip3 install opencv-python --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install tensorflow==2.13.0 --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install boto3 --target "${LAMBDA_TASK_ROOT}"
COPY natural_disaster.h5  .
COPY handler.py .
#########
# FINAL #
#########
# Work in the application directory

FROM public.ecr.aws/lambda/python:3.11
RUN pip3 install --upgrade pip
RUN yum update -y && yum install -y mesa-libGL-devel
COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

#COPY natural_disaster.keras /tmp/
COPY . ${LAMBDA_TASK_ROOT}
WORKDIR ${LAMBDA_TASK_ROOT}
CMD [ "handler.main" ]