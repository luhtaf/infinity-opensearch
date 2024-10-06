from flask import Flask, request, jsonify
import yaml
import time
import requests
# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Global variables
opensearch_url = config['opensearch']['url']
username = config['opensearch']['username']
password = config['opensearch']['password']
headers = {
    "Content-Type": "application/json"
}
app = Flask(__name__)

# Endpoint to count documents
@app.route('/count', methods=['GET','POST'])
def get_count():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": from_time,
                    "lte": to_time,
                    "format": "epoch_millis"
                }
            }
        }
    }

    index_pattern = "wazuh-alerts*"
    print("coba")
    url=f"{opensearch_url}/{index_pattern}/_count"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    # Return count response
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
