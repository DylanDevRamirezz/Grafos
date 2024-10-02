def grafo():
    return {
        'boqueron': {'la isla': 1900, 'villa mery': 900, 'terrazas boqueron': 800, 'jazmin': 2300, 'miramar': 2800, 'albania': 4500},
        'villa mery': {'boqueron': 900, 'terrazas boqueron': 180},
        'terrazas boqueron': {'boqueron': 800, 'villa mery': 180},
        'jazmin': {'boqueron': 2300, 'la union': 550, 'la isla': 290},
        'la isla': {'boqueron': 1900, 'jazmin': 290, 'la union': 850, 'miramar': 1300},
        'miramar': {'boqueron': 2800, 'albania': 2700, 'la union': 1100, 'la isla': 1300},
        'albania': {'boqueron': 4500, 'miramar': 2700},
        'la union': {'jazmin': 550, 'la isla': 850, 'miramar': 1100, 'darlo echandia': 400, 'granada': 210},
        'darlo echandia': {'la union': 400, 'granada': 300},
        'granada': {'la union': 210, 'san isidro': 850, 'darlo echandia': 300},
        'san isidro': {'granada': 850, 'colina 1': 600, 'cerros granate': 350},
        'colina 1': {'san isidro': 600, 'colina 2': 800},
        'colina 2': {'colina 1': 800},
        'cerros granate': {'san isidro': 350},
    }
