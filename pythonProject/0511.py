from openai import OpenAI
import tkinter as tk
from tkinter import ttk, scrolledtext
import json
from tkinter import messagebox


class TextAnalyzer:
    def __init__(self):
        self.client = OpenAI()
        self.window = tk.Tk()
        self.window.title("AI Tekstanalyse")
        self.window.geometry("900x700")

        # Input område
        self.input_frame = ttk.LabelFrame(self.window, text="Input Tekst")
        self.input_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.text_input = scrolledtext.ScrolledText(self.input_frame, height=10)
        self.text_input.pack(padx=5, pady=5, fill="both", expand=True)

        # Analyse muligheder
        self.options_frame = ttk.LabelFrame(self.window, text="Analyse Muligheder")
        self.options_frame.pack(padx=10, pady=5, fill="x")

        # Checkboxes for forskellige analyser
        self.sentiment_var = tk.BooleanVar(value=True)
        self.keywords_var = tk.BooleanVar(value=True)
        self.summary_var = tk.BooleanVar(value=True)
        self.readability_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(self.options_frame, text="Sentiment Analyse",
                        variable=self.sentiment_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(self.options_frame, text="Nøgleord",
                        variable=self.keywords_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(self.options_frame, text="Opsummering",
                        variable=self.summary_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(self.options_frame, text="Læsbarhed",
                        variable=self.readability_var).pack(side=tk.LEFT, padx=5)

        # Analyze knap
        self.analyze_btn = ttk.Button(self.window, text="Analyser Tekst",
                                      command=self.analyze_text)
        self.analyze_btn.pack(pady=10)

        # Output område
        self.output_frame = ttk.LabelFrame(self.window, text="Analyse Resultater")
        self.output_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(self.output_frame, height=15)
        self.output.pack(padx=5, pady=5, fill="both", expand=True)

    def analyze_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Advarsel", "Indtast venligst noget tekst at analysere!")
            return

        analysis_types = []
        if self.sentiment_var.get():
            analysis_types.append("sentiment")
        if self.keywords_var.get():
            analysis_types.append("keywords")
        if self.summary_var.get():
            analysis_types.append("summary")
        if self.readability_var.get():
            analysis_types.append("readability")

        prompt = f"""
        Analyser følgende tekst og giv en detaljeret rapport med følgende aspekter 
        {', '.join(analysis_types)}:

        Text til analyse:
        {text}

        For hver type analyse, giv detaljerede resultater i et letlæseligt format.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            self.output.delete("1.0", tk.END)
            self.output.insert("1.0", response.choices[0].message.content)

        except Exception as e:
            messagebox.showerror("Fejl", f"Der opstod en fejl under analysen: {str(e)}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TextAnalyzer()
    app.run()