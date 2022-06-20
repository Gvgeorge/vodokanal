from typing import IO

import httplib2
from apiclient.discovery import Resource, build
from dateutil.parser import parse
from django.core.exceptions import ValidationError
from oauth2client.service_account import ServiceAccountCredentials

from .validator import validate_order_row


# Авторизуемся и получаем service — экземпляр доступа к API
def create_gsheets_service(cred_file: IO) -> Resource:
    '''
    Авторизуется и получает service — экземпляр доступа к API
    cred_file - файл с креденшиалами, который выдает гуглапи
    '''
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        cred_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = build('sheets', 'v4', http=httpAuth)
    return service


def read_values(service: Resource,
                spreadsheetID: str,
                sheet: str, left_c: str, right_c: str) -> dict:
    '''
    Принимает на вход service — экземпляр доступа к API, название книги, листа,
    левую колонку, правую колонку.
    Возвращает значения между этими колонками.
    '''
    response = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheetID,
        ranges=f'{sheet}!{left_c}:{right_c}',
        majorDimension='ROWS'
    ).execute()
    return response


def parse_values_for_db(values: list) -> list:
    '''
    Проверяет и конвертирует данные на соответствие полям в БД
    '''
    values = values['valueRanges'][0]['values'][1:]
    response = []
    for row in values:
        try:
            validate_order_row(row)
        except ValidationError:
            continue
        parsed_row = {'row_id': int(row[0]),
                      'order_id': int(row[1]),
                      'amount_usd': float(row[2].replace(',',  '.')),
                      'date': parse(row[3], dayfirst=True).date()}
        response.append(parsed_row)
    return response


