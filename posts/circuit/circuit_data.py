#!/usr/bin/env python3
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
import base64
import json

solr_host = "localhost:8983"
solr_collection = "circuit"
num_documents = 1000000
docs_per_batch = 1000

print("")
print("--- Configuration ------------------")
print("--- Solr host:                    %s" % solr_host)
print("--- Collection name:              %s" % solr_collection)
print("--- Number of documents:          %s" % num_documents)
print("")

update_url = 'http://{}/solr/{}/update'.format(solr_host, solr_collection)
headers = { "Content-Type": "application/json" }

docs = []
docNum = 0
batchNum = 0

while docNum < num_documents:
  docNum += 1
  text = f"""Lorem{docNum} ipsum{docNum} dolor{docNum} sit{docNum} amet{docNum},
  consectetur{docNum} adipiscing{docNum} elit{docNum}, sed{docNum} do{docNum} eiusmod{docNum} tempor{docNum} incididunt{docNum}
  ut{docNum} labore{docNum} et{docNum} dolore{docNum} magna{docNum} aliqua{docNum}. 
  Ut{docNum} enim{docNum} ad{docNum} minim{docNum} veniam{docNum}, quis{docNum} nostrud{docNum} exercitation{docNum}
  ullamco{docNum} laboris{docNum} nisi{docNum} ut{docNum} aliquip{docNum} ex{docNum} ea{docNum} commodo{docNum} 
  consequat{docNum}. Duis{docNum} aute{docNum} irure{docNum} dolor{docNum} in{docNum} reprehenderit{docNum} in{docNum} voluptate{docNum} 
  velit{docNum} esse{docNum} cillum{docNum} dolore{docNum} eu{docNum} fugiat{docNum} 
  nulla{docNum} pariatur{docNum}. Excepteur{docNum} sint{docNum} occaecat{docNum} cupidatat{docNum} non{docNum} proident{docNum},
  sunt{docNum} in{docNum} culpa{docNum} qui{docNum} officia{docNum} deserunt{docNum} 
  mollit{docNum} anim{docNum} id{docNum} est{docNum} laborum{docNum}.
  Lorem{docNum} ipsum{docNum} dolor{docNum} sit{docNum} amet{docNum},
  consectetur{docNum} adipiscing{docNum} elit{docNum}, sed{docNum} do{docNum} eiusmod{docNum} tempor{docNum} incididunt{docNum}
  ut{docNum} labore{docNum} et{docNum} dolore{docNum} magna{docNum} aliqua{docNum}. 
  Ut{docNum} enim{docNum} ad{docNum} minim{docNum} veniam{docNum}, quis{docNum} nostrud{docNum} exercitation{docNum}
  ullamco{docNum} laboris{docNum} nisi{docNum} ut{docNum} aliquip{docNum} ex{docNum} ea{docNum} commodo{docNum} 
  consequat{docNum}. Duis{docNum} aute{docNum} irure{docNum} dolor{docNum} in{docNum} reprehenderit{docNum} in{docNum} voluptate{docNum} 
  velit{docNum} esse{docNum} cillum{docNum} dolore{docNum} eu{docNum} fugiat{docNum} 
  nulla{docNum} pariatur{docNum}. Excepteur{docNum} sint{docNum} occaecat{docNum} cupidatat{docNum} non{docNum} proident{docNum},
  sunt{docNum} in{docNum} culpa{docNum} qui{docNum} officia{docNum} deserunt{docNum} 
  mollit{docNum} anim{docNum} id{docNum} est{docNum} laborum{docNum}.
  Lorem{docNum} ipsum{docNum} dolor{docNum} sit{docNum} amet{docNum},
  consectetur{docNum} adipiscing{docNum} elit{docNum}, sed{docNum} do{docNum} eiusmod{docNum} tempor{docNum} incididunt{docNum}
  ut{docNum} labore{docNum} et{docNum} dolore{docNum} magna{docNum} aliqua{docNum}. 
  Ut{docNum} enim{docNum} ad{docNum} minim{docNum} veniam{docNum}, quis{docNum} nostrud{docNum} exercitation{docNum}
  ullamco{docNum} laboris{docNum} nisi{docNum} ut{docNum} aliquip{docNum} ex{docNum} ea{docNum} commodo{docNum} 
  consequat{docNum}. Duis{docNum} aute{docNum} irure{docNum} dolor{docNum} in{docNum} reprehenderit{docNum} in{docNum} voluptate{docNum} 
  velit{docNum} esse{docNum} cillum{docNum} dolore{docNum} eu{docNum} fugiat{docNum} 
  nulla{docNum} pariatur{docNum}. Excepteur{docNum} sint{docNum} occaecat{docNum} cupidatat{docNum} non{docNum} proident{docNum},
  sunt{docNum} in{docNum} culpa{docNum} qui{docNum} officia{docNum} deserunt{docNum} 
  mollit{docNum} anim{docNum} id{docNum} est{docNum} laborum{docNum}."""

  docs.append({"id": docNum, "text": text}) 

  if docNum % docs_per_batch == 0:
    batchNum += 1
    print("Sending batch")
    requests.post(update_url, json=docs, headers=headers)
    docs = []

print("Sending last batch")
requests.post(update_url, json=docs, headers=headers)
docs = []

print("Committing changes")
commit_url = 'http://{}/solr/{}/update?commit=true'
connection = urlopen(commit_url.format(solr_host, solr_collection))