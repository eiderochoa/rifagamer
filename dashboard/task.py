# Celery
from celery import shared_task
# Celery-progress
from celery_progress.backend import ProgressRecorder
from .models import *

# Celery Task
@shared_task(bind=True)
def generateNumbers(self, rifa):
    from .models import Numeros
    print('Task started')
    # Create the progress recorder instance
	# which we'll use to update the web page
    progress_recorder = ProgressRecorder(self)
    print('start')
    for i in range(10000):
         numero = Numeros(numero=str(i).zfill(5),rifa=rifa)
         numero.save()
         progress_recorder.set_progress(i + 1, 10000, description="Generating")
    print('end')

    return 'Task Complete'
