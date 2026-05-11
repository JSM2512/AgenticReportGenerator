import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import Annotated, List
from pydantic import BaseModel, Field
from typing import TypedDict
from langgraph.types import Send
import operator

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.1-8b-instant")

class Section(BaseModel):
    name: str = Field(description="The name of the section of report")
    description: str = Field(description="A brief overview of the main topics and concepts of the section")

class Sections(BaseModel):
    sections: List[Section] = Field(description="A list of sections in the report")

planner = llm.with_structured_output(Sections)

# graph state
# graph state
class State(TypedDict):
    topic:str
    sections:list[Section]
    completed_sections: Annotated[list, operator.add] # all workers will write to this key in parallel
    final_report:str

# worker state
class WorkerState(TypedDict):
    section:Section
    completed_sections: Annotated[list, operator.add] 


def orchestrator(state: State):
    """orchestrator that generates a plan for the report"""

    # generate queries
    report_sections = planner.invoke(
        [
            SystemMessage(content="""
                Generate a structured plan for a report on the following topic. The plan should include the main sections of the report, along with a brief description of what each section will cover.

                    STRICT RULES:
                    - Output must be plain text paragraph(s)
                    - No meta commentary
                    - No reasoning
                    - No first-person language
                    - No conversational tone

                        Begin immediately with the section title as a heading, then content."""),
            HumanMessage(content=f"here is the report topic{state['topic']}")
        ]
    )


    return {"sections": report_sections.sections}

def llm_call(state:WorkerState):
    """worker writes a section of the report"""

    # generate content for the section
    section = llm.invoke(
        [
            SystemMessage(content="""
                write a report section based on the following name and description.Include no preamble or your thinking, just the content of the section.

                    STRICT RULES:
                    - Output must be plain text paragraph(s)
                    - No meta commentary
                    - No reasoning
                    - No first-person language
                    - No conversational tone

                        Begin immediately with the section title as a heading, then content."""),
            HumanMessage(content=f"here is the section details, name: {state['section'].name} and description: {state['section'].description}")
        ]
    )

    # print("section content", section.content)

    return {"completed_sections": [section.content]}



# conditional edge function to create llm_call workers that each write a section of a report
def assign_workers(state:State):
    """assign workers to write sections in parallel"""

    # kick off sections in parallel via SendAPI
    return [Send("llm_call", {"section":s}) for s in state["sections"]]


def synthesizer(state:State):
    """synthesizer that combines the completed sections into a final report"""

    completed_sections = state["completed_sections"]
    # combine sections into final report
    final_report = "\n\n---\n\n".join(completed_sections)

    # final = llm.invoke("kindly remove the thinking part of the sections and generate a formal report from the content of the sections. The report should be well-structured, coherent, and suitable for a professional audience. Ensure that the final report is polished and free of any informal language or meta commentary. CONTENT : "+final_report)

    return {"final_report": final_report}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("orchestrator", orchestrator)
    builder.add_node("llm_call", llm_call)
    builder.add_node("synthesizer", synthesizer)
    builder.add_edge(START, "orchestrator")
    builder.add_conditional_edges("orchestrator", assign_workers, ["llm_call"])
    builder.add_edge("llm_call", "synthesizer")
    builder.add_edge("synthesizer", END)
    return builder.compile()