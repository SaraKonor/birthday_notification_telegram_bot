import datetime
import os
import re

import config
from gcal import GCal
from gcontacts import GContacts
from tg import send_message


class NotiBday:
    def __init__(self):
        self.calendar = GCal(config.CONTACTS_CAL_ID)
        self.agenda = GContacts()
        self.agenda.retrieve_contacts()

    @staticmethod
    def parse_bday_event(event):
        date, summary = event
        if not summary.startswith('Aniversario'):
            name = re.split(r'\s*–\s*', summary)[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        else:
            name, date = None, None
        return name, date

    def notify_today_birthdays(self):
        today = datetime.date.today().strftime('%d.%m.%Y')
        events = self.calendar.get_events()

        if events:
            buf = [f'🎂 *Дні народження сьогодні ({today}) у:*']
            for event in sorted(events, key=lambda t: t[1]):
                name, _ = NotiBday.parse_bday_event(event)
                if name:
                    age = self.agenda.get_contact_age(name)
                    phoneNumber = self.agenda.get_phone_number(name)
                    title = self.agenda.get_title(name)
                    department = self.agenda.get_department(name)

                    buf.append(f'')
                    buf.append(f'*{name}*, {age} років')
                    buf.append(f'{title}, {department}')
                    buf.append(f'{phoneNumber}')
        else:
            buf = [f'*Днів народженнів сьогодні ({today}) немає.*']
    
        msg = os.linesep.join(buf)
        send_message(msg)
