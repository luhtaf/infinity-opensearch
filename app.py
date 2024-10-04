from flask import Flask, request, jsonify
from opensearchpy import OpenSearch
import yaml
import time

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Global variables
opensearch_url = config['opensearch']['url']
username = config['opensearch']['username']
password = config['opensearch']['password']

# Initialize OpenSearch client
client = OpenSearch(
    [opensearch_url],
    http_auth=(username, password),
    verify_certs=True
)

app = Flask(__name__)

# Endpoint to count documents
@app.route('/count', methods=['GET'])
def get_count():
    # Get 'from' and 'to' from request parameters (in epoch)
    from_time = request.args.get('from')
    to_time = request.args.get('to')

    # Query for count with timestamp filter
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
    response = client.count(index=index_pattern, body=query)
    
    # Return count response
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
