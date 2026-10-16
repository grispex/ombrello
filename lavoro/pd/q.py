import urllib.request, urllib.parse, ssl, sys, json
q = sys.argv[1]
url = "https://dati.camera.it/sparql?" + urllib.parse.urlencode({"query": q, "format": "application/sparql-results+json"})
r = urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/sparql-results+json"}), timeout=60)
print(r.read().decode()[:6000])
