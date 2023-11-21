import io
import cv2
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
import numpy as np
from PIL import Image
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
    
def get_prediction(file: UploadFile = File(...)):
    try:
        img_array = process_image(file)
        prediction_data = cars_predictor.predict_image(img_array)
        return prediction_data
    except HTTPException as e:
        return e

@app.get("/reports", responses={200: {"content": {"text/csv": {}}}})
def generate_reports(file: UploadFile = File(...)):
    try:

        img_array = process_image(file)
        prediction_data = cars_predictor.predict_image(img_array)

        file_name = file.filename
        image_size = f"{prediction_data['image'].shape[1]}x{prediction_data['image'].shape[0]}"
        prediction_class = prediction_data["object_detection_result"].detections[0].class_name
        confidence = prediction_data["object_detection_result"].detections[0].confidence
        prediction_time = prediction_data["object_detection_result"].inference_time
        execution_time = prediction_data["execution_time"]
        model_used = "CarsPredictor"

        csv_content = f"{file_name},{image_size},{prediction_class},{confidence},{prediction_time},{execution_time},{model_used}\n"

        with open("Detectados.csv", "a") as csv_file:
            csv_file.write(csv_content)

        response_content = f"file_name,image_size,prediction,confidence,prediction_time,execution_time,model\n{csv_content}"
        return StreamingResponse(content=response_content, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=reports.csv"})
    except HTTPException as e:
        return e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
