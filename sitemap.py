import sys, requests, re

# Report back every X URLs
REPORT_EVERY = 100
# HTTP headers to use when downloading the sitemap and URLs
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
}


try:
    sitemap_url = sys.argv[1]
except IndexError:
    print("Usage: sitemap.py https://wwww.example.com/sitemap.xml")
    sys.exit(1)


print("Getting %s" % (sitemap_url))
sitemap_text = requests.get(sitemap_url, headers=HTTP_HEADERS).text
urls = re.findall("<loc>(.*?)</loc>", sitemap_text)
number_of_urls = len(urls)
print("Checking URLs...")


url_number = 0
for url in urls:
    try:
        request = requests.get(url, headers=HTTP_HEADERS)
        if request.status_code != 200:
            print("Error HTTP %s %s" % (str(request.status_code), url))
        if url_number % REPORT_EVERY == 0:
            print("Checked %s of %s URLs" % (url_number, number_of_urls))
        url_number += 1
    except requests.exceptions.ConnectionError:
        print("Error connecting %s" % (url))

print("Checked all %s URLs" % (number_of_urls))
