import requests
import json


GAPI_KEY = '48bad6a2dc7df8164930b0ed851e6d37'
language = 'en-US'
GURL = 'https://api.themoviedb.org/3/genre/movie/list'


resultlist = []
# params = {'api_key':GAPI_KEY,'language':language}
# # data = {'page':1}
# res = requests.get(GURL,params=params)
#
#
# #가공
# items = res.json()["genres"]
#
# for i in items:
#     temp = dict()
#     temp['model'] = "movies.genre"
#     temp['pk'] = i['id']
#     fields = dict()
#     fields['name'] = i['name']
#     temp['fields'] = fields
#
#     resultlist.append(temp)

API_KEY = '48bad6a2dc7df8164930b0ed851e6d37'
language = 'ko-KR'
URL = 'https://api.themoviedb.org/3/movie/popular'


pk=1
result = []
for p in range(1,501):
    params = {'api_key':API_KEY,'language':language}
    data = {'page':p}
    res = requests.post(URL,params=params,data=data)
    # print(res.json())

    #가공
    items = res.json()["results"]

    for i in items:
        temp = dict()
        temp['model'] = "movies.movie"
        temp['pk'] = pk
        pk+=1
        temp['fields'] = i
        fields =dict()
        fields['title']=i['title']
        fields['original_title']=i['original_title']
        #fields['release_date']=i['release_date']
        fields['popularity'] = i['popularity']
        fields['vote_count'] = i['vote_count']
        fields['vote_average']=i['vote_average']
        fields['adult']=i['adult']
        fields['overview']=i['overview']
        fields['original_language']=i['original_language']
        fields['poster_path']=i['poster_path']
        fields['backdrop_path']=i['backdrop_path']
        fields['video']=i['video']
        fields['movie_id']=i['id']
        fields['genre_ids'] = i['genre_ids']

        temp['fields'] = fields
        result.append(temp)
    # print('뭐냐',result)
    # resultlist.append(result)
    # print(resultlist)
# for x in result:
#     print(x)
#파일만들기

with open('moviesfinally.json', 'w', encoding='utf-8') as make_file:
    json.dump(result, make_file, ensure_ascii=False, indent='\t')