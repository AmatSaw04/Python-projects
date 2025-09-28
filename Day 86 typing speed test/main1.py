import tkinter as tk

import time

import random

texts = [

    "The quick brown fox jumps over the lazy dog.",

    "Python is a powerful programming language.",

    "Typing fast requires practice and focus.",

    "Artificial intelligence is shaping the future.",

    "Consistency is the key to improving your skills."

]

class Speed_Test_App:
    def __init__(self,root):
        self.root = root
        self.root.title("Test your Typing speed")
        self.root.geometry("800x400")
        self.sample_text = random.choice(texts)
        self.title_label = tk.Label(root, text="Typing Speed Test", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)

        self.text_Label = tk.Label(root, wraplength=700, font=("Arial", 14), fg="blue")
        self.text_Label.pack(pady=20)
        self.text_Label.config(text=self.sample_text)


        self.time_start = None
        self.test_running = False

        self.entry = tk.Text(root, height=5, width=80, font=("Arial", 12))
        self.entry.pack(pady=10)
        self.entry.bind("<KeyPress>", self.start_test)



        self.result_label = tk.Label(root, text="", font=("Arial", 16))
        self.result_label.pack(pady=20)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart)
        self.restart_button.pack(pady=10)


    def start_test(self, event):

        if not self.test_running:
            self.time_start = time.time()
            self.test_running = True

        if event.keysym == "Return":
            self.finish_test()

    def finish_test(self):
        end_time = time.time()
        elapsed_time = (end_time - self.time_start ) / 60
        typed_text = self.entry.get("1.0", tk.END).strip()
        word_count = len(typed_text.split())
        wpm = word_count / elapsed_time if elapsed_time > 0 else 0

        # Accuracy
        sample_words = self.sample_text.split()
        typed_words = typed_text.split()
        correct = sum(1 for i, w in enumerate(typed_words) if i < len(sample_words) and w == sample_words[i])
        accuracy = (correct / len(sample_words)) * 100
        self.result_label.config(text=f"Speed: {wpm:.2f} WPM | Accuracy: {accuracy:.1f}%")
        self.test_running = False

    def restart(self):
        self.sample_text = random.choice(texts)
        self.text_Label.config(text=self.sample_text)
        self.entry.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.test_running = False
        self.time_start = None

if __name__ == "__main__":
    root = tk.Tk()
    app = Speed_Test_App(root)
    root.mainloop()



