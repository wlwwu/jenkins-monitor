import requests
from requests.auth import HTTPBasicAuth
import ConfigParser
from sys import argv
import os
import logging

class Notify(object):
    def __init__(self):
        self.element = argv[1]
        self.headers = {'Content-Type': 'application/json'}
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='jenkins-monitor.log',
                filemode='a')

    @staticmethod
    def load_config():
        email_credentials = {}
        config = ConfigParser.ConfigParser()
        configFilePath = '/root/jenkins-monitor/configuartion'
        os.listdir('.')
        config.read(configFilePath)
        environment = config.get('parameters', 'environment')
        email_username = config.get('parameters', 'email_username')
        email_password = config.get("parameters", "email_password")
        email_url = config.get("parameters", "email_url")
        email_sender = config.get("parameters", "email_sender")
        email_updated_password = config.get("parameters", "email_updated_password")
        recipients = config.get("parameters", "recipients")
        email_credentials["environment"] = environment
        email_credentials["email_username"] = email_username
        email_credentials["email_password"] = email_password
        email_credentials["email_url"] = email_url
        email_credentials["email_sender"] = email_sender
        email_credentials["email_updated_password"] = email_updated_password
        email_credentials["recipients"] = recipients
        return email_credentials

    @staticmethod
    def config_email_service():
        notify = Notify()
        email_credentials = notify.load_config()
        email_username = email_credentials["email_username"]
        email_password = email_credentials["email_password"]
        email_url = email_credentials["email_url"]
        email_sender = email_credentials["email_sender"]
        email_updated_password = email_credentials["email_updated_password"]
        sub_url = "/management/mailAddresses/"
        url = email_url + sub_url + email_sender
        register_email = requests.post(url, headers= notify.headers, auth=HTTPBasicAuth(email_username, email_password))
        update_url = url + "/password/" + email_updated_password
        update_registered_password = requests.put(update_url, headers=notify.headers, auth=HTTPBasicAuth(email_username, email_password))
        status_code = [register_email.status_code, update_registered_password.status_code]
        print status_code
        return status_code

    @staticmethod
    def send_notification():
        notify = Notify()
        email_content = {}
        email_credentials = notify.load_config()
        environment = email_credentials["environment"]
        email_username = email_credentials["email_username"]
        email_password = email_credentials["email_password"]
        email_url = email_credentials["email_url"]
        email_sender = email_credentials["email_sender"]
        email_updated_password = email_credentials["email_updated_password"]
        recipients = email_credentials["recipients"]
        email_content["recipients"] = [{"to": recipients}]
        email_content["from"] = {"eMail": email_sender, "password": email_updated_password}
        alert_type = notify.element
        if alert_type == 'jenkins':
            content = environment + ' BuildpackManager Jenkins process down'
            email_content["subject"] = {"content": content}
            email_content["body"] = {
                "content": "Alerts! BuildpackManager Jenkins process down!",
                "contentType": "text/html"}
        elif alert_type == 'cpu':
            content = environment + ' BuildpackManager Jenkins vm cpu high'
            email_content["subject"] = {"content": content}
            email_content["body"] = {
                "content": "Alerts! BuildpackManager Jenkins vm cpu high!",
                "contentType": "text/html"}
        elif alert_type == 'memory':
            content = environment + ' BuildpackManager Jenkins vm memory high'
            email_content["subject"] = {"content": content}
            email_content["body"] = {
                "content": "Alerts! BuildpackManager Jenkins vm memory high!",
                "contentType": "text/html"}

        url = email_url + "/email"
        print "url:"
        print url
        print email_username
        print email_password
        r = requests.post(url, headers=notify.headers, auth=HTTPBasicAuth(email_username, email_password), json=email_content)
        print "r.status_code:"
        print r.status_code
        return r.status_code


if __name__ == "__main__":
    notify = Notify()
    if argv[1] == 'register':
        status_code = notify.config_email_service()
        if status_code[0] == 200:
            logging.info("email register successfully")
            print("email register successfully")
        elif status_code[0] != 200:
            logging.info("email register failed")
            print("email register failed")
        elif status_code[1] == 200:
            logging.info("email password update successfully")
            print("email password update successfully")
        else:
            logging.info("email password update failed")
            print ("email password update failed")
    else:
        notification_status_code = notify.send_notification()
        if notification_status_code == 200:
            logging.info("notification sent successfully")
            print("notification sent successfully")
        else:
            logging.info("notification sent failed")
            print("notification sent failed")