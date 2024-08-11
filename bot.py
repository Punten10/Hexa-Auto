import requests
import time

def authenticate(user_id, username):
    auth_url = "https://ago-api.hexacore.io/api/app-auth"

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

    auth_payload = {
        "user_id": user_id,
        "username": username
    }

    auth_response = requests.post(auth_url, headers=auth_headers, json=auth_payload)

    auth_token = auth_response.json().get("token")

    if not auth_token:
        raise ValueError("Authorization token not found in the response.")

    return auth_token

def complete_mining(auth_token, taps):
    click_url = "https://ago-api.hexacore.io/api/mining-complete"

    click_headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }

    click_payload = {
        "taps": taps
    }

    click_response = requests.post(click_url, headers=click_headers, json=click_payload)

    click_status = click_response.json().get("success")

    return click_status

def get_balance(auth_token, user_id):
    balance_url = f"https://ago-api.hexacore.io/api/balance/{user_id}"

    balance_headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }

    balance_response = requests.get(balance_url, headers=balance_headers)

    balance = balance_response.json().get("balance")

    return balance

def get_available_taps(auth_token):
    taps_url = "https://ago-api.hexacore.io/api/available-taps"

    taps_headers = {
        "Authorization": auth_token
    }

    taps_response = requests.get(taps_url, headers=taps_headers)

    available_taps = taps_response.json().get("available_taps")

    return available_taps

def get_reward_available(auth_token, user_id):
    reward_url = f"https://ago-api.hexacore.io/api/reward-available/{user_id}"

    reward_headers = {
        "Authorization": auth_token
    }

    reward_response = requests.get(reward_url, headers=reward_headers)

    reward_available = reward_response.json()

    return reward_available

def get_daily_reward(auth_token, user_id):
    daily_reward_url = "https://ago-api.hexacore.io/api/daily-reward"

    daily_reward_headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }

    daily_reward_payload = {
        "user_id": user_id
    }

    daily_reward_response = requests.post(daily_reward_url, headers=daily_reward_headers, json=daily_reward_payload)

    daily_reward = daily_reward_response.json()

    return daily_reward

def main():
    print("=========HEXA BOT=============")
    taps = int(input("Taps: "))
    sleep_time = int(input("Sleep time (in seconds): "))
    print("===============================")

    with open("data.txt", "r") as file:
        user_data = [line.strip().split(":") for line in file.readlines()]

    while True:
        for user_id, username in user_data:
            user_id = int(user_id)
            try:
                auth_token = authenticate(user_id, username)
                click_status = complete_mining(auth_token, taps)
                balance = get_balance(auth_token, user_id)
                available_taps = get_available_taps(auth_token)
                reward_available = get_reward_available(auth_token, user_id)
                daily_reward = get_daily_reward(auth_token, user_id)

                print("=========HEXA BOT=============")
                print(f"username: \"{username}\"")
                print(f"Click: {click_status}")
                print(f"Balance Response: {balance}")
                print(f"available_taps: {available_taps}")
                print(f"availabl_Reward: {reward_available}")
                print(f"daily-reward: {daily_reward}")
                print("===============================")
            except Exception as e:
                print(f"Error for user {username} (ID: {user_id}): {e}")

        print(f"Next run in {sleep_time} seconds...")
        for remaining in range(sleep_time, 0, -1):
            print(f"\rCountdown: {remaining} seconds", end="")
            time.sleep(1)

if __name__ == "__main__":
    main()
