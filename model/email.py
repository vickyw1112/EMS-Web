import yagmail

DEF_EMAIL_ADDRESS = ""
DEF_EMAIL_PASSWORD = ""

class email():
    def send_email(srcEmail, srcPassword, destEmail, subject, msg):
        yag = yagmail.SMTP(srcEmail, srcPassword)

        #html_msg = """<p>Hi!<br>
        #              How are you?<br>
        #              Here is the <a href="http://www.python.org">link</a> you wanted.</p>"""
        
        yag.send(destEmail, subject, msg)

    def email_eventCancelled(destName, destEmail, event):
        msg = "<p>Hello, <i>"+destName+"</i>!<br />"+ \
                "Unfortunately, the event you have previously joined, <br />" + \
                '<b>"'+event+'"</b><br />'+ \
                "Has been cancelled and no longer available for joining <br />" + \
                "We apologise for any unconvenience <br />" +  \
                "<br />" + \
                "Best Regards, <br />" + \
                "<i>nlogn</i></p>"
                
        
        cls.send_email(DEF_EMAIL_ADDRESS, DEF_EMAIL_PASSWORD, destEmail, "Event cancellation", msg)

        
