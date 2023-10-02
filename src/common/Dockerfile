FROM public.ecr.aws/lambda/python:latest

COPY src/common ./src/common
COPY src/components/convert ./src/components/convert

RUN pip install -r src/components/convert/requirements.txt

WORKDIR .

RUN ls .

CMD ["src.common.handler.lambda_handler"]


