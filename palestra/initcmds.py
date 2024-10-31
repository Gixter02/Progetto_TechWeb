from bookings.models import Prenotazione
from django.utils import timezone

def erase_old_bookings():
    print('Cancello le vecchie prenotazioni')
    vecchie_prenotazioni = Prenotazione.objects.filter(data_prenotazione__lt=timezone.now().date())
    vecchie_prenotazioni.delete()