import csv
from karpet import Karpet
from tqdm import tqdm
import aiohttp

k = Karpet()

# Path to a file which contains a list of cryptocurrencies
cryptolist = "path/cryptotitles.txt"

# Read a list from file above
with open(cryptolist, "r") as file:
    cryptocurrencies = [line.strip() for line in file.readlines()]

# File name to save the results
filename = "news.csv"

# Column headers in the save file
headers = ["cryptocurrency", "url", "title", "description", "date", "image"]

# List to store all articles
all_news = []

# Retrive news
with tqdm(total=len(cryptocurrencies), desc="data retrieval") as pbar:
    for cryptocurrency in cryptocurrencies:
        try:
            news = k.fetch_news(cryptocurrency)
            for article in news:
                article["cryptocurrency"] = cryptocurrency
            all_news.extend(news)
        except (aiohttp.client_exceptions.ClientConnectorCertificateError, aiohttp.client_exceptions.ClientConnectorError) as e:
            print("\n" + f"Ignoring error: {type(e).__name__}")
            continue

        pbar.update(1)
    pbar.update(0)

# Save results to CSV file
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for article in all_news:
        writer.writerow(article)

print("Results saved to CSV file: " + filename)