import requests

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url)
        print("🔎 Hasil:")
        print(response.text)
    except Exception as e:
        print("Gagal mengambil data cuaca:", e)

if __name__ == "__main__":
    print("=== Cek Cuaca ===")
    kota = input("Masukkan nama kota (misal: Jakarta): ")
    get_weather(kota)
