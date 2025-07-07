import requests

def es_feriado_irrenunciable(fecha):
    url = "https://api.boostr.cl/holidays.json"
    try:
        response = requests.get(url)
        feriados = response.json()
        # print(feriados)  # Descomenta para depurar
        fecha_str = fecha.strftime("%Y-%m-%d")
        for f in feriados:
            if isinstance(f, dict):
                if f.get('date') == fecha_str and f.get('irrenunciable', False):
                    return True
        return False
    except Exception as e:
        print(f"Error consultando feriados: {e}")
        return False