import requests

def test_all_berry_stats():
    response = requests.get("http://localhost:8000/allBerryStats")
    assert response.status_code == 200
    assert response.headers['content-type'] == "application/json"
    response = response.json()
    assert type(response) == dict
    response = response["Response"]
    assert type(response["berries_names"]) == list
    assert type(response["min_growth_time"]) == int
    assert type(response["median_growth_time"]) == float
    assert type(response["max_growth_time"]) == int
    assert type(response["variance_growth_time"]) == float
    assert type(response["mean_growth_time"]) == float
    assert type(response["frequency_growth_time"]) == dict
