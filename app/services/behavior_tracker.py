import datetime

def log_user_login(user_id, ip, user_agent):
    with open("login_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"[{timestamp}] User {user_id} — IP: {ip} — UA: {user_agent}\n")
