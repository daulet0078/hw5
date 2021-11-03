import smtplib


rec_email = "mirkhad.chekirbaev@gmail.com"
sender_email = "mirkhad.chekirbaev@iaau.edu.kg"
message = "code message"
password = input("enter password")

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

server.login(sender_email, password)
print("Login success")
server.sendmail(sender_email, rec_email, message)
print("Email has ben sent to ", rec_email)