from algo import normalize_time, fetch

def main():
    while True:
        language = input("Choose language for response: english/ukrainian\n")
        c = 1
        users_data = fetch(c)

        for user in users_data['data']:
            username = user["nickname"]
            status = normalize_time(user['lastSeenDate'], language)
            print(f"{username} {status}")

        c += 2

if __name__ == "__main__":
    main()
