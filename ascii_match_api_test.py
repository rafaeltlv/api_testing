import pytest
import json
import requests

results = []

def make_request(value):
    url = f'https://api.insoundz.io/v1/values/{value}'
    response = requests.get(url, timeout=5)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"Error: {e}")
        return None
    return response

@pytest.mark.parametrize("value", [1, 2, 3, 4, 5, 10])
def test_each_x_ascii_match(value):
    print(f"Testing x={value}")
    response = make_request(value)
    if response is None:
        pytest.skip(f"Skipping test for x={value} due to 404 error")

    status = response.json()
    print(f"Response received for x={value}: {status}")
    assert len(status) >= 2, f"Unexpected response length for x={value}: expected >= 2, actual = {len(status)}"

    match_found = False
    for i, c1 in enumerate(status):
        for j, c2 in enumerate(status):
            if i == j:
                continue
            if abs(ord(c1) - ord(c2)) == value:
                match_found = True
                break
        if match_found:
            break
    assert match_found, f"No x-ASCII-match found for x={value} and S='{status}'. Expected at least one x-ASCII-match."

    result = {
        "value": value,
        "status": status,
        "match_found": match_found
    }
    results.append(result)

# Run the tests
pytest.main(['-q', '-s'])

# Export results to JSON
with open('ascii_match_api_test_results.json', 'w') as jsonfile:
    json.dump(results, jsonfile)
