import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv


pages = ["/index.html", "/customers.html", "/artists.html", "/products.html"]
ips = ["192.168.1.1", "192.168.1.2", "10.0.0.1", "172.16.0.1"]
browsers = ["Chrome", "Firefox", "Safari", "Edge"]


access_log = []
current_time = datetime.now()
for _ in range(50):  
    page = random.choice(pages)
    ip = random.choice(ips)
    time = current_time - timedelta(minutes=random.randint(0, 120))
    browser = random.choice(browsers)
    access_log.append((page, ip, time, browser))


error_types = ["404 Not Found", "500 Internal Server Error", "403 Forbidden"]
error_log = []
for _ in range(10):  
    ip = random.choice(ips)
    time = current_time - timedelta(minutes=random.randint(0, 120))
    error = random.choice(error_types)
    error_log.append((ip, time, error))


page_hits = {page: 0 for page in pages}
ip_hits = {ip: 0 for ip in ips}
browser_hits = {b: 0 for b in browsers}

for page, ip, time, browser in access_log:
    page_hits[page] += 1
    ip_hits[ip] += 1
    browser_hits[browser] += 1

error_count = {}
for ip, time, err in error_log:
    error_count[err] = error_count.get(err, 0) + 1


with open("access_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Page", "IP", "Time", "Browser"])
    writer.writerows(access_log)

with open("error_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["IP", "Time", "Error"])
    writer.writerows(error_log)


plt.figure(figsize=(10, 5))
for page in pages:
    times = [time for p, ip, time, b in access_log if p == page]
    plt.scatter(times, [page]*len(times), label=page, marker="x", color="red")
plt.xlabel("Time")
plt.ylabel("Page")
plt.title("Page Access Timeline")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("access_timeline.png")
plt.close()

plt.figure(figsize=(10, 3))
for err in error_types:
    times = [time for ip, time, e in error_log if e == err]
    plt.scatter(times, [err]*len(times), label=err, marker="x", color="red")
plt.xlabel("Time")
plt.ylabel("Error Type")
plt.title("Error Timeline")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("error_timeline.png")
plt.close()



print("\n--- Page Hits ---")
for page, count in page_hits.items():
    print(f"{page}: {count}")

print("\n--- Hits by IP ---")
for ip, count in ip_hits.items():
    print(f"{ip}: {count}")

print("\n--- Hits by Browser ---")
for b, count in browser_hits.items():
    print(f"{b}: {count}")

print("\n--- Errors ---")
for err, count in error_count.items():
    print(f"{err}: {count}")
