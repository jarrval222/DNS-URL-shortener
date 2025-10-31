from flask import Flask, redirect
import requests
import json

app = Flask(__name__)

API_KEY = "2a2ca3c783fe4e01b7454b2a587bb547.2w4JODbmZMLlwmKWCxGDdbfy12ZHmsULFlZZirAWaKGwg7DI5GDcqaGlAupQgoLJ81VPrOgxIALwbdkSYsKwrQ"
DOMAIN = "jarrabaldv.es"
URL = f"https://api.hosting.ionos.com/dns/v1/zones/{DOMAIN}/records"
headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}

@app.route('/debug')
def debug():
    try:
        print("🔍 HACIENDO REQUEST A IONOS...")
        response = requests.get(URL, headers=headers)
        
        print(f"📡 STATUS CODE: {response.status_code}")
        print(f"📡 RESPONSE HEADERS: {dict(response.headers)}")
        print(f"📡 RESPONSE TEXT: {response.text}")
        
        if response.status_code == 200:
            records = response.json()
            print(f"📝 REGISTROS ENCONTRADOS: {len(records)}")
            
            for i, record in enumerate(records):
                print(f"  {i+1}. {record['name']} ({record['type']}) -> {record.get('content', 'N/A')}")
            
            return f"""
            <h1>DEBUG IONOS API</h1>
            <p>Status: {response.status_code}</p>
            <p>Registros: {len(records)}</p>
            <pre>{json.dumps(records, indent=2)}</pre>
            """
        else:
            return f"❌ ERROR {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"💥 EXCEPCIÓN: {str(e)}"

@app.route('/<codigo>')
def redirigir(codigo):
    try:
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            records = response.json()
            
            for record in records:
                if (record['type'] == 'TXT' and 
                    record['name'] == f"{codigo}.{DOMAIN}"):
                    
                    url = record['content'].strip('"')
                    return redirect(url)
            
            return f'No existe: {codigo}'
        else:
            return f'Error IONOS: {response.status_code} - {response.text}'
            
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/')
def home():
    return '''
    <h1>Acortador URLs</h1>
    <p>Usa: /yt, /gh, etc</p>
    <p><a href="/debug">VER DEBUG IONOS</a></p>
    '''
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)