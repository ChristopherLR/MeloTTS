import requests

sample_texts = [
    "It seems to me that the natural world is the greatest source of excitement; the greatest source of visual beauty; the greatest source of intellectual interest. It is the greatest source of so much in life that makes life worth living."
]


def test_en_us():
    url = "http://localhost:9000/audio/speech"
    data = {"text": sample_texts[0], "voice": "EN-US"}

    response = requests.post(url, json=data)

    assert response.status_code == 200

    with open("output-en-us.wav", "wb") as f:
        f.write(response.content)


def test_default():
    url = "http://localhost:9000/audio/speech"
    data = {"text": sample_texts[0]}

    response = requests.post(url, json=data)

    assert response.status_code == 200

    with open("output-default.wav", "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    test_default()
    test_en_us()
