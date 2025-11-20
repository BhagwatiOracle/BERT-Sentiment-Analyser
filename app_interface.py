import gradio as gr
from sentiment_analyser import sentiment_model
from googleapiclient.discovery import build
from LLM_review import generate_llm_review

def create_interface(model_name):

    analyser = sentiment_model(model_name)

    with gr.Blocks(
        title="BERT Sentiment Analyzer",
        theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="blue")
    ) as demo:
        # Header section
        gr.Markdown(
            """
            <div style="text-align:center; margin-bottom:20px;">
                <h1 style="font-size:2.5em;">🌟 BERT Sentiment Analyzer</h1>
                <p style="font-size:1.1em;">
                    Analyze text sentiment using a fine-tuned <b>BERT</b> model.<br>
                    Enter your own text or upload a dataset to visualize results interactively.
                </p>
                <p>🧠 <b>Model:</b> <code>bert-base-uncased-imdb</code></p>
            </div>
            """
        )

        with gr.Tabs():
            # -------- TAB 1: Single Review Analysis --------
            with gr.TabItem("📝 Single Review Analysis"):
                gr.Markdown("### ✍️ Analyze the sentiment of an individual review")

                with gr.Row():
                    with gr.Column(scale=2):
                        review_input = gr.Textbox(
                            label="Enter a review",
                            placeholder="Type your review here...",
                            lines=4
                        )
                        analyze_button = gr.Button("🔍 Analyze Sentiment", variant="primary")
                    
                    with gr.Column(scale=1):
                        sentiment_output = gr.Textbox(
                            label="Predicted Sentiment",
                            interactive=False,
                            placeholder="Sentiment will appear here..."
                        )

                # Backend logic for single review
                def analyze_single_review(review):
                    return analyser.analyse_single(review)

                analyze_button.click(
                    analyze_single_review,
                    inputs=review_input,
                    outputs=sentiment_output
                )

            # -------- TAB 2: Batch Review Analysis --------
            with gr.TabItem("📊 Batch Review Analysis"):
                gr.Markdown("### 📂 Upload a CSV to analyze multiple reviews and visualize sentiment distribution")

                with gr.Blocks():
                    file_input = gr.File(
                        label="Upload CSV file (must contain a 'review' column)",
                        file_types=[".csv"]
                    )

                    batch_analyze_button = gr.Button("🚀 Run Batch Analysis", variant="primary")

                with gr.Row():
                    table_output = gr.Dataframe(label="📋 Sentiment Analysis Results", wrap=True)
                
                with gr.Row():
                    plot_output1 = gr.Plot(label="📈 Sentiment Distribution")
        
                    plot_output2 = gr.Plot(label="☁️ Word Cloud of Reviews")

                # Backend logic for batch analysis
                def analyze_batch_reviews(file):
                    df, fig, fig_wc = analyser.analyse_batch(file)
                    return df, fig, fig_wc

                batch_analyze_button.click(
                    analyze_batch_reviews,
                    inputs=file_input,
                    outputs=[table_output,plot_output1,plot_output2]
                )


            # ------------- TAB 3: YouTube Comments Analysis -------------
            with gr.TabItem("🎥 YouTube Comments Analysis"):
                gr.Markdown("### 📥 Analyze sentiments of YouTube video comments")

                with gr.Blocks():
                    youtube_url_input = gr.Textbox(
                        label="Enter YouTube Video URL",
                        placeholder="https://www.youtube.com/watch?v=example"
                    )

                    fetch_comments_button = gr.Button("📥 Fetch and Analyze Comments", variant="primary")
                
                with gr.Row():
                    comments_table_output = gr.Dataframe(label="📋 YouTube Comments Sentiment Analysis", wrap=True)
                
                with gr.Row():
                    comments_plot_output1 = gr.Plot(label="📈 Comments Sentiment Distribution")
        
                    comments_plot_output2 = gr.Plot(label="☁️ Word Cloud of Comments")

                with gr.Row():
                    ai_review_output = gr.Textbox(
                        label="🤖 AI Generated Review Summary",
                        interactive=False,
                        placeholder="AI review summary will appear here...",
                        lines=15,
                        max_lines=50
                    )


                # Backend logic for YouTube comments analysis
                def analyze_youtube_comments(url):
                    from youtube_data import youtube_data
                    video = youtube_data(url)
                    video_id = video.get_video_id()
                    api_key ="AIzaSyBlLzsJI3wwqtYP7wIsiMOMxi0_zzeB-G8"
                    youtube = build('youtube', 'v3', developerKey=api_key)
                    comments = youtube_data.get_comments_for_video(youtube, video_id)
                    
                    # Save comments to a temporary CSV for analysis
                    temp_csv = "youtube_comments.csv"
                    comments.to_csv(temp_csv, index=False, header=['review'])
                    
                    df, fig, fig_wc = analyser.analyse_batch(temp_csv)

                    ai_review = generate_llm_review(df)

                    return df, fig, fig_wc, ai_review
                
                
                fetch_comments_button.click(
                    analyze_youtube_comments,
                    inputs=youtube_url_input,
                    outputs=[comments_table_output, comments_plot_output1, comments_plot_output2,ai_review_output]
                )

                
                    

        # Footer section
        gr.Markdown(
            """
            <hr>
            <div style="text-align:center; font-size:0.9em; color:gray;">
                Built with ❤️ using <b>Gradio</b> and <b>Transformers</b> 🤗
            </div>
            """
        )

    return demo


if __name__ == "__main__":
    model_name = "Hhsjsnns/bert-base-uncased-imdb"
    app = create_interface(model_name)
    app.launch()
