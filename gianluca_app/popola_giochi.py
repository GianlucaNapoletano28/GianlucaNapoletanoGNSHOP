from gianluca_app.models import Videogioco


esempi = [
    {
        'titolo': 'FIFA 2025',
        'genere': 'Sport',
        'prezzo_vendita': 60.00,
        'prezzo_noleggio': 15.00,
        'disponibilita': 10
    },
    {
        'titolo': 'Call of Duty',
        'genere': 'Azione',
        'prezzo_vendita': 70.00,
        'prezzo_noleggio': 20.00,
        'disponibilita': 8
    },
    {
        'titolo': 'The Witcher 3',
        'genere': 'RPG',
        'prezzo_vendita': 50.00,
        'prezzo_noleggio': 12.00,
        'disponibilita': 7
    },
    {
        'titolo': 'Mario Kart 8',
        'genere': 'Corse',
        'prezzo_vendita': 55.00,
        'prezzo_noleggio': 13.00,
        'disponibilita': 5
    },
    {
        'titolo': 'Minecraft',
        'genere': 'Sandbox',
        'prezzo_vendita': 30.00,
        'prezzo_noleggio': 8.00,
        'disponibilita': 12
    },
]

for gioco in esempi:
    Videogioco.objects.create(**gioco)
print('Esempi di giochi inseriti!')

