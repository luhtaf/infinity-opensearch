# Flask OpenSearch API

A simple Flask API that interacts with an OpenSearch instance. This API provides an endpoint that allows users to query the count of documents from OpenSearch based on a specified time range.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Running the Application](#running-the-application)
4. [API Endpoints](#api-endpoints)
5. [Configuration](#configuration)
6. [Notes](#notes)
7. [Contributing](#contributing)
8. [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (`venv`) for managing dependencies

## Setup Instructions

### 1. Clone the Repository

Open your terminal and run the following command to clone the repository:

```bash
git clone https://github.com/luhtaf/infinity-opensearch.git
cd infinity-opensearch/api_elastic
```

### 2. Set Up Virtual Environment

Create a virtual environment to isolate your project dependencies:

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

- For Linux/MacOS:
  ```bash
  source venv/bin/activate
  ```
### Activate the Virtual Environment

- For Windows:
  ```bash
  venv\Scripts\activate
  ```
### 3. Install Dependencies

Once the virtual environment is activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a configuration file from the provided example:

```bash
cp config.yaml.example config.yaml
```

Edit config.yaml and provide your OpenSearch URL, username, and password:

```yaml
opensearch:
  url: "https://your-opensearch-url.com/api/elastic/"
  username: "<your_username>"
  password: "<your_password>"
```

Make sure to replace your_username and your_password with your actual OpenSearch credentials.

## Running the Application

To start the Flask API, use the following command:

```bash
python app.py
```

The application will start in development mode and listen on http://127.0.0.1:5000/.

## Notes

- Ensure that your OpenSearch instance is accessible and that the credentials provided in `config.yaml` are correct.
- The endpoint uses OpenSearch’ API and filters data based on the `@timestamp` field. Adjust your queries accordingly based on your OpenSearch index mappings.
- If you encounter any errors, check the logs in your Flask application for more details.

## Contributing

Feel free to fork the repository and open pull requests for any improvements or additional features. Please ensure your code adheres to the existing style and includes appropriate tests where applicable.

## License

This project is open source license, please use it wisely.
