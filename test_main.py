from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_flux():
    predict = client.post("/Predict")
    assert predict.status_code == 422

    predict = client.post("/Predict", params={"SK_ID_CURR": "abc"})
    assert predict.status_code in (404, 422)

    predict = client.post("/Predict", params={"SK_ID_CURR": "100002"})
    assert predict.status_code == 200
    
    predict = predict.json()
    credit_accept = predict[1]
    credit_decline = predict[2]
    
    features = predict[3]
    features = features[0]

    assert features["DAYS_BIRTH"]/(-365) >= 18
    assert features["AMT_INCOME_TOTAL"]/12 > 0

    assert credit_accept + credit_decline == 100
