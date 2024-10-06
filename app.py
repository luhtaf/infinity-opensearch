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
@app.route('/countall', methods=['GET','POST'])
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
    url=f"{opensearch_url}/{index_pattern}/_count"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    # Return count response
    return jsonify(response.json())

@app.route('/auth_success_count', methods=['GET'])
def get_count_auth_success():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query = {
        "query": {
            "bool": {
                "must": [
                    { "match": { "rule.groups": "authentication_success" } },
                    { 
                        "range": {
                            "@timestamp": {
                            "gte": from_time,
                            "lte": to_time
                            }
                        }
                    }
                ]
            }
        }
    }
    index_pattern = "*"
    url=f"{opensearch_url}/{index_pattern}/_count"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    return jsonify(response.json())

@app.route('/medium_vuln_count', methods=['GET'])
def get_count_medium_vuln():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query = {
        "query": {
            "bool": {
                "must": [
                    { "range": {
                        "rule.level": {
                            "gte": 7,
                            "lte": 11
                            }
                        }
                    },
                    { 
                        "range": {
                            "@timestamp": {
                            "gte": from_time,
                            "lte": to_time
                            }
                        }
                    }
                ]
            }
        }
    }
    index_pattern = "wazuh-alerts*"
    url=f"{opensearch_url}/{index_pattern}/_count"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    return jsonify(response.json())

@app.route('/high_vuln_count', methods=['GET'])
def get_count_high_vuln():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query = {
        "query": {
            "bool": {
                "must": [
                    { "range": {
                        "rule.level": {
                            "gte": 12,
                            "lte": 14
                            }
                        }
                    },
                    { 
                        "range": {
                            "@timestamp": {
                            "gte": from_time,
                            "lte": to_time
                            }
                        }
                    }
                ]
            }
        }
    }
    index_pattern = "*"
    url=f"{opensearch_url}/{index_pattern}/_count"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    return jsonify(response.json())

@app.route('/critical_vuln_count', methods=['GET'])
def get_count_critical_count():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query = {
        "query": {
            "bool": {
                "must": [
                    { "range": {
                        "rule.level": {
                            "gte": 15,
                            }
                        }
                    },
                    { 
                        "range": {
                            "@timestamp": {
                            "gte": from_time,
                            "lte": to_time
                            }
                        }
                    }
                ]
            }
        }
    }
    index_pattern = "*"
    url=f"{opensearch_url}/{index_pattern}/_count"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    return jsonify(response.json())

@app.route('/top5_host_event', methods=['GET'])
def get_aggs_agent_event():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query= {
    "size": 0,
    "query": {
        "range": {
            "@timestamp": {
                "gte": from_time,
                "lte": to_time
            }
        }
    },
    "aggs": {
        "agent_names": {
            "terms": {
                "field": "agent.name",
                "size": 5  
            }
        }
    }
}

    index_pattern = "*"
    url=f"{opensearch_url}/{index_pattern}/_search"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    data = response.json()
    # buckets=buckets = data['aggregations']['agent_names']['buckets']
    # result_dict = {bucket['key']: bucket['doc_count'] for bucket in buckets}
    # return jsonify(result_dict)
    return jsonify(data)

@app.route('/top10_alerts', methods=['GET'])
def get_aggs_top10_alert():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query= {
        "size": 0,
        "query": {
            "range": {
                "@timestamp": {
                    "gte": from_time,
                    "lte": to_time
                }
            }
        },
        "aggs": {
            "alert_level": {
                "terms": {
                    "field": "rule.level",
                    "size": 10  
                }
            }
        }
    }
    index_pattern = "*"
    url=f"{opensearch_url}/{index_pattern}/_search"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    data = response.json()
    return data

@app.route('/vulnerability_severity_level', methods=['GET'])
def get_aggs_vuln_severity_level():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query = {
        "size": 0,
        "query": {
            "range": {
            "@timestamp": {
                "gte": from_time,
                "lte": to_time
            }
            }
        },
        "aggs": {
            "severity_levels": {
            "filters": {
                "filters": {
                "low": { "range": { "rule.level": { "gte": 0, "lte": 6 } } },
                "medium": { "range": { "rule.level": { "gte": 7, "lte": 11 } } },
                "high": { "range": { "rule.level": { "gte": 12, "lte": 14 } } },
                "critical": { "range": { "rule.level": { "gte": 15 } } }
                }
            }
            }
        }
    }

    index_pattern = "*"
    url=f"{opensearch_url}/{index_pattern}/_search"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    data = response.json()
    return data

@app.route('/top10_mitre', methods=['GET'])
def get_aggs_top10_mitre():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    query= {
        "size": 0,
        "query": {
            "range": {
                "@timestamp": {
                    "gte": from_time,
                    "lte": to_time
                }
            }
        },
        "aggs": {
            "alert_level": {
                "terms": {
                    "field": "rule.mitre.technique",
                    "size": 10  
                }
            }
        }
    }
    index_pattern = "*"
    url=f"{opensearch_url}/{index_pattern}/_search"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    data = response.json()
    return data

@app.route('/raw_alert', methods=['GET'])
def get_latest_alert():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    size=request.args.get('size', default=10, type=int)
    query= {
        "size": size,
        "sort": [
            {
            "@timestamp": {
                "order": "desc"
            }
            }
        ],
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
    url=f"{opensearch_url}/{index_pattern}/_search"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    data = response.json()
    return data

@app.route('/suricata_alert', methods=['GET'])
def get_suricata_alert():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    size=request.args.get('size', default=10, type=int)
    query={
        "size": size,
        "sort": [
            {
                "@timestamp": {
                    "order": "desc"
                }
            }
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": from_time,
                                "lte": to_time,
                                "format": "epoch_millis"
                            }
                        }
                    },
                    {
                        "term": {
                            "alert.group": "suricata"
                        }
                    }
                ]
            }
        }
    }

    index_pattern = "wazuh-alerts*"
    url=f"{opensearch_url}/{index_pattern}/_search"
    response = requests.get(url, headers=headers, json=query, auth=(username, password))
    data = response.json()
    return data



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
