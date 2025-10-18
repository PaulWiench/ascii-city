import mangum

from src.main import app


lambda_handler = mangum.Mangum(app)
