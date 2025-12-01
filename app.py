from flask import Flask, request, redirect
import hashlib
import requests
import json
import dns.resolver

app = Flask(__name__)

API_KEY = "2a2ca3c783fe4e01b7454b2a587bb547.2w4JODbmZMLlwmKWCxGDdbfy12ZHmsULFlZZirAWaKGwg7DI5GDcqaGlAupQgoLJ81VPrOgxIALwbdkSYsKwrQ"
DOMAIN = "jarrabaldv.es"

def crear_url_corta(url_larga):
    # Generar código
    codigo = hashlib.md5(url_larga.encode()).hexdigest()[:8]
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. Obtener zone ID
        zonas_url = "https://api.hosting.ionos.com/dns/v1/zones"
        respuesta = requests.get(zonas_url, headers=headers)
        
        if respuesta.status_code != 200:
            return None
        
        zonas = respuesta.json()
        zone_id = None
        
        for zona in zonas:
            if zona['name'] == DOMAIN:
                zone_id = zona['id']
                break
        
        if not zone_id:
            return None
        
        # 2. Crear registro
        records_url = f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}/records"
        
        datos = {
            "name": f"{codigo}.{DOMAIN}",
            "type": "TXT",
            "content": url_larga,
            "ttl": 3600,
            "prio": 0,
            "disabled": False
        }
        
        respuesta = requests.post(records_url, headers=headers, json=[datos])
        
        if respuesta.status_code in [200, 201]:
            return codigo
        else:
            return None
            
    except Exception as e:
        return None

def obtener_url_destino(codigo):
    """Obtiene la URL real desde el DNS"""
    try:
        respuesta = dns.resolver.resolve(f"{codigo}.{DOMAIN}", 'TXT')
        for registro in respuesta:
            return str(registro).strip('"')
    except:
        return None

@app.route('/<codigo>')
def redirigir(codigo):
    """Redirige desde la URL corta a la URL real"""
    url_destino = obtener_url_destino(codigo)
    if url_destino:
        return redirect(url_destino)
    else:
        return "URL no encontrada", 404

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url_larga = request.form['url_larga']
        codigo = crear_url_corta(url_larga)
        
        if codigo:
            url_corta = f"{codigo}.{DOMAIN}"
            return f'''
            <h1>✅ URL Acortada Creada</h1>
            <p><strong>URL Original:</strong> {url_larga}</p>
            <p><strong>URL Corta:</strong> {url_corta}</p>
            <p><a href="http://{url_corta}">Probar: http://{url_corta}</a></p>
            <a href="/">Volver</a>
            '''
        else:
            return '''
            <h1>❌ Error</h1>
            <p>No se pudo crear la URL</p>
            <a href="/">Volver</a>
            '''
    
    return '''
    <h1>🔗 Acortador de URLs</h1>
    <form method="post">
        <input type="url" name="url_larga" placeholder="https://ejemplo.com" required>
        <button type="submit">Acortar URL</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)