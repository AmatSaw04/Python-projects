import random
import smtplib
import datetime as dt


my_email = "amatyasawant@gmail.com"
password = "awjf tikk agnl nzdk"


now =  dt.datetime.now()
weekday = now.weekday()
if weekday ==1:
    with open("quotes.txt", "r") as quote:
        quote_of_day = quote.readlines()
        quotes = random.choice(quote_of_day)
    print(quotes)
    with smtplib.SMTP("smtp.gmail.com",  port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="amatyasawant2022@vitbhopal.ac.in",
            msg=f"Subject:Monday Motivation\n\n{quotes}")



