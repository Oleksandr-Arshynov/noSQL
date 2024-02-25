import pika
from faker import Faker
import mongoengine
from mongoengine import connect
from models import Contact

connect(db="my_db", host="mongodb+srv://oleksandr:dnkUq22IrgB7cDyq@cluster0.tgvrxhn.mongodb.net/my_db?retryWrites=true&w=majority&appName=Cluster0")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='contacts_queue')
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

# Генерування фейкових контактів та їх збереження у базу даних та надсилання в чергу
fake = Faker()
for _ in range(10):  # Генеруємо 10 фейкових контактів для прикладу
    full_name = fake.name()
    email = fake.email()
    phone_number = fake.phone_number()
    contact = Contact(full_name=full_name, email=email, phone_number=phone_number)
    contact.save()

    # Надсилаємо ID контакту в чергу RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key='contacts_queue',
                          body=str(contact.id))
    print(f"Sent {contact.id}")
    
    channel.basic_publish(exchange='',
                          routing_key='email_queue',
                          body=str(contact.id))
    print(f"Sent {contact.id}")
    
    channel.basic_publish(exchange='',
                          routing_key='sms_queue',
                          body=str(contact.id))
    print(f"Sent {contact.id}")

connection.close()
