import gradio as gr
import os
from transformers import pipeline

# Initialize zero-shot classification model
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except:
    classifier = None

def classify_single_email(email_text):
    """Classify a single email using improved rule-based system"""
    if not email_text or not email_text.strip():
        return "⚠️ Please enter email content to classify"
    
    email_lower = email_text.lower()
    
    # Enhanced keyword detection with weights
    score = 0
    reasons = []
    detected_category = None
    
    # HIGH PRIORITY keywords (score +3 each)
    high_keywords = {
        "urgent": 3, "asap": 3, "immediately": 3, "critical": 3, 
        "emergency": 3, "refund": 3, "complaint": 3, "bug": 3,
        "error": 3, "security": 3, "breach": 3, "down": 3,
        "not working": 3, "fix": 2, "problem": 2, "issue": 2
    }
    
    # MEDIUM PRIORITY keywords (score +1 each)
    medium_keywords = {
        "meeting": 1, "schedule": 1, "report": 1, "update": 1,
        "review": 1, "question": 1, "request": 1, "follow up": 1,
        "reminder": 1, "submit": 1, "deadline": 1, "attend": 1,
        "discuss": 1, "call": 1, "appointment": 1
    }
    
    # LOW PRIORITY keywords (score -2 each, stronger negative weight)
    low_keywords = {
        "newsletter": -2, "subscribe": -2, "offer": -2, "promotion": -2,
        "deal": -2, "sale": -2, "discount": -2, "unsubscribe": -2,
        "marketing": -2, "advertisement": -2, "win": -2, "free": -2,
        "congratulations": -2, "prize": -2, "special offer": -3,
        "limited time": -2, "exclusive": -2, "check out": -2,
        "latest updates": -2, "articles": -2, "weekend": -2
    }
    
    # Check HIGH priority keywords first
    for keyword, weight in high_keywords.items():
        if keyword in email_lower:
            score += weight
            reasons.append(f"HIGH: '{keyword}'")
            detected_category = "HIGH"
    
    # Check LOW priority keywords (these should override medium if present)
    low_score = 0
    for keyword, weight in low_keywords.items():
        if keyword in email_lower:
            low_score += weight
            reasons.append(f"LOW: '{keyword}'")
            if detected_category != "HIGH":
                detected_category = "LOW"
    
    # Check MEDIUM priority keywords only if no LOW keywords found
    if low_score == 0:
        for keyword, weight in medium_keywords.items():
            if keyword in email_lower:
                score += weight
                reasons.append(f"MEDIUM: '{keyword}'")
                if detected_category != "HIGH":
                    detected_category = "MEDIUM"
    else:
        score += low_score
    
    # Determine final priority with improved logic
    if detected_category == "LOW" or score < 0:
        priority = "🟢 LOW PRIORITY"
        action = "📋 Review when convenient (Informational/Marketing)"
        priority_level = "LOW"
    elif score >= 3 or detected_category == "HIGH":
        priority = "🔴 HIGH PRIORITY"
        action = "⚡ Respond immediately (Urgent/Critical)"
        priority_level = "HIGH"
    elif score >= 1 or detected_category == "MEDIUM":
        priority = "🟡 MEDIUM PRIORITY"
        action = "📅 Respond within 24 hours (Work/Normal Tasks)"
        priority_level = "MEDIUM"
    else:
        # Default to LOW if no clear indicators
        priority = "🟢 LOW PRIORITY"
        action = "📋 Review when convenient (No urgent indicators)"
        priority_level = "LOW"
    
    # Generate response
    result = f"""
📧 EMAIL CLASSIFICATION RESULT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Your Email:
{email_text[:200]}{'...' if len(email_text) > 200 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Classification: {priority}
📊 Priority Score: {score}

💡 Analysis:
"""
    
    if reasons:
        result += f"\n  Detected Keywords:\n"
        for reason in reasons[:5]:
            result += f"  • {reason}\n"
    else:
        result += "\n  • No specific keywords detected\n"
        result += "  • Classified as LOW priority by default\n"
    
    result += f"\n✅ Recommended Action:\n  {action}\n"
    result += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    return result

def classify_multiple_emails(emails_text):
    """Classify multiple emails separated by lines"""
    if not emails_text or not emails_text.strip():
        return "⚠️ Please enter email content to classify"
    
    # Split by double newlines
    emails = [e.strip() for e in emails_text.split('\n\n') if e.strip()]
    
    if len(emails) == 1:
        return classify_single_email(emails[0])
    
    result = f"📧 BATCH EMAIL CLASSIFICATION\n"
    result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    result += f"Total Emails: {len(emails)}\n\n"
    
    high_count = 0
    medium_count = 0
    low_count = 0
    
    for i, email in enumerate(emails[:10], 1):
        classification = classify_single_email(email)
        
        if "🔴 HIGH PRIORITY" in classification:
            high_count += 1
            priority = "🔴 HIGH"
        elif "🟡 MEDIUM PRIORITY" in classification:
            medium_count += 1
            priority = "🟡 MEDIUM"
        else:
            low_count += 1
            priority = "🟢 LOW"
        
        result += f"\n📨 Email #{i}: {priority}\n"
        result += f"Preview: {email[:80]}...\n"
    
    result += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    result += f"\n📊 SUMMARY:\n"
    result += f"  🔴 High Priority: {high_count}\n"
    result += f"  🟡 Medium Priority: {medium_count}\n"
    result += f"  🟢 Low Priority: {low_count}\n"
    
    return result

# Example emails for users to try
examples = [
    ["Subject: Weekly Newsletter\nCheck out our latest updates and articles."],
    ["Subject: Special Offer\nGet 20% discount on all items this weekend."],
    ["Subject: Meeting Reminder\nPlease attend the meeting at 4 PM today."],
    ["Subject: Report Submission\nSubmit the weekly report by tomorrow."],
    ["Subject: Urgent Refund Request\nI need my money back immediately. Please respond ASAP."],
    ["Subject: Server Down\nThe system is not working. Fix this immediately!"],
    ["Meeting at 5 PM\n\nURGENT refund needed\n\nWin a free iPhone now!"]
]

# Create Gradio interface
with gr.Blocks(title="📧 Email Triage System", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📧 AI-Powered Email Triage System
    
    Automatically classify and prioritize your emails with high accuracy.
    
    **Priority Levels:**
    - 🔴 **HIGH**: Urgent/Critical (refund, bug, emergency, ASAP)
    - 🟡 **MEDIUM**: Work/Normal Tasks (meeting, report, schedule)
    - 🟢 **LOW**: Informational/Marketing (newsletter, offer, promotion)
    
    **How to use:**
    1. Paste your email content in the text box below
    2. Click "Classify Email" to get instant priority classification
    3. For multiple emails, separate them with blank lines
    """)
    
    with gr.Row():
        with gr.Column():
            email_input = gr.Textbox(
                label="📝 Enter Email Content",
                placeholder="Paste your email here...\n\nFor multiple emails, separate with blank lines.",
                lines=10
            )
            classify_btn = gr.Button("🚀 Classify Email", variant="primary", size="lg")
        
        with gr.Column():
            output = gr.Textbox(
                label="📊 Classification Results",
                lines=15
            )
    
    gr.Markdown("### 💡 Try These Test Cases:")
    gr.Examples(
        examples=examples,
        inputs=email_input,
        outputs=output,
        fn=classify_single_email,
        cache_examples=False
    )
    
    classify_btn.click(
        fn=classify_multiple_emails,
        inputs=email_input,
        outputs=output
    )
    
    gr.Markdown("""
    ---
    ### 🎯 Keyword Detection:
    
    | Priority | Keywords |
    |----------|----------|
    | 🔴 HIGH | urgent, asap, immediately, critical, refund, bug, error, security, down |
    | 🟡 MEDIUM | meeting, schedule, report, update, reminder, submit, deadline, discuss |
    | 🟢 LOW | newsletter, offer, promotion, deal, sale, discount, subscribe, win, free |
    
    ### 👥 Team Dragon
    Built by: Mallarapu Arun Chand & T. Someswararao
    """)

if __name__ == "__main__":
    demo.launch()
