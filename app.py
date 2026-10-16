import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage

# Import our custom tools from tools.py
from tools import verify_drug_batch, check_clinic_inventory, evaluate_patient_triage

# 1. Load Environment Variables
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY is missing from .env!")

# 2. Register Available Tools
tools_list = [verify_drug_batch, check_clinic_inventory, evaluate_patient_triage]
tools_map = {tool.name: tool for tool in tools_list}

# 3. Initialize Groq Model and Bind Tools
llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    groq_api_key=groq_key,
    temperature=0
).bind_tools(tools_list)


def run_bioguard_agent(user_query: str):
    """Executes the iterative agent loop with multi-tool capabilities."""
    messages = [
        ("system", "You are BioGuard AI, an expert autonomous assistant for rural clinical triage and drug verification. Always use available tools when factual clinic data, batch verification, or triage analysis is needed."),
        HumanMessage(content=user_query)
    ]

    print(f"\n==================================================")
    print(f"👤 USER QUERY: {user_query}")
    print(f"==================================================\n")
    print("🤖 Agent analyzing query...")

    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        ai_msg = llm.invoke(messages)
        messages.append(ai_msg)

        # Check if model generated tool calls
        if ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                tool_name = tool_call["name"]
                selected_tool = tools_map.get(tool_name)

                if selected_tool:
                    print(f"\n⚙️ EXECUTING TOOL [Step {iteration}]: '{tool_name}'")
                    print(f"   Arguments: {tool_call['args']}")

                    # Execute the tool
                    tool_output = selected_tool.invoke(tool_call['args'])
                    print(f"   Result: {tool_output}")

                    # Append tool response back to conversation memory
                    messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))
        else:
            # Model has gathered all data and produced the final text response
            print("\n🎉 BIOGUARD AI RESPONSE:")
            print(ai_msg.content)
            break


# --- Quick Test Execution ---
if __name__ == "__main__":
    test_query = "Please verify medicine batch BATCH-FAKE-009 and check if we have Amoxicillin in stock at the clinic."
    run_bioguard_agent(test_query)