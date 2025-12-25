"""FeedBack Management"""
import re
import psycopg2
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import FastAPI, HTTPException

def get_db_connection():
    """"DbConnection"""
    return psycopg2.connect(
        "postgresql://postgres:Papai12#@localhost:5432/postgres"
    )


QUERY = """
        CREATE TABLE IF NOT EXISTS user_feedback
        (
            feedback_id       SERIAL PRIMARY KEY,
            user_name         TEXT NOT NULL,
            email_id          TEXT NOT NULL,
            age               INTEGER CHECK (age > 0),
            phone_number      VARCHAR(15),
            rating            INTEGER CHECK (rating BETWEEN 1 AND 10),
            feedback_comments TEXT,
            created_date      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ); \
        """
con = get_db_connection()
cur = con.cursor()
cur.execute(QUERY)
con.commit()
con.close()
print("Table created successfully")

tags_metadata = [
    {
        "name": "Feedback",
        "description": "Operations related to user feedback"
    }
]

app = FastAPI(
    title="Feedback Management API",
    description="APIs to create, view, update and delete user feedback",
    version="26.6.0",
    openapi_tags=tags_metadata,
    docs_url="/ronish",
)


class Feedback(BaseModel):
    """Request for Feedback"""
    user_name: str
    email_id: EmailStr
    age: int
    phone_number: str
    rating: int
    feedback_comments: str

    @field_validator('age')
    @classmethod
    def age_must_be_positive(cls, v):
        """Validation of age"""
        if v <= 0:
            raise ValueError("Age must be a positive number")
        return v

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v):
        """Validation of rating"""
        if not 1 <= v <= 10:
            raise ValueError("Rating must be between 1 and 10")
        return v

    @field_validator("feedback_comments")
    @classmethod
    def comment_length(cls, v):
        """Validation of feedback comments"""
        if len(v) > 35:
            raise ValueError("Comments length must be <= 35")
        return v

    @field_validator("user_name")
    @classmethod
    def validate_name(cls, v):
        """Validation of User"""
        if not re.fullmatch(r"[A-Za-z ]+", v):
            raise ValueError("User Name must contain only alphabets and spaces")
        return v


class FeedbackCommentUpdate(BaseModel):
    """Request to update the Feedback"""
    feedback_comments: str

    @field_validator("feedback_comments")
    @classmethod
    def comment_length(cls, v):
        """Validation of comments for updating the comment"""
        if len(v) > 35:
            raise ValueError("Comments length must be <= 35")
        return v


@app.post("/feedback/add", tags=["Feedback"])
def add_feedback(feed: Feedback):
    """API to add the Feedback Details"""
    user_name = feed.user_name
    email_id = feed.email_id
    age = feed.age
    phone_number = feed.phone_number
    rating = feed.rating
    comments = feed.feedback_comments
    conn = None
    cursor = None

    if not feed.phone_number.isdigit() or len(feed.phone_number) != 10:
        raise HTTPException(status_code=460, detail="Phone number must be exactly 10 digits")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = """
                       INSERT INTO user_feedback(user_name, email_id, age, phone_number, rating, feedback_comments)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       RETURNING
                           feedback_id, user_name, email_id, age, phone_number, rating,
                           feedback_comments, created_date, updated_date; \
                       """

        cursor.execute(
            insert_query,
            (
                user_name,
                email_id,
                age,
                phone_number,
                rating,
                comments
            )
        )

        inserted_row = cursor.fetchone()
        conn.commit()

        return {
            "feedback_id": inserted_row[0],
            "user_name": inserted_row[1],
            "email": inserted_row[2],
            "age": inserted_row[3],
            "phone_number": inserted_row[4],
            "rating": inserted_row[5],
            "feedback_comments": inserted_row[6],
            "created_date": inserted_row[7],
            "updated_date": inserted_row[8],
            "code":200,
            "status": "Feedback created Successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.get("/feedback/getAll", tags=["Feedback"])
def get_all_feedback():
    """API to get all the Feedback Details"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
                select *
                from user_feedback \
                """
        cursor.execute(query)
        feedback = cursor.fetchall()

        result = []
        for row in feedback:
            result.append({
                "feedback_id": row[0],
                "user_name": row[1],
                "email": row[2],
                "age": row[3],
                "phone_number": row[4],
                "rating": row[5],
                "feedback_comments": row[6],
                "created_date": row[7],
                "updated_date": row[8],
            })

        return {
            "message": "Get all the Feedback",
            "code": 200,
            "count": len(result),
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.get("/feedback/{feedback_id}", tags=["Feedback"])
def get_feedback(feedback_id: int):
    """API to get the Feedback details using feedback id"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
                SELECT *
                from user_feedback
                WHERE feedback_id = %s
                ; \
                """
        cursor.execute(query, (feedback_id,))
        feedback = cursor.fetchone()

        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback Not Found")

        return {
            "status": "Feedback fetched Successfully",
            "user_name": feedback[1],
            "email": feedback[2],
            "age": feedback[3],
            "phone_number": feedback[4],
            "rating": feedback[5],
            "feedback_comments": feedback[6],
            "created_date": feedback[7],
            "updated_date": feedback[8],
            "code": 200
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.patch("/feedback/comment/{feedback_id}", tags=["Feedback"])
def update_feedback_comment(feedback_id: int, data: FeedbackCommentUpdate):
    """API to update the Feedback using feedback id"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
                SELECT feedback_comments,user_name
                from user_feedback
                WHERE feedback_id = %s; \
                """
        cursor.execute(query, (feedback_id,))
        feedback = cursor.fetchone()
        if feedback is None:
            raise HTTPException(status_code=404, detail="Feedback not found")

        update_query = """
                   UPDATE user_feedback
                   SET feedback_comments = %s, updated_date = CURRENT_TIMESTAMP
                   where feedback_id = %s; \
                   """
        cursor.execute(update_query, (data.feedback_comments, feedback_id))
        conn.commit()
        return {
            "status": "Feedback Updated Successfully",
            "user_name": feedback[1],
            "old Feedback": feedback[0],
            "new Feedback": data.feedback_comments,
            "code": 200
         }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.delete("/feedback/remove/{feedback_id}", tags=["Feedback"])
def delete_feedback(feedback_id: int):
    """Delete the Feedback"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
                DELETE
                from user_feedback
                WHERE feedback_id = %s; \
                """
        cursor.execute(query, (feedback_id,))
        conn.commit()
        record = cursor.rowcount

        if record == 0:
            raise HTTPException(status_code=404, detail="Feedback not found")

        return {
            "status": "Feedback deleted Successfully",
            "record": record,
            "code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()