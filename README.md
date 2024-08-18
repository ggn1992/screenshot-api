# Screenshot API

Screenshot API is a FastAPI-based service that allows you to capture screenshots of websites programmatically. It offers various customization options, including format, delay, viewport size, full-page capture, mobile simulation, user-agent customization, and the ability to inject custom JavaScript. It's also available using Docker.

**Request URL**

```http://127.0.0.1:8000/screenshot?url=http://127.0.0.1:8000/docs&format=png&width=1920&height=1080&full_page=true&mobile=false&delay=2```

**Server response**

![Screenshot](https://github.com/ggn1992/screenshot-api/blob/main/screenshot.png?raw=true)

## Features

- Capture screenshots in PNG or Base64 format.
- Customize viewport dimensions and simulate mobile devices.
- Inject custom JavaScript before capturing the screenshot.
- Capture full-page screenshots.
- Customize the user-agent string for requests.
- Built-in, interactive API documentation with Swagger and ReDoc.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/screenshot-api
    ```
2.  Navigate to the project directory and create a virtual environment:
    ```bash
    cd screenshot-api
    python3 -m venv venv
    ```
3.  Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
4.  Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
## Usage

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

Or use Docker:

```bash
docker-compose up --build
```

The endpoint of the API is available at http://127.0.0.1:8000/screenshot.

### Accessing API Documentation

- Swagger UI: http://127.0.0.1:8000/docs - Interactive API documentation.
- ReDoc: http://127.0.0.1:8000/redoc - Alternative API documentation.

## Contributing

Contributions are welcome! If you would like to improve this project, please fork the repository and submit a pull request. For major changes, please open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License.