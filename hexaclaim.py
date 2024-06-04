import requests

# URL untuk otentikasi
auth_url = "https://hexacore-tg-api.onrender.com/api/app-auth"

# URL tambahan yang diperlukan
mission_url = "https://twitter.com/intent/tweet?text=Join%20me%20at%20Hexacore%20Gaming%20Universe%20and%20earn%20rewards!%20link:%20{REFERRAL_LINK}"
url_cek_mission = "https://hexacore-tg-api.onrender.com/api/mission-complete"
passive_income_url = "https://hexacore-tg-api.onrender.com/api/total-passive"
upgrade_level_url = "https://hexacore-tg-api.onrender.com/api/upgrade-level"
check_level_url = "https://hexacore-tg-api.onrender.com/api/level"
buy_tap_url = "https://hexacore-tg-api.onrender.com/api/buy-tap-passes"

# Header umum untuk request
common_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://ago-wallet.hexacore.io",
    "Priority": "u=1, i",
    "Referer": "https://ago-wallet.hexacore.io/"
}

# Header khusus untuk otentikasi
auth_headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://ago-wallet.hexacore.io",
    "Referer": "https://ago-wallet.hexacore.io/",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}

# Fungsi untuk membaca data dari file dan mengembalikan daftar pasangan user_id dan username
def read_user_data(filename):
    user_data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                user_id = parts[0].strip()
                username = parts[1].strip()
                user_data.append((user_id, username))
    return user_data

# Fungsi untuk mencetak hasil dengan format yang diminta
def print_results(username, mission_results=None, upgrade_level_result=None, check_level_result=None, passive_income_result=None, buy_tap_result=None):
    print("=========HEXA BOT=============")
    print(f"Username: \"{username}\"")
    if mission_results:
        for mission_id, response in mission_results.items():
            print(f"Mission {mission_id} : {response}")
    if upgrade_level_result:
        print(f"Naik level : {upgrade_level_result}")
        if not upgrade_level_result.get("success", True):
            print("Balance tidak cukup")
    if check_level_result:
        print(f"Level : {check_level_result}")
    if passive_income_result:
        total_passive_income = passive_income_result.get("total_passive_income", "N/A")
        print(f"Pasive income : {total_passive_income}")
    if buy_tap_result:
        print(f"Buy tap : {buy_tap_result}")
    print("=" * 80)

# Membaca user_id dan username dari file data.txt
user_data = read_user_data('data.txt')

# Daftar mission_id yang ada
mission_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Daftar REFERRAL_LINK yang ada
referral_links = [
    "https://twitter.com/settings/profile",
    "https://twitter.com/Hexacore_UGC",
    "https://twitter.com/pocketspacegg",
    "https://twitter.com/aleks_blanche",
    "https://twitter.com/AlexanderKorch7",
    "https://twitter.com/settings/profile",
    "https://discord.com/invite/2Z8XurKufH"
]

# Menampilkan opsi kepada pengguna
print("=========HEXA BOT=============")
print("Opsi:")
print("1. Claim Mission")
print("2. Upgrade Level")
print("3. Cek Level")
print("4. Cek Pasive Income")
print("5. Buy Tap 1 Day ( 270 AGO )")
print("6. Buy Tap 3 Day ( 1125 AGO )")
print("7. Buy Tap 7 Day ( 1800 AGO )")

# Membaca pilihan pengguna
choice = input("Masukkan pilihan Anda: ")

# Mengirimkan request POST untuk setiap pasangan user_id dan username
for user_id, username in user_data:
    auth_payload = {
        "user_id": user_id,
        "username": username
    }
    
    response = requests.post(auth_url, headers=auth_headers, json=auth_payload)
    
    if response.status_code == 200:
        auth_response = response.json()
        token = auth_response.get("token", "")  # Asumsi token ada di dalam respons otentikasi
        
        if token:
            common_headers["Authorization"] = token  # Menggunakan token langsung tanpa "Bearer"
            
            print("-" * 80)  # Untuk memisahkan output tiap request
            
            if choice == "1":
                mission_results = {}
                # Menjalankan semua referral links sebelum cek mission
                for referral_link in referral_links:
                    full_mission_url = mission_url.replace("{REFERRAL_LINK}", referral_link)
                    # Simulasikan request ke URL mission, di sini hanya untuk ilustrasi karena tidak ada request POST sebenarnya ke URL ini
                    print(f"Visiting referral link: {full_mission_url}")

                # Mission complete request
                for mission_id in mission_ids:
                    mission_payload = {"missionId": mission_id}
                    mission_response = requests.post(url_cek_mission, headers=common_headers, json=mission_payload)
                    mission_results[mission_id] = mission_response.json()
                print_results(username, mission_results=mission_results)
                    
            elif choice == "2":
                # Upgrade level request
                upgrade_level_response = requests.post(upgrade_level_url, headers=common_headers, json={})
                print_results(username, upgrade_level_result=upgrade_level_response.json())
                
            elif choice == "3":
                # Check level request
                check_level_response = requests.get(check_level_url, headers=common_headers)
                print_results(username, check_level_result=check_level_response.json())
                
            elif choice == "4":
                # Passive income request
                passive_income_response = requests.get(passive_income_url, headers=common_headers)
                print_results(username, passive_income_result=passive_income_response.json())
                
            elif choice == "5":
                # Buy TAP 1 Day request
                buy_tap_payload = {"name": "1_day"}
                buy_tap_response = requests.post(buy_tap_url, headers=common_headers, json=buy_tap_payload)
                print_results(username, buy_tap_result=buy_tap_response.text)

            elif choice == "6":
                # Buy TAP 1 Day request
                buy_tap_payload = {"name": "3_days"}
                buy_tap_response = requests.post(buy_tap_url, headers=common_headers, json=buy_tap_payload)
                print_results(username, buy_tap_result=buy_tap_response.text)

            elif choice == "7":
                # Buy TAP 1 Day request
                buy_tap_payload = {"name": "7_days"}
                buy_tap_response = requests.post(buy_tap_url, headers=common_headers, json=buy_tap_payload)
                print_results(username, buy_tap_result=buy_tap_response.text)        
                
            else:
                print("Pilihan tidak valid.")
                break
        else:
            print(f"Failed to get token for user_id={user_id}, username={username}")
    else:
        print(f"Auth failed for user_id={user_id}, username={username}: {response.text}")
    print("-" * 80)
