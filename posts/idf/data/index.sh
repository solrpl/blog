curl -XPOST -H 'Content-Type: application/json' 'http://localhost:8983/solr/non_distrib_idf/update?commit=true' -d '[
 {
 	"id" : 1,
 	"title" : "Solr document one"
 },
 {
 	"id" : 2,
 	"title" : "Solr document two"
 },
 {
 	"id" : 3,
 	"title" : "Solr document three"
 },
 {
 	"id" : 4,
 	"title" : "Solr document four"
 }
]'


curl -XPOST -H 'Content-Type: application/json' 'http://localhost:8983/solr/distrib_idf/update?commit=true' -d '[
 {
 	"id" : 1,
 	"title" : "Solr document one"
 },
 {
 	"id" : 2,
 	"title" : "Solr document two"
 },
 {
 	"id" : 3,
 	"title" : "Solr document three"
 },
 {
 	"id" : 4,
 	"title" : "Solr document four"
 }
]'
