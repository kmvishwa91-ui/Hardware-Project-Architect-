import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

app = FastAPI(title="Hardware Architect API", version="1.0")

# Request Model
class HardwareRequest(BaseModel):
    project_idea: str
    microcontroller: str
    experience_level: str

# Setup LangChain LLM Pipeline
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3, # Low temperature for accurate pinouts and code
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create the prompt template
system_prompt = """
You are an Expert Hardware Project Architect and Electronics Engineer.
Your task is to design a complete hardware prototype plan for the following project: {project_idea}.
The user prefers using the {microcontroller} platform and has an experience level of: {experience_level}.

Format your response exactly with these markdown headings:

### ⚙️ System Overview
[Briefly explain how the system will work and the logic flow]

### 📦 Bill of Materials (BOM)
[Bullet list of required components (e.g., sensors, motor drivers, resistors, power supply)]

### 🔌 Wiring & Pin Connections
[A clear text-based schematic/table explaining what connects to which pin]

### 💻 Starter Code
[Provide the base code (e.g., C++ for Arduino, Python for Raspberry Pi) to initialize the components and run a basic test. Use code blocks.]
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "Please architect this hardware project.")
])

# Build the chain
architect_chain = prompt | llm | StrOutputParser()

@app.post("/architect-project")
async def architect_project(request: HardwareRequest):
    try:
        # Invoke the LangChain pipeline
        result = architect_chain.invoke({
            "project_idea": request.project_idea,
            "microcontroller": request.microcontroller,
            "experience_level": request.experience_level
        })
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the server:
# uvicorn main:app --reload --port 8000
