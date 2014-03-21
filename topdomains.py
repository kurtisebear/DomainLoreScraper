import urllib2
import cookielib
import urllib
import json
import smtplib
import email
import os
import config
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEText import MIMEText
import mimetypes

#cookies
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


# headers
opener.addheaders = [('User-agent', 'firefox')]

urllib2.install_opener(opener)

#the target action
auth_url = 'https://domainlore.co.uk/member/login'

#send parms add your domainlore.co.uk username and password here
payload = ({
	'email': os.environ['DLORE_USERNAME'],
	'password': os.environ['DLORE_PASSWORD'],
	'return_to': '',
	'submit': 'Log in'
})

#get just domain and tag
def droplist(parsed, d=[]):
    for c in parsed['droplist']:
        d.append({'Domain:' : c.get('d'), 'Tag' : c.get('t')})
    return d

#send email with list of domains change user & passw for your gmail details and from and to address
def emaillist(listofdomains):
    user = os.environ['GMAIL_USERNAME']
    passw = os.environ['GMAIL_PASSWORD']
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP()
    server.connect(smtp_host,smtp_port)
    server.ehlo()
    server.starttls()
    server.login(user,passw)
    fromaddr = 'GMAIL EMAIL'
    toaddr = 'ANY EMAIL'
    subject = 'Top Domains Dropping'

    msg = email.MIMEMultipart.MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(listofdomains))
    server.sendmail(user,toaddr,msg.as_string())
    



data = urllib.urlencode(payload)
print data

req= urllib2.Request(auth_url, data)

resp = urllib2.urlopen(req)
contents = resp.read()




listdomains = 'http://domainlore.co.uk/droplist/json/1/1'
req1 = urllib2.Request(listdomains)

resp1 = urllib2.urlopen(req1)

contents1 = resp1.read()
parsed = json.loads(contents1)
listofdomains = droplist(parsed)
listofdomains = json.dumps(listofdomains, indent=4, sort_keys=True)


emaillist(listofdomains)
