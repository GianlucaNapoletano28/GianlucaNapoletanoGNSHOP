Utente DIPENDENTE (Andare nella sezione staff e inserire il codice dipendente cosi da poter accedere ai vari ordini)

Username   LucaDirettore1
password   Gianluca_1
codice per accedere a sezione staff   2810

PER CREARE UN DIPENDENTE BISOGNA FARLO DALLA SHELL, una volta nella shell si
crea il dipendente con i dati che si vuole, nel mio caso questi :

from gianluca_app.models import Dipendente
Dipendente.objects.create_user(
    username='LucaDirettore1',
    password='Gianluca_1',
    email='lucadirettore1@email.com',
    first_name='Luca',
    last_name='Direttore',
    ruolo='Direttore',
    codice_staff='2810'
)

Utente CLIENTE 1 
Username   GianlucaCliente1
password   Luca_123



Per la registrazione, funziona correttamente, ma dopo alcune modifiche, quando viene creato l'utente da un errore, ma l'utente viene creato lo stesso, nel caso si può aggiungere sempre tramite la shell 
from gianluca_app.models import Utente, Cliente
user = Utente.objects.get(username='GianlucaCliente1')
    Cliente.objects.create(
    id=user.id,
    username=user.username,
    password=user.password,
    email=user.email,
    first_name=user.first_name,
    last_name=user.last_name,
    telefono=user.telefono,
    tipo_cliente='standard'
)
