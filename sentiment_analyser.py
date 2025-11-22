import pandas as pd
import matplotlib.pyplot as plt
from transformers import BertTokenizer, BertForSequenceClassification
import torch

class sentiment_model:

    def __init__(self,model_name):

        self.model = BertForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = BertTokenizer.from_pretrained(model_name)


    def analyse_single(self,text):

        inputs = self.tokenizer(text, return_tensors='pt', padding=True,truncation=True)
        with torch.no_grad():
            output = self.model(**inputs)
        
        logits = output.logits
        predicted_class = torch.argmax(logits, dim=-1).item()

        labels = ['Negative', 'Positive']

        return labels[predicted_class]
    
    
    def analyse_batch(self,file_path):

        df = pd.read_csv(file_path)
        if "review" not in df.columns:
            return "CSV must contain a column named 'review'."
        
        texts = df['review'].tolist()
        results = []

        for text in texts:
            result = self.analyse_single(text)
            results.append(result)

        df['sentiment'] = results

        # Visualize the results

        # ----Bar Plot----
        sentiment_count = df['sentiment'].value_counts()
        fig, (ax1, ax2) = plt.subplots(1,2)
        sentiment_count.plot(kind='bar',ax=ax1, color=['red', 'green'])
        ax1.set_title('Bar Plot')
        ax1.set_xlabel('Sentiment')
        ax1.set_ylabel('Count')

        # ----Pie Chart----
        sentiment_count.plot(kind='pie',ax=ax2,autopct='%1.1f%%', colors=['red', 'green'])
        ax2.set_title('Pie Plot')
        plt.tight_layout()

        # -----Word Cloud -------
        from wordcloud import WordCloud

        text = " ".join(df["review"].astype(str))
        wc = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis('off')
        ax_wc.set_title("Word Cloud of Reviews")

                
        return df, fig, fig_wc




