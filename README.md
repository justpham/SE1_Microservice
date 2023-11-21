# U.S President Description and Portrait Generator

This project consists of two microservices: `descGen.py` and `imgGen.py`. The following sections describe how to request data from the `descGen.py` microservice, use that data to generate the associated image from the `imgGen.py` microservice, and includes a UML sequence diagram that illustrates the process.

## Requesting Data from descGen.py

### Prerequisites
- Python installed 
- RabbitMQ server running locally
- Python libraries utilized include: pika, tk from tkinter, and the wikipedia api

### Steps to Request Data
1. Clone or download the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the `descGen.py` script:

    ```bash
    python descGen.py
    ```

4. The GUI window will appear, allowing you to enter the name of any current or former United States President.
5. Click the "Get Description" button to request the description from Wikipedia.

Example Call using the President George Washington and the RabbitMQ server to request data from my microservice (descGen.py) and send it to my partner's microservice (imgGen.py): 

```python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='image_name_queue')
president_name = "George Washington"
channel.basic_publish(exchange='', routing_key='image_name_queue', body=president_name)
print(f"Requested description for {president_name}")
connection.close()
```

## Receiving Data (from descGen.py) with imgGen.py

### Prerequisites
- Python installed
- RabbitMQ server running locally
- Python libraries utilized include: pika, os, Image & ImageTk from PIL, and tk from tkinter
  
### Steps to Recieve Data
1. Open a new terminal window.
2. Navigate to the project directory.
3. Run the `imgGen.py` script:

    ```bash
    python imgGen.py
    ```

4. The `imgGen.py` script will start waiting for messages. To exit, press CTRL+C.

The `imgGen.py` microservice recieves the input name from `descGen.py` and displays the corresponding presidential portrait in the local image folder. And error message is sent back to be displayed in the GUI if the name does not have an associated image with it in the image folder.

## UML Sequence Diagram

Below is a UML sequence diagram illustrating the processes for requesting and receiving data:

![UMLSequenceDiagram](https://github.com/mfaks/CS361_Microservice/assets/91384685/e66e4b7a-981a-492c-a477-10b891a0be7e)
