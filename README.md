## How to build an launch the app with Flask
First install all the dependencies
    ```bash
    python pip install -r requirements.txt
    
Then run it
    ```bash
    flask run --port 8888

## How to build an launch the app with Docker
First we build the image
    ```bash
    docker build -t powerplant .

Then run it
    ```bash
    docker run -p 8888:8888 -w powerplant

    ```bash
    http://localhost:8888/productionplan