import io
import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse, JSONResponse
import numpy as np
from PIL import Image
from datetime import datetime
from predictor import cars_predictor

app = FastAPI(title="Car Detection API", description="API for detecting objects in the streets and similar scenarios.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Car Detection API"}

@app.get("/status", response_class=PlainTextResponse)
def get_status():
    service_info = "Car Detection API Status:\n"
    model_info = "Model Information:\n"
    service_info += "Service is running smoothly.\n"
    model_info += "Object Detection Model: CarsPredictor\n"
    model_info += "Model Path: {}\n".format(cars_predictor.model_path)

    return service_info + model_info

@app.post("/predict", responses={200: {"content": {"image/jpeg": {}}}})
def predict(file: UploadFile = File(...)):
    try:
        img_array = process_image(file)
        prediction_data = cars_predictor.predict_image(img_array)

        for detection in prediction_data["object_detection_result"].detections:
            bbox = detection.bounding_box
            cv2.rectangle(
                img_array,
                (int(bbox.origin_x), int(bbox.origin_y)),
                (int(bbox.origin_x + bbox.width), int(bbox.origin_y + bbox.height)),
                (0, 255, 0),
                2
            )

        img_pil = Image.fromarray(img_array)
        image_stream = io.BytesIO()
        img_pil.save(image_stream, format="JPEG")
        image_stream.seek(0)

        return StreamingResponse(content=image_stream, media_type="image/jpeg")
    except HTTPException as e:
        return e

def process_image(file):
    try:
        img_stream = io.BytesIO(file.file.read())
        if file.content_type.split("/")[0] != "image":
            raise HTTPException(
                status_code=415, detail="Not an image"
            )
        img_obj = Image.open(img_stream)
        img_obj = img_obj.convert("RGB")

        img_array = np.array(img_obj)
        return img_array
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing image: {str(e)}"
        )

@app.get("/reports", responses={200: {"content": {"application/json": {}}}})
def generate_reports():
    try:
        file_name = "example_image.jpg"  
        image_size = "100x100" 
        date_time = datetime.now().strftime("%a,%d %b %Y %H:%M:%S GMT")
        server_info = "uvicorn" 
        transfer_encoding = "chunked"  

        response_data = {
            "content-type": "image/jpeg",
            "date": date_time,
            "server": server_info,
            "transfer-encoding": transfer_encoding
        }

        csv_content = f"{file_name},{image_size},{date_time},{server_info},{transfer_encoding}\n"

        with open("Destacados.csv", "a") as csv_file:
            csv_file.write(csv_content)

        return JSONResponse(content=response_data)
    except HTTPException as e:
        return e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
