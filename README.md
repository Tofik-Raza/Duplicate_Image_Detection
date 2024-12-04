# Image Comparison API

This is a FastAPI-based application for comparing two images to determine if they are duplicates or subparts of each other. It uses ORB feature matching to compare images.

## Features
- Upload two images via API.
- Compare the images and return whether they are duplicates or subparts.
- Temporary file storage and cleanup.

## Requirements
- Python 3.7 or later
- OpenCV
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
git clone <repository_url> cd <repository_directory>

markdown
Copy code

2. Install the required dependencies:
pip install -r requirements.txt

markdown
Copy code

3. Run the application:
uvicorn app:app --reload

markdown
Copy code

4. Access the API documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Usage

### Endpoint: `/compare`
- **Method:** POST
- **Description:** Compares two uploaded images.
- **Parameters:**
- `image1`: The first image file.
- `image2`: The second image file.
- **Response:**
- `result` (boolean): Whether the images are duplicates or subparts.
- `message` (string): A detailed message about the comparison.

### Example with `curl`:
curl -X POST "http://127.0.0.1:8000/compare" \ -F "image1=@path_to_image1.jpg" \ -F "image2=@path_to_image2.jpg"

markdown
Copy code

## Notes
- Temporary files are stored in the `temp` directory and are deleted after the comparison.
- Make sure to install OpenCV with Python bindings.

## Troubleshooting
If you encounter any issues:
1. Verify Python and OpenCV installation.
2. Check for missing dependencies and install them.
