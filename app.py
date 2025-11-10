#!/usr/bin/env python3
import hashlib
import requests
import json

API_KEY = "2a2ca3c783fe4e01b7454b2a587bb547.2w4JODbmZMLlwmKWCxGDdbfy12ZHmsULFlZZirAWaKGwg7DI5GDcqaGlAupQgoLJ81VPrOgxIALwbdkSYsKwrQ"
DOMAIN = "jarrabaldv.es"

def acortar_url():
    print("🔗 ACORTADOR DE URLs - IONOS API")
    print("=" * 50)
    
    url_larga = input("Introduce la URL que quieres acortar: ").strip()
    
    if not url_larga:
        print("❌ No se introdujo ninguna URL")
        return
    
    # Generar código
    codigo = hashlib.md5(url_larga.encode()).hexdigest()[:8]
    print(f"📝 Código generado: {codigo}")
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. Obtener zone ID
        print("🔍 Buscando zona DNS...")
        zonas_url = "https://api.hosting.ionos.com/dns/v1/zones"
        respuesta = requests.get(zonas_url, headers=headers)
        
        if respuesta.status_code != 200:
            print(f"❌ Error API (Zonas): {respuesta.status_code}")
            print(respuesta.text)
            return
        
        zonas = respuesta.json()
        zone_id = None
        
        for zona in zonas:
            if zona['name'] == DOMAIN:
                zone_id = zona['id']
                break
        
        if not zone_id:
            print(f"❌ No se encontró el dominio {DOMAIN}")
            return
        
        print(f"✅ Zona encontrada: {zone_id}")
        
        # 2. Crear registro con formato EXACTO de IONOS
        print("🔄 Creando registro TXT...")
        records_url = f"https://api.hosting.ionos.com/dns/v1/zones/{zone_id}/records"
        
        # FORMATO EXACTO según documentación IONOS
        datos = {
            "name": f"{codigo}.{DOMAIN}",
            "type": "TXT",
            "content": url_larga,
            "ttl": 3600,
            "prio": 0,
            "disabled": False
        }
        
        print(f"📤 Enviando: {json.dumps(datos, indent=2)}")
        
        # Probar con PUT en lugar de POST
        respuesta = requests.post(records_url, headers=headers, json=[datos])
        
        print(f"📡 Status: {respuesta.status_code}")
        print(f"📡 Respuesta: {respuesta.text}")
        
        if respuesta.status_code in [200, 201]:
            url_corta = f"{codigo}.{DOMAIN}"
            print("\n" + "=" * 50)
            print("✅ URL ACORTADA CREADA")
            print("=" * 50)
            print(f"URL Corta: {url_corta}")
            print(f"URL Larga: {url_larga}")
        else:
            print(f"❌ Error: {respuesta.status_code}")
            
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    acortar_url()