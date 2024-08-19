# Crazy Calculatorz - Vulnerable Web Application

## Overview
Crazy Calculatorz is a custom-built, intentionally vulnerable web server designed for educational purposes. This project was developed for CSEC 731 to simulate security flaws commonly found in web applications and to provide a hands-on learning experience in web app protocols, security, and the entire lifecycle from development to deployment.

The application was developed using raw socket programming and a self-written HTTP parser. It was then containerized using Docker and deployed automatically via Ansible. A comprehensive security analysis was conducted, including detailed documentation of the vulnerabilities present within the application.

## Important Disclaimer
**This application contains intentionally built vulnerabilities and is highly insecure.** It should only be used in a controlled environment for educational purposes. Do not deploy this application on a production server or expose it to the internet, as it poses a significant security risk.

## Project Documentation
- [Ansible Documentation](./ansible/ansible_README.md)
- [Code Documentation](./code/code_README.md)
- [Docker Documentation](./docker/docker_README.md)
- [Vulnerability Report](./documents/vulnerability_report.md)
- [Risk Assessment](./documents/Crazy_Calculatorz_Risk_Assesment.pdf)

## Features
- **Custom Web Server:** Developed using raw socket programming and a custom HTTP parser.
- **Intentional Vulnerabilities:** Designed to simulate real-world security flaws for educational use.
- **Dockerized Deployment:** Easily deploy the application in a controlled environment using Docker.
- **Automated Deployment:** Ansible scripts are provided to automate the deployment process.
- **Security Analysis:** Comprehensive documentation and analysis of the vulnerabilities present in the application.
- **Automated Testing:** Selenium scripts provided for automated testing and exploitation of the web application.

## Learning Objectives
- Understand the basics of web server development and HTTP protocol.
- Learn how security flaws can be introduced during the development process.
- Gain hands-on experience in identifying and exploiting vulnerabilities.
- Explore containerization and automated deployment with Docker and Ansible.
- Conduct a thorough security analysis and document findings effectively.

## Usage
To set up and run the Crazy Calculatorz web application, please refer to the respective documentation linked above for detailed instructions on Ansible deployment, Docker setup, and code structure.

**Remember:** This application is intended for educational purposes only. Use it responsibly within a secure and isolated environment.