"""
Docstring for Asignment_Day_2_3_4.arg_feedback_assignment
"""

import fastapi

app = fastapi.FastAPI()

@app.put("/feedback/{feedback_id}")

@app.post("/feedback/")
def create_feedback(feedback: dict):
    """Create a new feedback entry with the provided feedback data
    """
    