import requests

def es_feriado_irrenunciable(fecha):
    url = "https://api.boostr.cl/holidays.json"
    try:
        response = requests.get(url)
        feriados = response.json()
        for f in feriados:
            if f['date'] == fecha.strftime("%Y-%m-%d") and f['irrenunciable']:
                return True
        return False
    except:
        return False


