import convertapi


NAME = 'Converting'
# args = ('document', 'document_name', 'convert_api_secret')
response = ('images',)


JOB_STATUS_FRESH = "fresh"
JOB_STATUS_INPROGRESS = "in_progress"
JOB_STATUS_SUCCESS = "success"
JOB_STATUS_ERROR = "error"
ALLOWED_TYPES = {'jpg', 'png', 'tiff', 'pdf', 'docx', 'xls', 'xlsx', 'csv'}


def clogic(access, **data):
    job_id = data.get("job_id")
    access.set_job_id(job_id)

    document_name, bulk_job = access.jobs.document_name.get(), access.jobs.bulk_job.get(refresh=False)
    secret = access.convert_api_secret.get()

    if bulk_job:
        subfile_names = access.jobs.subfile_names.get(refresh=False)
        if not subfile_names:
            access.jobs.frontend_status.set(JOB_STATUS_ERROR)
            return {'statusCode': 500, 'body': f"Bulk job {job_id} has empty subfile_names."}

        bulk_document_bytes = access.subfiles.get()
        job_images = []
        for document_bytes, document_name in zip(bulk_document_bytes, subfile_names):
            document_images = call_convert(secret, document_bytes, document_name, "png")
            job_images.extend(document_images["images"])

    else:
        document_bytes = access.document.get()
        job_images = call_convert(secret, document_bytes, document_name, "png")["images"]

    access.images.set(job_images)
    access.jobs.pages_in_document.set(len(job_images))
    
    if data.get('test') == True:
        return job_images


def call_convert(convertapi_secret, doc_bytes, doc_filename, image_type='jpg'):
    if image_type not in ('jpg', 'png'):
        raise ValueError(f'image_type must be either jpg or png')
    if doc_filename.endswith(f'.{image_type}'):
        return {"images": [doc_bytes]}

    convertapi.api_secret = convertapi_secret

    upload_io = convertapi.UploadIO(doc_bytes, filename=doc_filename)
    response = convertapi.convert(image_type, {'File': upload_io})

    img_bytes_list = []
    for img in response.files:
        img.io.seek(0)
        img_bytes_list.append(img.io.getvalue())
    return {"images": img_bytes_list}
