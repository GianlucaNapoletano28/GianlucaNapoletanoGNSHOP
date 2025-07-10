# gianluca_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Utente(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Cliente(Utente):
    TIPO_CLIENTE_CHOICES = [
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    tipo_cliente = models.CharField(
        max_length=20,
        choices=TIPO_CLIENTE_CHOICES,
        default='standard'
    )
    id_fidelity = models.ForeignKey(
        'ProgrammaFidelity',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='clienti'
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return f"Cliente: {super().__str__()} - Tipo: {self.tipo_cliente}"

class Dipendente(Utente):
    ruolo = models.CharField(max_length=100)
    codice_staff = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Dipendente"
        verbose_name_plural = "Dipendenti"

    def __str__(self):
        return f"Dipendente: {super().__str__()} - Ruolo: {self.ruolo}"

class ProgrammaFidelity(models.Model):
    tipo_abbonamento = models.CharField(max_length=100)
    data_inizio = models.DateField()
    data_fine = models.DateField()
    sconto_noleggio = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Programma Fidelity"
        verbose_name_plural = "Programmi Fidelity"

    def __str__(self):
        return self.tipo_abbonamento

class Videogioco(models.Model):
    titolo = models.CharField(max_length=200)
    genere = models.CharField(max_length=100)
    prezzo_vendita = models.DecimalField(max_digits=6, decimal_places=2)
    prezzo_noleggio = models.DecimalField(max_digits=6, decimal_places=2)
    disponibilita = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Videogioco"
        verbose_name_plural = "Videogiochi"

    def __str__(self):
        return self.titolo

class Vendita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vendite', default=1)
    id_gioco = models.ForeignKey(Videogioco, on_delete=models.CASCADE)
    totale = models.DecimalField(max_digits=7, decimal_places=2)
    data_acquisto = models.DateField(auto_now_add=True)
    tipo_pagamento = models.CharField(max_length=100)
    quantita = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Vendita"
        verbose_name_plural = "Vendite"

    def __str__(self):
        return f"Vendita #{self.pk} - {self.data_acquisto}"

class DettaglioVendita(models.Model):
    id_vendita = models.ForeignKey(Vendita, on_delete=models.CASCADE, related_name='dettagli')
    id_gioco = models.ForeignKey(Videogioco, on_delete=models.CASCADE)
    quantita = models.PositiveIntegerField()
    prezzo_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    sconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Dettaglio Vendita"
        verbose_name_plural = "Dettagli Vendita"

    def __str__(self):
        return f"Dettaglio Vendita #{self.id_vendita.pk} - {self.id_gioco.titolo}"

class Noleggio(models.Model):
    totale_noleggio = models.DecimalField(max_digits=7, decimal_places=2)
    inizio_noleggio = models.DateField()
    fine_noleggio = models.DateField()
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='noleggi')
    id_dipendente = models.ForeignKey(Dipendente, on_delete=models.CASCADE, related_name='noleggi', null=True, blank=True)
    id_gioco = models.ForeignKey(Videogioco, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Noleggio"
        verbose_name_plural = "Noleggi"

    def __str__(self):
        return f"Noleggio #{self.pk} - {self.id_gioco.titolo} ({self.id_cliente.username})"

class Recensione(models.Model):
    testo = models.TextField()
    valutazione = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],  # Valori da 1 a 5
        default=5
    )
    data = models.DateField(auto_now_add=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='recensioni')
    id_gioco = models.ForeignKey(Videogioco, on_delete=models.CASCADE, related_name='recensioni')

    class Meta:
        verbose_name = "Recensione"
        verbose_name_plural = "Recensioni"

    def __str__(self):
        return f"Recensione di {self.id_cliente.username} su {self.id_gioco.titolo}"