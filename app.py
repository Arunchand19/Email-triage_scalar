import gradio as gr
import os
from transformers import pipeline

# Initialize zero-shot classification model
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except:
    classifier = None

def classify_single_email(email_text):
    """Classify a single email using AI"""
    if not email_text or not email_text.strip():
        return "⚠️ Please enter email content to classify"
    
    email_lower = email_text.lower()
    
    # Use AI model if available
    if classifier:
        try:
            labels = ["urgent high priority", "medium priority", "low priority spam"]
            result = classifier(email_text, labels)
            top_label = result["labels"][0]
            confidence = result["scores"][0]
            
            if "urgent" in top_label or "high" in top_label:
                priority = "🔴 HIGH PRIORITY"
            elif "medium" in top_label:
                priority = "🟡 MEDIUM PRIORITY"
            else:
                priority = "🟢 LOW PRIORITY"
            
            return f"""
📧 EMAIL CLASSIFICATION RESULT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Your Email:
{email_text[:200]}{'...' if len(email_text) > 200 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Classification: {priority}
📊 Confidence: {confidence:.2%}

💡 AI Analysis:
{top_label.upper()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        except Exception as e:
            pass
    
    # Fallback: Rule-based classification
    score = 0
    reasons = []
    
    # High priority keywords
    urgent_keywords = ["urgent", "asap", "immediately", "critical", "emergency", "important", 
                       "deadline", "refund", "complaint", "bug", "error", "security", "breach"]
    for keyword in urgent_keywords:
        if keyword in email_lower:
            score += 3
            reasons.append(f"Contains urgent keyword: '{keyword}'")
    
    # Medium priority keywords
    medium_keywords = ["meeting", "schedule", "report", "update", "review", "question", 
                       "request", "follow up", "reminder"]
    for keyword in medium_keywords:
        if keyword in email_lower:
            score += 1
            reasons.append(f"Contains medium priority keyword: '{keyword}'")
    
    # Low priority keywords
    low_keywords = ["newsletter", "subscribe", "offer", "promotion", "deal", "sale", 
                    "unsubscribe", "marketing", "advertisement"]
    for keyword in low_keywords:
        if keyword in email_lower:
            score -= 1
            reasons.append(f"Contains low priority keyword: '{keyword}'")
    
    # Determine priority
    if score >= 3:
        priority = "🔴 HIGH PRIORITY"
        action = "⚡ Respond immediately"
    elif score >= 1:
        priority = "🟡 MEDIUM PRIORITY"
        action = "📅 Respond within 24 hours"
    else:
        priority = "🟢 LOW PRIORITY"
        action = "📋 Review when convenient"
    
    # Generate response
    result = f"""
📧 EMAIL CLASSIFICATION RESULT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Your Email:
{email_text[:200]}{'...' if len(email_text) > 200 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Classification: {priority}
📊 Priority Score: {score}/10

💡 Analysis:
"""
    
    if reasons:
        for reason in reasons[:3]:
            result += f"\n  • {reason}"
    else:
        result += "\n  • No specific keywords detected"
        result += "\n  • Classified as standard email"
    
    result += f"\n\n✅ Recommended Action:\n  {action}\n"
    result += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    return result

def classify_multiple_emails(emails_text):
    """Classify multiple emails separated by lines"""
    if not emails_text or not emails_text.strip():
        return "⚠️ Please enter email content to classify"
    
    # Split by double newlines or numbered lines
    emails = [e.strip() for e in emails_text.split('\n\n') if e.strip()]
    
    if len(emails) == 1:
        return classify_single_email(emails[0])
    
    result = f"📧 BATCH EMAIL CLASSIFICATION\n"
    result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    result += f"Total Emails: {len(emails)}\n\n"
    
    high_count = 0
    medium_count = 0
    low_count = 0
    
    for i, email in enumerate(emails[:10], 1):  # Limit to 10 emails
        classification = classify_single_email(email)
        
        if "HIGH PRIORITY" in classification:
            high_count += 1
            priority = "🔴 HIGH"
        elif "MEDIUM PRIORITY" in classification:
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
    ["URGENT: Customer refund request - Order #12345 needs immediate attention!"],
    ["Hi, can we schedule a meeting next week to discuss the project?"],
    ["Subscribe to our newsletter for exclusive deals and offers!"],
    ["CRITICAL BUG: Production server is down, users cannot access the application"],
    ["Reminder: Monthly report submission deadline is tomorrow"]
]

# Create Gradio interface
with gr.Blocks(title="📧 Email Triage System", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📧 AI-Powered Email Triage System
    
    Automatically classify and prioritize your emails using AI technology.
    
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
    
    gr.Markdown("### 💡 Try These Examples:")
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
    ### 🎯 Priority Levels:
    - 🔴 **HIGH**: Urgent matters requiring immediate attention
    - 🟡 **MEDIUM**: Important but not urgent, respond within 24 hours
    - 🟢 **LOW**: Informational, review when convenient
    
    ### 👥 Team Dragon
    Built by: Mallarapu Arun Chand & T. Someswararao
    """)

if __name__ == "__main__":
    demo.launch()
