import tkinter as tk
from tkinter import messagebox
import os
import inputmessage
import exception
import outputmessage


class LogAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Analyzer")
        self.root.geometry("600x400")
        self.root.configure(bg="yellow")  # Set background color to yellow

        # Variable to hold the selected file path
        self.selected_file = tk.StringVar(value="")

        # Path to the sample logs folder
        self.sample_logs_dir = os.path.join(os.getcwd(), "Sample logs")

        # Initialize the login page
        self.login_page()

    def login_page(self):
        """Login page to authenticate the user."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Log Analyzer Tool", font=("Times New Roman", 30, "italic"), bg="yellow", fg="blue").pack(pady=20)
        tk.Label(self.root, text="Please Log In", font=("Times New Roman", 18, "italic"), bg="yellow", fg="darkblue").pack(pady=10)

        # Username and Password labels and entry widgets
        tk.Label(self.root, text="Username:", font=("Times New Roman", 18, "italic"), bg="yellow", fg="black").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Times New Roman", 18))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Times New Roman", 18, "italic"), bg="yellow", fg="black").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Times New Roman", 18), show="*")
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(self.root, text="Login", command=self.authenticate_user, font=("Times New Roman", 18, "italic"), bg="green", fg="white").pack(pady=20)

    def authenticate_user(self):
        """Authenticate the user credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Replace this with your own authentication logic
        if username == "log" and password == "786":
            messagebox.showinfo("Login Successful", "Welcome to the Log Analyzer Tool!")
            self.file_selection_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def file_selection_page(self):
        """First page: Display log files in the form of buttons."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Log Analyzer Tool", font=("Times New Roman", 30, "italic"), bg="yellow", fg="blue").pack(pady=20)
        tk.Label(self.root, text="Select a log file from 'sample_logs':", font=("Times New Roman", 18, "italic"), bg="yellow", fg="darkblue").pack(pady=10)

        # Create a frame for the log file buttons
        frame = tk.Frame(self.root, bg="yellow")
        frame.pack(expand=True)

        if not os.path.exists(self.sample_logs_dir):
            os.makedirs(self.sample_logs_dir)
            messagebox.showinfo("Info", f"'sample_logs' folder created at:\n{self.sample_logs_dir}")

        log_files = [f for f in os.listdir(self.sample_logs_dir) if f.endswith(".log")]

        if log_files:
            for index, log_file in enumerate(log_files):
                btn = tk.Button(
                    frame,
                    text=log_file,
                    font=("Times New Roman", 18, "italic"),
                    width=25,
                    height=2,
                    bg="skyblue",
                    command=lambda f=log_file: self.on_file_select(f),
                )
                btn.grid(row=index, column=0, pady=5, padx=5)  # Align buttons in a single column
        else:
            tk.Label(
                frame,
                text="No log files found in 'sample_logs' folder.",
                font=("Times New Roman", 18, "italic"),
                bg="yellow",
                fg="red",
            ).pack(pady=10)

    def on_file_select(self, log_file):
        """Handle file selection and move to the next page."""
        self.selected_file.set(os.path.join(self.sample_logs_dir, log_file))
        messagebox.showinfo("File Selected", f"Log file selected:\n{self.selected_file.get()}")
        self.button_page()

    def button_page(self):
        """Second page: Display buttons for processing options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Log Analyzer Tool", font=("Times New Roman", 30, "italic"), bg="yellow", fg="blue").pack(pady=20)

        # Processing buttons
        tk.Button(self.root, text="Process InputMessage",
                  command=self.process_input_message, font=("Times New Roman", 18, "italic"), width=20, bg="skyblue").pack(pady=10)
        tk.Button(self.root, text="Process Exceptions",
                  command=self.process_exceptions, font=("Times New Roman", 18, "italic"), width=20, bg="orange").pack(pady=10)
        tk.Button(self.root, text="Process OutputMessage",
                  command=self.process_output_message, font=("Times New Roman", 18, "italic"), width=20, bg="lightgreen").pack(pady=10)
        tk.Button(self.root, text="Back to File Selection", 
                  command=self.file_selection_page, font=("Times New Roman", 18, "italic"), width=20, bg="pink").pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.root.quit, font=("Times New Roman", 18, "italic"), width=20, bg="red").pack(pady=10)

    def process_input_message(self):
        """Process input messages using the selected log file."""
        if not self.selected_file.get():
            messagebox.showwarning("No File Selected", "Please select a log file first.")
            return
        try:
            self.input_data = inputmessage.process_log_file(self.selected_file.get())
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the file: {e}")

    def process_exceptions(self):
        """Process exceptions using the selected log file."""
        if not self.selected_file.get():
            messagebox.showwarning("No File Selected", "Please select a log file first.")
            return
        try:
            self.exception_data = exception.process_log_file(self.selected_file.get())
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the file: {e}")

    def process_output_message(self):
        """Process OutputMessage using the selected log file."""
        if not self.selected_file.get():
            messagebox.showwarning("No File Selected", "Please select a log file first.")
            return
        try:
            self.output_data = outputmessage.process_log_file(self.selected_file.get())
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LogAnalyzerApp(root)
    root.mainloop()
