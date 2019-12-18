from datetime import datetime
from .models import Religion, UserProfile
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch()


class ElasticSearch:

    def __init__(self):
        pass

    def insert_data(self):
        bulk_data = []
        raw_data = list(UserProfile.objects.all().values('user__first_name',
                                                         'gender',
                                                         'userinfo__religion__name',
                                                         'profile_pic',
                                                         'userinfo__city',
                                                         'userinfo__state',
                                                         'userinfo__dist',
                                                         'userinfo__mother_tongue__language',
                                                         'userinfo__cast__name',
                                                         'userinfo__subcast__name',
                                                         'id', 'userinfo__height',
                                                         'is_active',
                                                         'userinfo__religion__name',
                                                         'userinfo__dob',
                                                         'userinfo__occupation',

                                                         ))
        for index, lang in enumerate(raw_data):
            # print(index)
            print(lang)
            temp_dict = {}
            temp_dict['_index'] = 'user_profile'
            temp_dict['_type'] = 'lang'
            temp_dict['id'] = index + 1
            # temp_dict['_source'] = {}
            temp_dict['_source'] = lang
            bulk_data.append(temp_dict)

        helpers.bulk(es, bulk_data)
        return bulk_data

    def query_data(self, gender, mother_tongue, religion, cast, sub_cast):

        # print("=============>>>>>>>>>>>>>>>>>")
        # print(gender)
        # print(mother_tongue)
        # print(religion)
        # print(cast)
        # print(sub_cast)
        # # print(dob)

        query_string = {
            "from": 0, "size": 10,
            "query": {
                "bool": {
                    "must": {
                        "term": {"is_active": True}
                    },
                    "filter": {
                        "term": {
                            "gender": gender
                        }
                    },
                    "should": [
                        {"term": {"userinfo__religion__name": religion}},
                        {"term": {"userinfo__cast__name": cast}},
                        {"term": {"userinfo__subcast__name": sub_cast}},
                        {"term": {"userinfo__mother_tongue__language": mother_tongue}},
                    ],
                }
            }
        }

        res = es.search(index="user_profile", body=query_string)
        print("Got %d Hits:" % res['hits']['total']['value'])
        dict = []
        for hit in res['hits']['hits']:
            dict.append(hit['_source'])

        return dict


els_lan = ElasticSearch()
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
