import pytest 
import requests

def test_prediction_status():

        response = requests.get('http://128.2.205.5:8082/recommend/11880')
        print(response.status_code == 200)

        assert response.status_code == 200

def test_prediction():
        old_list1 = requests.get('http://128.2.205.5:8082/recommend/11880')
        old_list2 = requests.get('http://128.2.205.5:8082/recommend/11880')
        print(old_list1.content == old_list2.content)

        assert old_list1.content == old_list2.content

        new_list1 = requests.get('http://128.2.205.5:8082/recommend/12345')
        new_list2 = requests.get('http://128.2.205.5:8082/recommend/12345')
        print(new_list1.content != new_list2.content)

        assert new_list1.content != new_list2.content
