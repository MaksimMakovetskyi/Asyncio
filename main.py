import sqlite3
import asyncio
from email.message import EmailMessage

import aiosmtplib


async def send_email():
    sqlite_connection = sqlite3.connect('contacts.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = "SELECT first_name, last_name, email from contacts"
    cursor.execute(sqlite_select_query)
    data = cursor.fetchall()
    for row in data:
        message = EmailMessage()
        message["From"] = "root@localhost"
        message["To"] = f"{row[2]}"
        message["Subject"] = "Hello Customer!"
        message.set_content(f"Уважаемый(ая) {row[0]}{row[1]}! Спасибо, что пользуетесь нашим сервисом объявлений.")

        await aiosmtplib.send(message, hostname="smtp.gmail.com", port=465, use_tls=True)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(send_email())
