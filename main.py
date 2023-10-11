from algo import normalize_time_human_implementation, fetch

def main():
    #print(check_dates_correspond("2025-27-09-20:00", "2025-14-09-20:00"))
    language = input("Choose language for response: english/ukrainian\n")
    #print(normalize_time_human_implementation("2023-10-11T20:29:33.8772757+00:00", language, "2023-11-10-20:00"))
    c = 0
    users_data = fetch(c)
    q = int(users_data['total'])
    while q > 0:
        #print(c)
        #print("\n")
        for user in users_data['data']:
            username = user["nickname"]
            status = normalize_time_human_implementation(user['lastSeenDate'], language)
            print(f"{username} {status}")
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

if __name__ == "__main__":
    main()
