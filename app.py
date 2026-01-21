from flask import Flask
import requests

app = Flask(__name__)

def get_metadata(path):
    token = requests.put(
        "http://169.254.169.254/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        timeout=2
    ).text

    return requests.get(
        f"http://169.254.169.254/latest/meta-data/{path}",
        headers={"X-aws-ec2-metadata-token": token},
        timeout=2
    ).text

@app.route("/")
def home():
    az = get_metadata("placement/availability-zone")
    region = az[:-1]
    return f"Region: {region}, AZ: {az}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
