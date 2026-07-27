import csv
import io
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import UploadFileModel, UserPointModel

User = get_user_model()


@shared_task
def process_csv_file_task(file_id):
    try:
        upload_instance = UploadFileModel.objects.get(id=file_id)
        # uploaded_by = upload_instance.uploaded_by

        upload_instance.status = UploadFileModel.Status.PROCESSING
        upload_instance.save()

        csv_file = upload_instance.file.open('r')
        file_data = csv_file.read()
        if isinstance(file_data, bytes):
            file_data = file_data.decode('utf-8-sig')

        io_string = io.StringIO(file_data)
        reader = csv.DictReader(io_string)
        # print(reader)

        points_to_create = []

        for row in reader:
            # print(row)
            name = row.get('name') or row.get('Name')
            lat = row.get('lat') or row.get('latitude')
            lon = row.get('lon') or row.get('longitude')
            # print(name, lat, lon)

            if not name or lat is None or lon is None:
                return False

            points_to_create.append(
                UserPointModel(
                    # uploaded_by=upload_instance.uploaded_by,
                    owner = upload_instance.owner,
                    name=name.strip(),
                    latitude=float(lat),
                    longitude=float(lon),
                    source_file=upload_instance
                )
            )

        if points_to_create:
            UserPointModel.objects.bulk_create(points_to_create)
        # print(len(points_to_create))

        upload_instance.status = UploadFileModel.Status.COMPLETED
        upload_instance.save()

    except Exception as e:
        upload_instance = UploadFileModel.objects.filter(id=file_id).first()
        if upload_instance:
            upload_instance.status = UploadFileModel.Status.FAILED
            upload_instance.error_message = str(e)
            upload_instance.save()