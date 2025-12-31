# --------------------------------------------------------------
# 0️⃣  Install (run once)
# --------------------------------------------------------------
# pip install --upgrade "langchain[all]" "langchain-ollama"

# --------------------------------------------------------------
# 1️⃣ Imports – new core locations
# --------------------------------------------------------------

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.tracers import LangChainTracer
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
import json, re, asyncio, sys
from itertools import islice
from langsmith import Client


# --------------------------------------------------------------
# 2️⃣ Pydantic schema + parser
# --------------------------------------------------------------
class MovieInfo(BaseModel):
    """Information about the requested movie."""
    title: str = Field(..., description="Official title of the movie.")
    year: int = Field(..., description="Release year (e.g. 2008)")
    director: str = Field(..., description="Full name of the director")


pydantic_parser = PydanticOutputParser(pydantic_object=MovieInfo)

# --------------------------------------------------------------
# 3️⃣ Ollama chat model (JSON‑only mode)
# --------------------------------------------------------------
llm = ChatOllama(
    model="llama3.2:1b",  # any local Ollama model that supports JSON mode

    temperature=0.0,
    max_tokens=1024,
    # **Important** – tell Ollama to emit *pure* JSON, no markdown
    #   The underlying API accepts a `format="json"` kwarg.
    #   In the Python wrapper we pass it via `response_format`.
    response_format="json",  # <-- forces JSON output
)

# --------------------------------------------------------------
# 4️⃣ PromptTemplate – make the instruction crystal‑clear
# --------------------------------------------------------------
# The parser already gives us a block that says “return a JSON object …”.
# We add two more lines that explicitly forbid schema output and markdown.

template = """
Return ONLY valid JSON with EXACTLY these keys:
- title (string)
- year (integer)
- director (string)

Do NOT include schema, properties, descriptions, or extra text.

User question: {user_query}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["user_query"],
    partial_variables={"format_instructions": pydantic_parser.get_format_instructions()},
)


# --------------------------------------------------------------
# 5️⃣ Helper – safe parsing (fallback to regex if needed)
# --------------------------------------------------------------
def safe_parse(text: str) -> MovieInfo:
    """
    Tries the normal Pydantic parser.
    If it fails, extracts the first JSON block with a regex
    and parses that raw dict.
    """
    try:
        return pydantic_parser.invoke(text)
    except Exception as exc:
        # ------------------------------------------------------
        # 5️⃣a  Grab the *first* {...} block (handles markdown fences)
        # ------------------------------------------------------
        json_match = re.search(r"\{[\s\S]*?\}", text)
        if not json_match:
            raise RuntimeError(f"Unable to find JSON in LLM output: {text}") from exc

        candidate = json_match.group(0)
        try:
            data = json.loads(candidate)
            return MovieInfo(**data)
        except Exception as inner:
            raise RuntimeError(
                f"Could not build MovieInfo from extracted JSON: {candidate}"
            ) from inner


# --------------------------------------------------------------
# 6️⃣ METHOD 1 – Classic (prompt → LLM → parse)
# --------------------------------------------------------------
def classic_flow():
    print("\n--- Classic string‑then‑parse flow ---")
    full_prompt = prompt.invoke({"user_query": "What is Iron Man's first movie, year and director?"})
    print("[Prompt sent to Ollama]")
    print(full_prompt)

    # Ollama wrapper accepts a plain string and automatically wraps it into a user message.
    raw_output = llm.invoke(full_prompt).content
    print("\n[Raw LLM output]")
    print(raw_output)
    # movie = pydantic_parser.parse(raw_output)
    movie = safe_parse(raw_output)
    print("\n[Parsed MovieInfo]")
    print(movie)
    print("title:", movie.title, "year:", movie.year, "director:", movie.director)


# --------------------------------------------------------------
# 7️⃣ METHOD 2 – Runnable pipeline (sync + async)
# --------------------------------------------------------------
def runnable_flow():
    print("\n--- Runnable pipeline (sync) ---")
    pipeline = (
            prompt
            | llm
            | StrOutputParser()  # converts AIMessage → plain string
            | RunnableLambda(safe_parse)  # safe_parse returns a MovieInfo
    )

    # optional tracing – prints a tiny tree to stdout
    pipeline = pipeline.with_config(callbacks=[LangChainTracer()])

    result_sync = pipeline.invoke(
        {"user_query": "What is Iron Man's first movie called?"}
    )
    print("\nResult (sync):", result_sync)

    async def async_part():
        result_async = await pipeline.ainvoke(
            {"user_query": "What is Iron Man's first movie called?"}
        )
        print("\nResult (async):", result_async)

    asyncio.run(async_part())


# --------------------------------------------------------------
# 8️⃣ METHOD 3 – Streaming + manual parse
# --------------------------------------------------------------
def streaming_flow():
    print("\n--- Streaming flow (token‑by‑token) ---")

    # Build the prompt string first (the Ollama model expects a string)
    prompt_str = prompt.invoke({"user_query": "What is Iron Man's first movie called?"})
    token_stream = llm.stream(prompt_str)

    collected = ""
    print("[Streaming output]")
    for chunk in token_stream:
        txt = chunk.content
        print(txt, end="", flush=True)  # live display
        collected += txt
    print("\n--- end of stream ---")

    # Parse the final collected text
    movie = safe_parse(collected)
    print("\nParsed after streaming:")
    print(movie)


# --------------------------------------------------------------
# 9️⃣ Run everything
# --------------------------------------------------------------
if __name__ == "__main__":
    # 1️⃣ Classic
    classic_flow()
    print("classic_flow completed.")

    # 2️⃣ Runnable pipeline
    runnable_flow()
    print("runnable_flow completed.")

    # 3️⃣ Streaming
    streaming_flow()
    print("streaming_flow completed.")

