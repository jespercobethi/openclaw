import json, urllib.request, urllib.parse

city = urllib.parse.quote("湘潭")
url = f"https://wttr.in/{city}?format=j1"
req = urllib.request.Request(url, headers={"User-Agent": "curl/7.64.1"})
data = json.loads(urllib.request.urlopen(req).read())

for day in data["weather"]:
    if day["date"] == "2026-05-14":
        print(f"日期: {day['date']}")
        print(f"最高: {day['maxtempC']}C / 最低: {day['mintempC']}C")
        print("-" * 50)
        for h in day["hourly"]:
            t = int(h["time"]) // 100
            desc = h.get("lang_xx", [{}])[0].get("value", h["weatherDesc"][0]["value"])
            print(f"{t:02d}:00 | {h['tempC']}C | {desc} | rain {h['chanceofrain']}% | humid {h['humidity']}%")
