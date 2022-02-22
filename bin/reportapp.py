import requests


def main():
    while choice := input("[R]eport weather or [s]ee reports? "):
        if choice.lower().strip() == 'r':
            report_event()
        elif choice.lower().strip() == 's':
            see_events()
        else:
            print(f"Don't know what to do with {choice}.")

        choice = input("[R]eport weather or [s]ee reports? ")


def report_event():
    desc = input("What is happening now? ")
    lat = input("What latitude? ")
    lon = input("What longitude? ")

    data = {
        "description": desc,
        "location": {
            "lat": lat,
            "lon": lon
        }
    }
    print(data)
    url = "http://127.0.0.1:8000/api/reports"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    resp = requests.post(url, json=data, headers=headers)
    resp.raise_for_status()

    result = resp.json()
    print(f"Reported new event: {result.get('id')}")


def see_events():
    url = "http://127.0.0.1:8000/api/reports"
    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()
    for r in data:
        print(f"{r.get('location').get('lat')}/{r.get('location').get('lon')} has {r.get('description')}")


if __name__ == '__main__':
    main()