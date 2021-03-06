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
def process_raw_emails(cnx, ml_name, committers, base_dir):
    for dev in committers:
        id = dev['id']
        out_dir = '{0}/{1}'.format(base_dir, id)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        sender = dev['email']
        sender_alias = dev['alias']

        query = "select message_body, email_address from messages as M " \
                "inner join messages_people as MP on MP.message_id = M.message_id " \
                "inner join mailing_lists as ML on ML.mailing_list_url = MP.mailing_list_url" \
                "where  ML.mailing_list_name like '%{0}%' " \
                "AND (email_address = '{1}' OR email_address = '{2}') " \
                "AND type_of_recipient = 'From' " \
                "AND year(arrival_date) = %s AND month(arrival_date) = %s " \
                "order by arrival_date ASC;".format(ml_name, sender, sender_alias)
        cursor = cnx.cursor()

        # TODO should find start/end month/year through queries
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


def __process_results(cursor, out_dir, current_year, current_month):
    # perform some clean up then save query results to file and
    for (message_body, email_address) in cursor:
        new_file = '{0}/{1}-{2}.txt'.format(out_dir, current_year, current_month)

        clean_message_body = __clean_up(message_body)
        with open(new_file, 'w') as f:
            f.write(clean_message_body)
            f.close()


def __clean_up(message_body):
    soup = BS4(message_body, 'html.parser')
    clean_message_body = soup.text

    clean_message_body = re.sub(r'^\s*>+( .*)?', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'^\s*$+( .*)?', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'^\s*\+', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'^\s*---\+', '', clean_message_body, flags=re.MULTILINE)
    # dates
    clean_message_body = re.sub(r'https?:\/\/\S*', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'[\w\.-]+ @ [\w\.-]+', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'On .* wrote:.*', '', clean_message_body, flags=re.MULTILINE)
    clean_message_body = re.sub(r'\n[\t\s]*\n+', '', clean_message_body, flags=re.MULTILINE)

    clean_message_body = u''.join(clean_message_body).encode('utf-8').strip()
    return clean_message_body
