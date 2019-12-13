from datetime import datetime
from .models import Religion
from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch()

# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# bulk_data = MotherTongue.objects.all()
# helpers.bulk(es, bulk_data)
#
# res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
# print(res['result'])
#
# res = es.get(index="test-index", doc_type='tweet', id=1)
# print(res['_source'])
#
# es.indices.refresh(index="test-index")
#
# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])



class ElasticSearch:

    def __init__(self):
        self.insert_data()

    def insert_data(self):
        bulk_data = []
        raw_data = list(Religion.objects.all().values('name'))
        for index, lang in enumerate(raw_data):
            print(index)
            print(lang)
            temp_dict = {}
            temp_dict['_index'] = 'religion'
            temp_dict['_type'] = 'lang'
            temp_dict['id'] = index + 1
            temp_dict['_source'] = {}
            temp_dict['_source']['data'] = lang
            bulk_data.append(temp_dict)

        helpers.bulk(es, bulk_data)
        return bulk_data



els_lan = ElasticSearch()
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

from elasticsearch_dsl import Document, Date, Keyword, Text

# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from .models import Car, Education
#
# @registry.register_document
# class CarDocument(Document):
#     class Index:
#         name = 'cars'
#         settings = {'number_of_shards': 1,
#                     'number_of_replicas': 0}
#
#     class Django:
#         model = Car
#         fields = [
#             'name',
#             'color',els
#         ]
#
# @registry.register_document
# class EducationDocument(Document):
#     class Index:
#         name = 'educations'
#         settings = {'number_of_shards': 1,
#                     'number_of_replicas': 0}
#
#     class Django:
#         model = Education
#         fields = [
#             'field',
#         ]

#
# from django_elasticsearch_dsl import Index
# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from .models import Religion
#
#
# @registry.register_document
# class CarDocument(Document):
#     class Index:
#         name = 'religions'
#         settings = {'number_of_shards': 1,
#                     'number_of_replicas': 0}
#
#     class Django:
#         model = Religion  # The model associated with this Document
#
#         # The fields of the model you want to be indexed in Elasticsearch
#         fields = [
#             'name',
#         ]