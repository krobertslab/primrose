#Close the index so that modifications can be made
curl -X POST "localhost:9200/trials/_close"


#Add the analyzer to the index-- probs will have to do again for abstracts once complete
#curl -XPUT 'localhost:9200/trials/_settings' -H 'Content-Type: application/json' -d '{
#     "analysis":{
#         "analyzer":{
#             "second":{
#                 "type":"custom",
#                 "tokenizer":"standard",
#                "filter":[
#                     "standard",
#                     "lowercase",
#                     "filter_stemmer",
#                     "filter_shingle"
#                 ]
#                 }
#             },
#            "filter":{
#                 "filter_shingle":{
#                     "type":"shingle",
#                     "max_shingle_size":5,
#                     "min_shingle_size":2,
#                     "output_unigrams":false
#                 },
#                 "filter_stemmer":{
#                     "type":"porter_stem",
#                     "langauge":"English"
#                 }
#             }
#         }
#     
#    
#   
#    }'




# Update both mappings
curl -X PUT "localhost:9200/trials/_mapping" -H 'Content-Type: application/json' -d'
{
  "properties": {
    "brief_title": {
        "properties":{
            "type": "text",
            "analyzer": "second"
        }
     
    }
  }
}
'



#Reopen the index so that we can use it normally
curl -X POST "localhost:9200/trials/_open" 