# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routes import calculate_router

# # Initialize FastAPI
# app = FastAPI()

# # Allow all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Include routes
# app.include_router(calculate_router)

# # Root endpoint
# @app.get("/")
# def root():
#     return {"message": "Delivery Cost Calculator API"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import calculate_router  # Ensure this is defined in your routes.py file
import logging

# Initialize FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Allow all origins (CORS configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routes
app.include_router(calculate_router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Delivery Cost Calculator API is running."}

# Startup event
@app.on_event("startup")
async def startup_event():
    logging.info("Application has started successfully.")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application is shutting down.")

# For local development or debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
