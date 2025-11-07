import requests

BASE_URL = "http://localhost:8000/api/v1"

# Test /api/seed (admin-only)
def test_seed():
    # Replace with valid admin token if needed
    headers = {"Authorization": "Bearer test_admin_token"}
    resp = requests.post(f"{BASE_URL}/seed", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "seeded"

# Test /api/opportunities
def test_opportunities():
    resp = requests.get(f"{BASE_URL}/opportunities")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

# Test /api/ai/test (admin-only)
def test_ai_test():
    headers = {"Authorization": "Bearer test_admin_token"}
    payload = {"raw_text": "Test opportunity for ASI1."}
    resp = requests.post(f"{BASE_URL}/ai/test", json=payload, headers=headers)
    assert resp.status_code == 200
    assert "result" in resp.json()

# Test /api/ai/recommend (admin-only)
def test_ai_recommend():
    headers = {"Authorization": "Bearer test_admin_token"}
    payload = {"query": "machine learning internship"}
    resp = requests.post(f"{BASE_URL}/ai/recommend", json=payload, headers=headers)
    assert resp.status_code == 200
    assert "recommendations" in resp.json()

if __name__ == "__main__":
    test_seed()
    test_opportunities()
    test_ai_test()
    test_ai_recommend()
    print("All endpoint tests passed.")
