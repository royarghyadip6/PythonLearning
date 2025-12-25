import langchain_core as lc
from pydantic.v1.fields import FieldInfo as FieldInfoV1
def create_prompt_template():
    """Create a prompt template for LangChain"""
    template = """You are a helpful assistant that translates {input_language} to {output_language}.

    {input_language}: {text}

    {output_language}:"""
    prompt = lc.PromptTemplate()
    return prompt

if __name__ == "__main__":
    prompt_template = create_prompt_template()
    print("abc : ", prompt_template)
    #     """
#     return {"message": "Feedback created successfully"}
#     def username_length(cls, v):
#         """Validation of user name"""
#         if len(v) < 3 or len(v) > 20:
#             raise ValueError("User name length must be between 3 and 20 characters")
#         return v
#
# @app.post("/feedback/", tags=["Feedback"])
# def create_feedback(feedback: Feedback):
#     """Create a new feedback entry with the provided feedback data"""
#     con = get_db_connection()
#     cur = con.cursor()
#     insert_query = """INSERT INTO feedback (user_name, email_id, age, phone_number, rating, feedback_comments)
#     VALUES (%s, %s, %s, %s, %s, %s) RETURNING feedback_id;"""
#     cur.execute(insert_query, (
#         feedback.user_name,
#         feedback.email_id,
#         feedback.age,
#         feedback.phone_number,
#         feedback.rating,
#         feedback.feedback_comments
#     ))
#     feedback_id = cur.fetchone()[0]
#     con.commit()
#     close_db_cursor_connection(cur, con)
#     return {"feedback_id": feedback_id, "message": "Feedback created successfully"}
#
# @app.put("/feedback/{feedback_id}", tags=["Feedback"])
# def update_feedback(feedback_id: int, feedback: Feedback):
#     """Update an existing feedback entry by its ID"""
#     con = get_db_connection()
#     cur = con.cursor()
#     update_query = """UPDATE feedback SET user_name=%s, email_id=%s, age=%s, phone_number=%s, rating=%s, feedback_comments=%s
#     WHERE feedback_id=%s;"""
#     cur.execute(update_query, (
#         feedback.user_name,
#         feedback.email_id,
#         feedback.age,
#         feedback.phone_number,
#         feedback.rating,
#         feedback.feedback_comments,
#         feedback_id
#     ))
#     con.commit()
#     close_db_cursor_connection(cur, con)
#     return {"feedback_id": feedback_id, "message": "Feedback updated successfully"}
