import gradio as gr
from environment import EmailTriageEnv
from models import Action, Classification

env = EmailTriageEnv()

def classify_email(task_difficulty, email_text):
    try:
        obs = env.reset(task=task_difficulty.lower())
        
        # Create action for all emails
        action = Action(
            classification={i: Classification.medium for i in range(len(obs.emails))},
            response={},
            priority_order=list(range(len(obs.emails)))
        )
        
        obs, reward, done, info = env.step(action)
        
        result = f"📧 Email Triage Results\n\n"
        result += f"Task: {obs.current_task}\n"
        result += f"Progress: {obs.task_progress}\n\n"
        result += f"Score: {reward.score:.2f}\n"
        result += f"Feedback: {reward.feedback}\n\n"
        result += f"Emails processed: {len(obs.emails)}\n\n"
        
        for email in obs.emails[:3]:
            result += f"📨 Email #{email.id}\n"
            result += f"From: {email.sender}\n"
            result += f"Subject: {email.subject}\n"
            result += f"Body: {email.body[:100]}...\n\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=classify_email,
    inputs=[
        gr.Dropdown(["Easy", "Medium", "Hard"], label="Task Difficulty", value="Easy"),
        gr.Textbox(label="Additional Context (optional)", placeholder="Enter any additional context...")
    ],
    outputs=gr.Textbox(label="Triage Results", lines=20),
    title="📧 Email Triage System",
    description="AI-powered email classification and prioritization system"
)

if __name__ == "__main__":
    demo.launch()
