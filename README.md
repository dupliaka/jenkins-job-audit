# Jenkins Job Checker
This Python script interacts with a Jenkins server, retrieves information about jobs, and records certain details (name, URL, and owner) into a CSV file. It's particularly useful for administrators who need to audit Jenkins jobs and understand job ownership.

## Features
- Retrieves jobs recursively from Jenkins.
- Checks job configuration for specific owners.
- Generates a CSV report listing job names, URLs, and owners.
## Prerequisites
- Python 3.6 or higher.
- Access to a Jenkins server with appropriate credentials.
- Required Python packages: python-jenkins.
## Installation
- Clone the repository or download the script directly.
- Install the required Python package python-jenkins using pip:

```
pip install python-jenkins
```

- Configure your Jenkins server URL, username, and API key. You can provide them via a configuration file or environment variables. Refer to the script's documentation for detailed instructions. 
Jenkins API key could be found under your Profile -> Configure -> API Token.
## Usage
1) Prepare your Jenkins credentials by either:
   - Placing your Jenkins server URL, username, and API token in a file named `.api_key` in the script's directory (each piece of information on a new line).
   - Or, setting environment variables: JENKINS_URL, JENKINS_USERNAME, and JENKINS_API_KEY.
2) Create a file named .owners containing the usernames of the potential owners you're checking against (each username on a new line).

Run the script:
```
python jenkins_job_checker.py
```

The script will create a `report.csv` file in the same directory, containing the name, URL, and owner of each Jenkins job.
