import pika
import tkinter as tk
import wikipedia

#establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='image_name_queue')

#declare a new queue for errors/reponses
channel.queue_declare(queue='response_queue')  

#check for a response
def check_for_response():
    
    method_frame, header_frame, body = channel.basic_get(queue='response_queue', auto_ack=True)

    #display response message
    if body:
        
        response_message = body.decode('utf-8')
        print(response_message)
       
        if response_message == "Image not found":
            
            text_label.config(text="Image not found. Please enter a valid current or former U.S President. \nEx: 'George Washington'")
            
    #repeat check after short delay
    root.after(100, check_for_response)

#retrieve the description using the Wikipedia API
def get_president_description():
    
    president_name = entry.get()
    president_page = wikipedia.page(president_name)
    paragraphs = president_page.summary.split('\n')
    first_paragraph = paragraphs[0]

    #add border around the generated description
    text_label.config(text=first_paragraph, bd=2, relief="solid")

    #add entered name to the listbox
    president_names.insert(tk.END, president_name.center(30))

    #send president name to image generation queue
    channel.basic_publish(exchange='', routing_key='image_name_queue', body=president_name)

#clear contents of GUI
def clear_content():
    
    entry.delete(0, tk.END)
    text_label.config(text="")

#build GUI window
root = tk.Tk()
root.title("President Description and Image Generator")
root.geometry("800x800")
root.configure(bg="light blue")

#build GUI elements
presidential_description_label = tk.Label(root, text="Enter the Name of any Current or Former United States President:", font=("Arial", 14))
presidential_description_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=10)

button = tk.Button(root, text="Get Description", command=get_president_description, font=("Arial", 12))
button.pack(pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_content, font=("Arial", 12))
clear_button.pack(pady=10)

presidential_description_label = tk.Label(root, text="Description of the President (source: Wikipedia):",
                                          font=("Arial", 14))
presidential_description_label.pack()

text_label = tk.Label(root, text="", font=("Arial", 12), wraplength=600)
text_label.pack(pady=20)

president_names_label = tk.Label(root, text="Entered Names:", font=("Arial", 14), width=21, height=2)
president_names_label.pack(pady=10)

president_names_frame = tk.Frame(root, width=200, height=200)
president_names_frame.pack(pady=10)

president_names = tk.Listbox(president_names_frame, font=("Arial", 12), width=30, height=15)
president_names.pack(fill=tk.BOTH, expand=True)

president_names_label.pack_configure(anchor=tk.CENTER)
president_names_frame.pack_configure(anchor=tk.CENTER)

president_names_frame.pack_propagate(0)

root.after(100, check_for_response)
root.mainloop()
