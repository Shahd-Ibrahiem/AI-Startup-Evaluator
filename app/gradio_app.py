import gradio as gr
import time

from app.graph.workflow import create_workflow
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------------- Workflow ----------------
workflow = create_workflow()


# ---------------- Helpers ----------------
def get_score_status(score):
    if score < 40:
        return "🔴 Reject"
    elif score < 70:
        return "🟡 Consider"
    else:
        return "🟢 Invest"


def generate_pdf(text, score):
    file_path = "startup_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("AI Startup Evaluation Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Investment Score: {score}", styles["Heading2"]))
    content.append(Spacer(1, 12))

    content.append(
        Paragraph(text.replace("\n", "<br/>"), styles["BodyText"])
    )

    doc.build(content)
    return file_path


# ---------------- Core Function ----------------
def evaluate_startup(idea: str , request: gr.Request):
    if not idea.strip():
        return ("Please enter a startup idea", 0, "", "", "", "")

    result = workflow.invoke(
        {
            "idea": idea,
            "market_analysis": "",
            "competitor_analysis": "",
            "swot_analysis": "",
            "financial_risk_analysis": "",
            "market_score": 50,
            "investment_score": 0,
            "final_decision": "",
            "messages": [],
        },
        config={"configurable": {"thread_id": request.session_hash}},
    )

    score = result.get("investment_score", 0)
    status = get_score_status(score)

    overview = f"""
# {status}

===== MARKET ANALYSIS =====
{result.get("market_analysis", "")}

===== COMPETITORS =====
{result.get("competitor_analysis", "")}

===== SWOT =====
{result.get("swot_analysis", "")}

===== FINANCIAL RISK =====
{result.get("financial_risk_analysis", "")}

===== FINAL DECISION =====
{result.get("final_decision", "")}

===== SCORE =====
{score}/100
"""

    return (
        overview,
        score,
        result.get("market_analysis", ""),
        result.get("competitor_analysis", ""),
        result.get("swot_analysis", ""),
        result.get("financial_risk_analysis", ""),
    )


# ---------------- UI ----------------
with gr.Blocks(title="AI Startup Evaluator") as demo:

    gr.Markdown("# 🚀 AI Startup Evaluator (VC Intelligence System)")
    gr.Markdown("Enter a startup idea and get full AI investment analysis.")

    idea_input = gr.Textbox(
        label="Startup Idea",
        placeholder="Example: AI-powered fitness startup",
    )

    submit_btn = gr.Button("Evaluate 🚀")

    with gr.Tabs():

        # ---------------- Overview ----------------
        with gr.Tab("📊 Overview"):
            output_text = gr.Markdown()
            # score_gauge = gr.Gauge(
            #     label="Investment Score",
            #     minimum=0,
            #     maximum=100,
            #     value=0,
            #     interactive=False,
            # )

            score_gauge = gr.Slider(
                minimum=0,
                maximum=100,
                label="Investment Score",
                value=0,
                interactive=False
            )

        # ---------------- Market ----------------
        with gr.Tab("📈 Market Analysis"):
            market_box = gr.Markdown()

        # ---------------- Competitors ----------------
        with gr.Tab("🏢 Competitors"):
            competitor_box = gr.Markdown()

        # ---------------- SWOT ----------------
        with gr.Tab("🧠 SWOT Analysis"):
            swot_box = gr.Markdown()

        # ---------------- Financial ----------------
        with gr.Tab("💰 Financial Risk"):
            financial_box = gr.Markdown()

    # ---------------- PDF ----------------
    download_btn = gr.Button("📄 Download Report")
    file_output = gr.File()

    # ---------------- Events ----------------
    submit_btn.click(
        fn=evaluate_startup,
        inputs=idea_input,
        outputs=[
            output_text,
            score_gauge,
            market_box,
            competitor_box,
            swot_box,
            financial_box,
        ],
    )

    download_btn.click(
        fn=lambda text, score: generate_pdf(text, score),
        inputs=[output_text, score_gauge],
        outputs=file_output,
    )


# ---------------- Run ----------------
if __name__ == "__main__":
    #demo.launch(share=True)
    demo.launch()