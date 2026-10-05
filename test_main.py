from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_flux():
    predict = client.post("/Predict", params={"SK_ID_CURR": "100002"})
    assert predict.status_code == 200
    predict = predict.json()
    credit_accept = predict[1]
    credit_decline = predict[2]
    assert credit_accept + credit_decline == 100

test_flux()





