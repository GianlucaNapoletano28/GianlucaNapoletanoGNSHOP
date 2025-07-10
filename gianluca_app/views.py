from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Videogioco, Recensione, Cliente, Vendita, Noleggio
from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse
from gianluca_app.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db.models import Q


def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Accesso effettuato con successo!")
            return redirect('home')
        else:
            messages.error(request, "Credenziali non valide. Riprova.")
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if Cliente.objects.filter(email=email).exists():
                messages.error(request, "Un utente con questa email esiste già. Per favore, usa un'altra email.")
            else:
                user = form.save(commit=False)
                user.is_active = True  # Assicura che l'utente sia attivo
                user.save()
                # Crea un oggetto Cliente associato all'utente
                cliente = Cliente.objects.create(
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    password=user.password,
                    tipo_cliente='standard'  # Imposta un tipo di cliente predefinito
                )
                cliente.save()
                login(request, user)
                messages.success(request, "Registrazione avvenuta con successo!")
                return redirect('home')
        else:
            messages.error(request, "Errore nella registrazione. Per favore, controlla i dati inseriti.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')


def news_view(request):
    return render(request, 'section.html', {'section_name': 'NEWS'})


def catalogo_view(request):
    giochi = Videogioco.objects.all()
    abbonato = False
    cliente = None
    if request.user.is_authenticated:
        # Cerca se l'utente è anche Cliente
        from .models import Cliente
        try:
            cliente = Cliente.objects.get(username=request.user.username)
            abbonato = cliente.id_fidelity is not None
        except Cliente.DoesNotExist:
            abbonato = False
    if request.method == 'POST':
        gioco_id = request.POST.get('gioco_id')
        tipo = request.POST.get('tipo')
        try:
            gioco = Videogioco.objects.get(pk=gioco_id)
            if tipo == 'vendita':
                if cliente:
                    Vendita.objects.create(cliente=cliente, id_gioco=gioco, totale=gioco.prezzo_vendita,
                                             tipo_pagamento='Carta', quantita=1)
                    messages.success(request, f"Hai acquistato {gioco.titolo}!")
                else:
                    messages.error(request, "Devi essere un cliente per acquistare.")
            elif tipo == 'noleggio':
                if cliente and cliente.id_fidelity:
                    Noleggio.objects.create(id_cliente=cliente, id_gioco=gioco,
                                              totale_noleggio=gioco.prezzo_noleggio,
                                              inizio_noleggio=date.today(),
                                              fine_noleggio=date.today() + timedelta(days=7))
                    messages.success(request, f"Hai noleggiato {gioco.titolo}!")
                else:
                    messages.error(request, "Devi essere abbonato per noleggiare.")
            return HttpResponseRedirect(reverse('catalogo'))
        except Videogioco.DoesNotExist:
            messages.error(request, "Gioco non trovato.")
    return render(request, 'section.html', {
        'section_name': 'CATALOGO',
        'giochi': giochi,
        'abbonato': abbonato
    })


def programma_fidelity_view(request):
    user = request.user
    fidelity = None
    abbonato = False
    fidelity_details = {}

    if user.is_authenticated:
        try:
            cliente = Cliente.objects.get(username=user.username)
            fidelity = cliente.id_fidelity
            abbonato = fidelity is not None

            if abbonato:
                fidelity_details = {
                    'tipo_abbonamento': fidelity.tipo_abbonamento,
                    'data_inizio': fidelity.data_inizio,
                    'data_fine': fidelity.data_fine,
                    'sconto_noleggio': fidelity.sconto_noleggio,
                }

            if request.method == 'POST' and not abbonato:
                from .models import ProgrammaFidelity
                # Crea un programma fidelity di default se non esiste
                programma, created = ProgrammaFidelity.objects.get_or_create(
                    tipo_abbonamento="Standard",
                    defaults={
                        'data_inizio': date.today(),
                        'data_fine': date.today() + timedelta(days=30),
                        'sconto_noleggio': 10.00
                    }
                )
                cliente.id_fidelity = programma
                cliente.save()
                messages.success(request, f"Ti sei abbonato al programma fidelity!\nData inizio: {programma.data_inizio}\nScadenza: {programma.data_fine}")
                return HttpResponseRedirect(reverse('programma_fidelity'))
        except Cliente.DoesNotExist:
            messages.error(request, "Errore: Cliente non trovato.")

    return render(request, 'section.html', {
        'section_name': 'PROGRAMMA FIDELITY',
        'abbonato': abbonato,
        'fidelity': fidelity,
        'fidelity_details': fidelity_details
    })


def contatti_view(request):
    return render(request, 'section.html', {'section_name': 'CONTATTI'})


@login_required
def recensioni_view(request):
    from .models import Recensione, Videogioco, Vendita, Cliente
    recensioni = Recensione.objects.select_related('id_cliente', 'id_gioco').all().order_by('-data')
    giochi = Videogioco.objects.all()
    giochi_acquistati = []
    giochi_acquistati_ids = []
    if request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(username=request.user.username)
            # Recupera gli ID dei giochi acquistati dal cliente
            acquisti = Vendita.objects.filter(cliente=cliente)
            giochi_acquistati_ids = [acquisto.id_gioco.id for acquisto in acquisti]
            giochi_acquistati = Videogioco.objects.filter(id__in=giochi_acquistati_ids)
        except Cliente.DoesNotExist:
            messages.error(request, "Cliente non trovato.")
    if request.method == 'POST' and request.user.is_authenticated:
        testo = request.POST.get('testo')
        valutazione = request.POST.get('valutazione')
        id_gioco = request.POST.get('id_gioco')
        if testo and valutazione and id_gioco:
            try:
                gioco = Videogioco.objects.get(pk=id_gioco)
                Recensione.objects.create(
                    id_cliente=cliente,  # Usa l'istanza di Cliente
                    id_gioco=gioco,
                    testo=testo,
                    valutazione=valutazione
                )
                messages.success(request, "Recensione inviata con successo!")
                return HttpResponseRedirect(reverse('recensioni'))
            except Videogioco.DoesNotExist:
                messages.error(request, "Videogioco non trovato.")
        else:
            messages.error(request, "Tutti i campi sono richiesti.")
    return render(request, 'section.html', {
        'section_name': 'RECENSIONI',
        'recensioni': recensioni,
        'giochi': giochi,
        'giochi_acquistati': giochi_acquistati,
        'giochi_acquistati_ids': giochi_acquistati_ids
    })


def staff_view(request):
    from .models import Dipendente, Vendita, Noleggio
    staff_access = False
    staff_user = None
    staff_error = None
    ordini_vendita = []
    ordini_noleggio = []
    ricerca = request.GET.get('ricerca', '').strip()
    if request.method == 'POST' and 'codice_staff' in request.POST:
        codice = request.POST.get('codice_staff')
        try:
            dipendente = Dipendente.objects.get(codice_staff=codice)
            staff_access = True
            staff_user = dipendente
        except Dipendente.DoesNotExist:
            staff_error = "Codice staff non valido."
    elif request.method == 'GET' and request.GET.get('accesso_staff') == '1':
        staff_access = True
        staff_user = None
    if staff_access:
        if ricerca:
            ordini_vendita = Vendita.objects.filter(
                Q(cliente__first_name__icontains=ricerca) |
                Q(cliente__last_name__icontains=ricerca) |
                Q(id_gioco__titolo__icontains=ricerca)
            )
            ordini_noleggio = Noleggio.objects.filter(
                Q(id_cliente__first_name__icontains=ricerca) |
                Q(id_cliente__last_name__icontains=ricerca) |
                Q(id_gioco__titolo__icontains=ricerca)
            )
        else:
            ordini_vendita = Vendita.objects.all()
            ordini_noleggio = Noleggio.objects.all()
    return render(request, 'section.html', {
        'section_name': 'STAFF',
        'staff_access': staff_access,
        'staff_user': staff_user,
        'staff_error': staff_error,
        'ordini_vendita': ordini_vendita,
        'ordini_noleggio': ordini_noleggio,
        'ricerca': ricerca
    })


def ordini_view(request):
    ordini_vendita = []
    ordini_noleggio = []
    if request.user.is_authenticated:
        ordini_vendita = Vendita.objects.filter(cliente=request.user)
        ordini_noleggio = Noleggio.objects.filter(id_cliente=request.user)
    return render(request, 'section.html', {
        'section_name': 'ORDINI',
        'ordini_vendita': ordini_vendita,
        'ordini_noleggio': ordini_noleggio
    })
