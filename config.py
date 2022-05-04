import os

GOOGLE_API_SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/contacts.readonly'
]

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID')
CONTACTS_CAL_ID = os.environ.get('CONTACTS_CAL_ID')
CREDENTIALS = os.environ.get('CREDENTIALS')
