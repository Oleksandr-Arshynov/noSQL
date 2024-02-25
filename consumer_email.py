import pika
from models import Contact

def callback(ch, method, properties, body):
    # Обробка повідомлення з черги для електронної пошти
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        # Надсилання електронної пошти
        print(f"Sending email to {contact.email}...")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for email messages...')
    channel.start_consuming()

if __name__ == '__main__':
    main()
