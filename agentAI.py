import os
from browser_use.agent.service import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
import asyncio
import time

async def SiteValidation():
    """Run end-to-end UI validation using Gemini-powered agent"""

    # Set your Google Gemini API key securely (consider using an environment variable or secret manager)
    os.environ["Gemini_api_key"] = "AIzaSyBMwKJoyggPEMdndpCOQMZMEt17SBOKEoI"
    api_key = os.environ["Gemini_api_key"]

    # Define actionable and granular task instructions for the agent
    task = (
        "You are an expert UI automation agent testing an e-commerce flow.",
        "1. Navigate to https://rahulshettyacademy.com/loginpagePractise/",
        "2. Enter username 'rahulshettyacademy' and password 'learning' and click the login button.",
        "3. Wait for login to complete and redirect.",
        "4. Click the 'Add' button for the first product iphone X and samsung note 8 listed on the page .",
        "5. Click the checkout button and store the total price displayed."
        "6. On checkout Page verify the total amount displayed and click on checkout button"
        "7. On confirmation page verify the order number and click on purchase button"
        "8. On success page verify the message displayed and click on close button"

    )

    # Initialize the LLM (Google Gemini) for agent decision making
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=SecretStr(api_key)
    )

    # Create the agent
    agent_instance = Agent(task, llm, use_vision=True)  # Ensure agent uses vision capabilities

    start_time = time.time()  # Start time for timeout monitoring
    timeout = 300  # 5-minute timeout (adjust as needed)

    try:
        # Run the agent and monitor time
        history = await agent_instance.run()

        # Check for timeout
        if time.time() - start_time > timeout:
            raise TimeoutError("Task took too long, exiting...")

        # Print the output summary of the task execution
        print("\n✅ Automation complete. Task history:")
        print(history)

    except TimeoutError as e:
        print(f"❌ Error: {str(e)}")
        # Handle the timeout by logging or stopping further execution

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        # Handle any other exceptions that may arise

if __name__ == "__main__":
    asyncio.run(SiteValidation())
