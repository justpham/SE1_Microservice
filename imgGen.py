import pika
import os
from PIL import Image, ImageTk
import tkinter as tk

#establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='image_name_queue')
channel.queue_declare(queue='response_queue') 

def display_image(image_path):
    
    root = tk.Tk()
    root.title("Presidential Portrait")
    
    #load and display the image using Pillow
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    label.image = photo
    label.pack()

    root.mainloop()

#send response back if the presidential image does not exist
def send_response(response_message):
    
    channel.basic_publish(exchange='', routing_key='response_queue', body=response_message)

#recieve President name from descGen.py
def callback(ch, method, properties, body):
    
    president = body.decode('utf-8')
    format_president = body.decode('utf-8').replace(' ', '_')
    print(f"Received image name: {format_president}")

    #search for the image in the 'images' folder using the proper format
    image_path = os.path.join('images', f"{format_president}.jpg")
    
    #output image status
    if os.path.exists(image_path):
        
        print(f"Image found: {image_path}")
        display_image(image_path)
        send_response("Image found")

    else:
        
        print(f"Image not found for {president}")
        send_response("Image not found")

channel.basic_consume(queue='image_name_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
