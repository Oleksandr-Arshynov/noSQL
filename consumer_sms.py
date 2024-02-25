import pika
from models import Contact

def callback(ch, method, properties, body):
    # Обробка повідомлення з черги для SMS
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending SMS to {contact.phone_number}...")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue')
    channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for SMS messages...')
    channel.start_consuming()

if __name__ == '__main__':
    main()
