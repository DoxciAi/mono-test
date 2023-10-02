import os
import json

from .accessor import Accessor as BaseAccessor, PersistenceConfig, SecretManager, QueueManager
from .accessor import JobsTable, ScenariosTable, UsersTable, BytesAsset, BytesArrayAsset, JsonAsset, JsonArrayAsset, PickleAsset
from ..components.convert.clogic import clogic


class Accessor(BaseAccessor, PersistenceConfig, SecretManager, QueueManager):
    s3_bucket_name = os.getenv('BUCKET_NAME', 'doxci-development-main')


def handle_event(event):
    try:
        record = event['Records'][0]
        message_body = record['body']
        data = json.loads(message_body)
        print(message_body)
        return data
    except Exception as E:
        print(E)
        print(event)
        return event

def handle_clogic(access, data):
    import traceback
    try:
        return clogic(access, **data), None
    except Exception as E:
        return None, traceback.format_exc()


def lambda_handler(event, context):
    access = Accessor()
    print(access)
    access.set_job_id('frontend')
    job1_status, job1_docname = access['jobs']['frontend_status'], access['jobs']['document_name']
    print('status:', job1_status, '- document name:', job1_docname)

    # read event data
    # data = handle_event(event)
    #
    # job_id = data['job_id']
    # access.set_job_id(job_id)
    #
    # access['jobs']['frontend_status'] = "fresh"
    # access['jobs']['bulk_job'] = False
    #
    # job1_status = access['jobs']['frontend_status']
    # job1_docname = access['jobs']['document_name']
    #
    # print('Job:', job_id, '- status:', job1_status, '- document name:', job1_docname)
    #
    # response, error = handle_clogic(access, data)
    #
    # if error is None:
    #     return {
    #         'statusCode': 200,
    #         'body': json.dumps(response)
    #     }
    # elif response is None:
    #     return {
    #         'statusCode': error.get('statusCode', 500),
    #         'body': error
    #     }

