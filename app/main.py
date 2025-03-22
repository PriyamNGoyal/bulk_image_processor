import uuid
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header, Response
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Product
from .tasks import process_images
import os
from dotenv import load_dotenv
import csv
from io import StringIO

load_dotenv()
AUTH_BEARER_TOKEN = os.getenv("AUTH_BEARER_TOKEN")

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization != f"Bearer {AUTH_BEARER_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        df = pd.read_csv(file.file)
        required_columns = ["Sr No.", "Product Name", "Image URLs"]
        for column in required_columns:
            if column not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing required column: {column}")
        errors = []
        for index, row in df.iterrows():
            if pd.isna(row["Product Name"]) or row["Product Name"] == "":
                errors.append(f"Row {index+1}: Missing 'Product Name'")

            if pd.isna(row["Image URLs"]) or row["Image URLs"] == "":
                errors.append(f"Row {index+1}: Missing 'Image URLs'")
        if errors:
            raise HTTPException(status_code=400, detail="CSV Validation Errors: " + "; ".join(errors))
        request_id = str(uuid.uuid4())
        for _, row in df.iterrows():
            product_name = row["Product Name"]
            image_urls = row["Image URLs"].split(",")
            db_product = Product(
                id=str(uuid.uuid4()),
                request_id=request_id,
                product_name=product_name,
                original_urls=image_urls,
                status="processing"
            )
            db.add(db_product)
            process_images.delay(request_id, product_name, image_urls)
        db.commit()
        return {"request_id": request_id, "message": "Processing started"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/status/{request_id}")
def check_status(request_id: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.request_id == request_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="Request ID not found")
    
    # Check if all products are completed
    statuses = [p.status for p in products]
    
    # If all statuses are completed, generate a CSV
    if all(status == "completed" for status in statuses):
        output = StringIO()
        writer = csv.writer(output, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write CSV header
        writer.writerow(["srno", "Product_Name", "Input Image Urls", "Output Image Urls"])
        
        # Write each product's data into the CSV
        for index, product in enumerate(products, start=1):
            input_urls = ", ".join(product.original_urls)
            output_urls = ", ".join(product.compressed_urls)
            writer.writerow([index, product.product_name, input_urls, output_urls])
        
        # Move to the beginning of the StringIO object for reading
        output.seek(0)
        
        # Return CSV as a downloadable file
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=status_{request_id}.csv"}
        )
    
    # If not all products are completed, just return the status
    return {"request_id": request_id, "status": statuses}

@app.get("/products/{product_name}")
def get_product(product_name: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_name == product_name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "product_name": product.product_name,
        "original_urls": product.original_urls,
        "compressed_urls": product.compressed_urls,
        "status": product.status
    }
