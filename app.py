from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import os
import uuid  # For generating unique filenames

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to compare images using ORB feature matching
def are_images_duplicates(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        return False, "One or both images couldn't be loaded."

    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    # Create BFMatcher object based on Hamming distance (used with ORB)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort them in the order of their distances
    matches = sorted(matches, key=lambda x: x.distance)

    # Compute the matching score
    good_matches = [m for m in matches if m.distance < 50]

    # If a significant portion of the features match, they are duplicates or subparts
    match_percentage = len(good_matches) / min(len(kp1), len(kp2)) * 100

    # Set a threshold for considering them duplicates or subparts (adjust if necessary)
    threshold = 30.0  # e.g., 30% of features should match
    if match_percentage > threshold:
        return True, f"The images are duplicates or subparts (Match Percentage: {match_percentage:.2f}%)."
    else:
        return False, f"The images are not duplicates (Match Percentage: {match_percentage:.2f}%)."

@app.post("/compare")
async def compare(image1: UploadFile = File(...), image2: UploadFile = File(...)):
    # Generate unique filenames using UUID
    unique_filename1 = str(uuid.uuid4()) + "_" + image1.filename
    unique_filename2 = str(uuid.uuid4()) + "_" + image2.filename

    # Ensure the "temp" directory exists
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Save the images temporarily with unique filenames
    image1_path = os.path.join("temp", unique_filename1)
    image2_path = os.path.join("temp", unique_filename2)

    with open(image1_path, "wb") as f:
        f.write(await image1.read())
    with open(image2_path, "wb") as f:
        f.write(await image2.read())

    try:
        # Compare the images
        result, message = are_images_duplicates(image1_path, image2_path)
    finally:
        # Remove the temp images after comparison
        os.remove(image1_path)
        os.remove(image2_path)

    return JSONResponse(content={"result": result, "message": message})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
