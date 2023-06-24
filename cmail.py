import smtplib
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('yaswanthganji123@gmail.com','fsfzeiwgzcjoswzo')
    msg=EmailMessage()
    msg['From']='yaswanthganji23@gmail.com'
    msg['To']=to
    msg['Subject']=subject
    msg.set_content(body)
    server.send_message(msg)
    server.quit()
