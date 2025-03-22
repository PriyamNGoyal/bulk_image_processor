import requests
import uuid
from PIL import Image
from io import BytesIO
from sqlalchemy.orm import Session
from .celery_config import celery_app  # Importing after celery_app initialization
from .database import SessionLocal
from .models import Product
from .s3_utils import upload_to_s3

@celery_app.task
def process_images(request_id, product_name, image_urls):
    print("process_images tasks is triggered.")
    compressed_urls = []
    session: Session = SessionLocal()

    for url in image_urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise error for bad response
            
            img = Image.open(BytesIO(response.content))
            img = img.convert("RGB")
            img.thumbnail((500, 500))

            output = BytesIO()
            img.save(output, format="JPEG", quality=85)
            compressed_image = output.getvalue()

            filename = f"{uuid.uuid4()}.jpg"
            s3_url = upload_to_s3(compressed_image, filename)
            compressed_urls.append(s3_url)

        except Exception as e:
            print(f"Error processing {url}: {e}")

    product = session.query(Product).filter(Product.request_id == request_id, Product.product_name == product_name).first()
    if product:
        product.compressed_urls = compressed_urls
        product.status = "completed" if compressed_urls else "failed"
        session.commit()
    
    session.close()
