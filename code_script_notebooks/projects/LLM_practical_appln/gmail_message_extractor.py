#Script to extract the messages from your gmail account and store it as txt file.
#This script will be the feeder for the summarization activity that we will 
#inside the Colab Environment

from simplegmail import Gmail
from simplegmail.query import construct_query

gmail = Gmail()

query_params = {
    "read":True,
    "sender":["action@ifttt.com"],
    "newer_than":(5,"day"),
    "labels":[["CATEGORY_FORUMS"],["INBOX"]]
}

promo_query = construct_query(query_params)

output = gmail.get_messages(query=promo_query)

with open('mail_collector.txt','a') as col:
    for mail in output:    
        #writing sender
        col.write(mail.sender)
        col.write('\n')
        #writing subject
        col.write(mail.subject)
        col.write('\n')
        col.write(mail.date)
        #writing plain text part of mail 
        if mail.plain:
            txt = mail.plain.strip()
            txt = txt.replace('\n','')
            txt = txt.replace('\r','')
            col.write(txt)
        else:
            col.write('No Plain Text data')
        col.write('\n')

print('Write completed')
