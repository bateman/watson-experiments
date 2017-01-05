import mysql.connector
import os
from bs4 import BeautifulSoup as BS4
import re


def connect():
    cnx = mysql.connector.connect(user='root',
                                  password='5tartQu3ry1ng!',
                                  host='127.0.0.1',
                                  database='mlstats')
    return cnx


def disconnect(cnx):
    cnx.close()


# first email march 2015
# last email december 2016
def build_corpus(cnx, committers, base_dir):
    for dev in committers:
        id = dev['id']
        out_dir = '{0}/{1}'.format(base_dir, id)
        sender = dev['email']
        sender_alias = dev['alias']

        query = "select message_body from messages as M " \
                "inner join messages_people on messages_people.message_id = M.message_id " \
                "where  M.mailing_list_url like '%groovy%' " \
                "AND (email_address = '{0}' OR email_address = '{1}') " \
                "AND type_of_recipient = 'From' " \
                "AND year(arrival_date) = %s AND month(arrival_date) = %s " \
                "order by arrival_date ASC;".format(sender, sender_alias)
        cursor = cnx.cursor()

        # year 2015
        current_month = 3
        current_year = 2015
        while current_month <= 12:
            # execute  query
            cursor.execute(query, (current_year, current_month))
            __process_results(cursor, out_dir, current_year, current_month)
            current_month += 1

        # year 2016
        current_month = 1
        current_year = 2016
        while current_month <= 12:
            # execute  query
            cursor.execute(query, (current_year, current_month))
            __process_results(cursor, out_dir, current_year, current_month)
            current_month += 1

        cursor.close()


def __process_results(cursor, directory, current_year, current_month):
    # perform some clean up then save query results to file and
    for (message_body) in cursor:
        if not os.path.exists(directory):
            os.makedirs(directory)
        new_file = '{0}/{1}-{2}.txt'.format(directory, current_year, current_month)

        clean_message_body = __clean_up(message_body)
        with open(new_file, 'w') as f:
            f.write(clean_message_body)
            f.close()


def __clean_up(message_body):
    soup = BS4(message_body, 'html.parser')
    clean_message_body = soup.text

    clean_message_body = re.sub(r'^\s*>+( .*)?', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'^\s*\+', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'^\s*---\+', '', clean_message_body, flags=re.MULTILINE)
    # dates
    clean_message_body = re.sub(r'https?:\/\/\S*', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'[\w\.-]+ @ [\w\.-]+', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'On .* wrote:.*', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'\n[\t\s]*\n+', '', clean_message_body, flags=re.MULTILINE)

    clean_message_body = u''.join(clean_message_body).encode('utf-8').strip()
    return clean_message_body
