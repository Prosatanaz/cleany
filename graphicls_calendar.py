from __future__ import print_function

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GoogleCalendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = 'clinny-361618-f313b3437739.json'

    def __init__(self):
        credentials = Credentials.from_service_account_file('clinny-361618-f313b3437739.json', scopes=self.SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendarId):
        calendar_list_entry = {'id': calendarId}
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def get_calendar(self, calendarId):
        calendar = self.service.calendars().get(calendarId=calendarId).execute()

        return calendar

    def create_event(self, start_time, end_time, description, calendarId):
        event = {
            'summary': 'Google I/O 2015',

            'description': description,
            'start': {
                'dateTime': start_time,
            },
            'end': {
                'dateTime': end_time,
            },
        }
        event = self.service.events().insert(calendarId=calendarId, body=event).execute()
        return event


calendarId = 'i7mlmtftm205o983g9f2kubsgo@group.calendar.google.com'
obj = GoogleCalendar()
start_time = '2022-09-08T09:00:00-07:00'
end_time = '2022-09-08T09:00:00-09:00'
description = 'fgdgdfg'
obj.add_calendar(calendarId)
print(obj.get_calendar(calendarId))
print(obj.create_event(start_time, end_time, description, calendarId))
