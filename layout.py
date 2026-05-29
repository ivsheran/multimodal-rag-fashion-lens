import gradio as gr
import os

CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Mulish:wght@300;400;600&display=swap');

* {
    font-family: 'Mulish', sans-serif;
    color: #F8F0E2;
}

h1 {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 2rem;
}

h3 {
    font-family: 'Mulish', sans-serif;
    font-weight: 300;
}

.analyse-btn {
    background-color: #AE144A !important;
    color: #F8F0E2 !important;
}
"""

# Convert image_paths to HTML
def build_similar_items_html(image_paths, metadatas):
    html = "<div style='display:flex; flex-wrap:wrap; gap:16px;'>"
    for path, meta in zip(image_paths, metadatas):
        abs_path = os.path.abspath(path)
        html += f"""
        <div style='width:160px; text-align:center;'>
            <img src='gradio_api/file={abs_path}'
                style='width:160px; height:200px; object-fit:contain; 
                    background:#f5f5f5; border-radius:8px;'/>
            <p style='font-size:11px; margin-top:4px;'>
            {meta['product_name']}
            </p>
        </div>"""
        html += "</div>"
    return html

def create_layout(analyse_fn, clear_fn):
    with gr.Blocks(css=CSS, title="FashionLens", theme=gr.themes.Default()) as demo:
        
        # Header
        gr.Markdown("""
        # FashionLens
        ### Your AI fashion assistant — upload an outfit, get detailed style analysis and discover similar items
        """)
        
        # Fashion Analysis Section
        gr.Markdown("### Fashion Analysis")
        
        with gr.Row():
            # Left column — image upload
            with gr.Column(scale=1):
                image_input = gr.Image(
                    label="Upload your outfit",
                    type="filepath",
                    height=300
                )
                analyse_btn = gr.Button(
                    "Analyse",
                    elem_classes=["analyse-btn"]
                )
                clear_btn = gr.Button("Clear")
            
            # Right column — description output
            with gr.Column(scale=1):
                description_output = gr.Markdown(value="")
        
        # Similar Items Section
        gr.Markdown("### Similar Items")
        similar_items_output = gr.HTML(value="")
        
        # Button actions — we'll wire these in app.py
        analyse_btn.click(
            fn=analyse_fn,
            inputs=[image_input],
            outputs=[description_output, similar_items_output]
        )
        
        clear_btn.click(
            fn=clear_fn,
            inputs=[],
            outputs=[image_input, description_output, similar_items_output]
        )

    return demo
