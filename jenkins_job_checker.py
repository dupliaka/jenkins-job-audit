import csv
import re
import jenkins
from typing import List, Tuple
import os


def parse_job_url(job_url: str) -> str:
    """
    Parse the job URL to extract the specific job path.
    """
    job_link = re.sub(r'%20', ' ', job_url)
    return re.sub(r'^https://[^/]+|/job', '', job_link).strip('/')


def get_job_config(server: jenkins.Jenkins, job_path: str) -> str:
    """
    Retrieve the job configuration XML from Jenkins.
    """
    try:
        return server.get_job_config(job_path)
    except jenkins.JenkinsException as e:
        print(f"Error checking url {job_path}: {str(e)}")
        return ""


def find_owners_in_config(config_xml: str, owners_list: List[str]) -> List[str]:
    """
    Find the job owners present in the job configuration XML.
    """
    # If the owners are in specific XML tags, consider parsing the XML and finding them.
    # Here we're keeping the original approach as we don't have the XML structure.
    return [owner for owner in owners_list if owner in config_xml]


def check_job(server: jenkins.Jenkins, job: dict, owners_list: List[str]) -> List[Tuple[str, str, List[str]]]:
    """
    Check the job for owners and recurse if nested jobs are found.
    """
    jobs_info = []

    if 'jobs' in job:
        for sub_job in job['jobs']:
            jobs_info.extend(check_job(server, sub_job, owners_list))
    else:
        job_path = parse_job_url(job["url"])
        xml_config = get_job_config(server, job_path)
        owners = find_owners_in_config(xml_config, owners_list)
        jobs_info.append((job["name"], job["url"], owners))

    return jobs_info


def read_api_config(filename: str) -> tuple[str, ...]:
    """
    Read the Jenkins API configuration from the environment or a file.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return tuple(line.strip() for line in f.readlines())
    else:
        # Consider raising an error if the configuration is not found
        return os.getenv('JENKINS_URL', ''), os.getenv('JENKINS_USERNAME', ''), os.getenv('JENKINS_API_KEY', '')


def read_owners(filename: str) -> List[str]:
    """
    Read the list of owners from a file.
    """
    with open(filename, 'r') as f:
        return [owner.strip() for owner in f.readlines()]


def main():
    # Configurations
    api_config_file = '.api_key'
    owners_file = '.owners'
    report_file = "report.csv"

    # Read configurations
    jenkins_url, username, api_key = read_api_config(api_config_file)
    owners_list = read_owners(owners_file)

    # Initialize Jenkins server connection
    server = jenkins.Jenkins(jenkins_url, username=username, password=api_key)

    # Fetch all jobs and check for job owners
    jobs = server.get_jobs()
    jobs_info = []
    for job in jobs:
        jobs_info.extend(check_job(server, job, owners_list))

    # Write the job information to a CSV file
    with open(report_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(("name", "url", "owner"))
        for job_info in jobs_info:
            name, url, owners = job_info
            writer.writerow((name, url, ", ".join(owners)))


if __name__ == "__main__":
    main()