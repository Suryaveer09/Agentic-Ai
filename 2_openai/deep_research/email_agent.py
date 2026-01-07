import os
from typing import Dict

import resend
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body using Resend."""
    resend.api_key = os.environ.get("RESEND_API_KEY")

    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",      # must be a verified sender/domain in Resend
        "to": ["leelasaisvp@gmail.com"],      # list or string
        "subject": subject,
        "html": html_body,
        # Optional:
        # "text": "Plain-text fallback",
        # "reply_to": "support@yourdomain.com",
        # "cc": ["..."],
        # "bcc": ["..."],
    }

    result = resend.Emails.send(params)
    # result typically includes an email id, e.g. {"id": "..."}
    print("Resend response:", result)

    return {"status": "success", "id": result.get("id", "")}


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
