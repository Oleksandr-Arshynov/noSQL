import pika
from mongoengine import connect
from models import Contact
import mongoengine

connect(db="my_db", host="mongodb+srv://oleksandr:dnkUq22IrgB7cDyq@cluster0.tgvrxhn.mongodb.net/my_db?retryWrites=true&w=majority&appName=Cluster0")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue')


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects.get(id=contact_id)

    print(f"Sending email to {contact.email}")
    contact.email_sent = True
    contact.save()

    print(f"Email sent to {contact.email}")


# Підписуємось на чергу та обробляємо повідомлення
channel.basic_consume(queue='contacts_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
