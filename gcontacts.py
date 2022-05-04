import datetime

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools

import config


class GContacts:
    def __init__(self):
        credFile = open('credentials.json', 'w')
        credFile.write(config.CREDENTIALS)
        credFile.close()

        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json',
                                                  config.GOOGLE_API_SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('people', 'v1', http=creds.authorize(Http()))

    def retrieve_contacts(self):
        data = self.service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            personFields='names,birthdays,phoneNumbers,organizations').execute()

        self.contacts = {}
        for contact in data['connections']:
            if 'names' in contact.keys():
                full_name = contact['names'][0]['displayName']
                self.contacts[full_name] = {
                    "phoneNumber": "",
                    "title": "",
                    "department": ""
                }

                if 'birthdays' in contact.keys():
                    birthday = contact['birthdays'][0]['date']
                    self.contacts[full_name]['birthdate'] = datetime.date(**birthday)

                if 'phoneNumbers' in contact.keys():
                    self.contacts[full_name]['phoneNumber'] = contact['phoneNumbers'][0]['canonicalForm']

                if 'organizations' in contact.keys():
                    organization = contact['organizations'][0]
                    self.contacts[full_name]['title'] = organization['title']
                    
                    if 'department' in organization.keys():
                        self.contacts[full_name]['department'] = organization['department']

    def get_contact_age(self, contact_name):
        birthdate = self.contacts.get(contact_name)['birthdate']
        if birthdate is None:
            return -1
        delta = datetime.date.today() - birthdate
        return round(delta.days / 365)

    def get_phone_number(self, contact_name):
        return self.contacts.get(contact_name)['phoneNumber']

    def get_title(self, contact_name):
        return self.contacts.get(contact_name)['title']

    def get_department(self, contact_name):
        return self.contacts.get(contact_name)['department']
