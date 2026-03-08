import requests
import sys

def test_connection(url):
    print(f"Probando conexión a: {url}")
    try:
        # Los servidores SSE de MCP responden a un GET inicial
        # Usamos stream=True porque SSE es una conexión persistente
        response = requests.get(url, timeout=5, stream=True)
        print(f"✅ Éxito! Código de estado: {response.status_code}")
        print("Cerrando conexión de prueba...")
        return True
    except requests.exceptions.Timeout:
        print("❌ Error: Tiempo de espera agotado (Timeout). El servidor no respondió.")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Conexión rechazada. ¿Está el servidor AntV corriendo en ese puerto?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    return False

if __name__ == "__main__":
    # Probamos las dos variantes más comunes
    urls = ["http://127.0.0.1:8081/sse", "http://127.0.0.1:8081"]
    
    any_success = False
    for url in urls:
        if test_connection(url):
            any_success = True
            print(f"\n👉 URL CORRECTA DETECTADA: {url}")
            print("Asegúrate de que esta URL esté en tu archivo .env como CHART_TOOLBOX_URL")
            break
        print("-" * 30)
    
    if not any_success:
        print("\n🚨 Ninguna URL funcionó. Revisa que el comando npx esté corriendo y no haya un firewall bloqueando el puerto 8081.")
