import requests
import json


def submission(is_test=False,host='192.168.1.200',port='3000'):

    if is_test:
        url = "http://" + host + ":" + port + "/test/submit"
    else:
        url = "http://" + host + ":" + port + "/submit"

    payload = {
		"scene_no": 1,
		"ppe": {
			"helmet": True,
			"glasses": True,
			"coverall": True,
			"boots": True,
			"gloves": True
		}
	}

    header = {
		"Content-Type": "application/json",
		"cache-control": "no-cache",
		"Authorization": "Bearer " +  "NA3TTAB-ET7MF2J-P21KZY2-A3XK35N"
	}

    response_decoded_json = requests.post(url, data=json.dumps(payload), headers=header)
    try:
        response_json = response_decoded_json.json()
        print("Complete to request",payload)
        print()
        return True
    except:
        print("Cannot submit the answer")
        print()
        return False
submission(is_test=True)