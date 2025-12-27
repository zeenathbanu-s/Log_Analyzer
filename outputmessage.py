import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

def analyze_log_file(log_file):
    """Extract lines containing the word 'OutputMessage'."""
    OutputMessage_lines = []
    lines = []
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "OutputMessage" in line:
                    OutputMessage_lines.append((i, line.strip()))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return [], []
    return OutputMessage_lines, lines

def display_results(OutputMessage_lines, lines, log_file):
    """Display the lines containing 'OutputMessage' and allow graph selection."""
    results_window = tk.Toplevel()
    results_window.title("OutputMessage Lines & Graph")
    results_window.geometry("1300x800")
    results_window.configure(bg="lightblue")

    # Top frame for buttons and file name
    top_frame = tk.Frame(results_window, bg="lightblue")
    top_frame.pack(fill="x", padx=10, pady=10)

    # Add selected file name at the center
    selected_file_label = tk.Label(
        top_frame,
        text=f"Selected File: {os.path.basename(log_file)}",
        font=("Times New Roman", 16, "italic"),
        fg="brown",
        bg="lightblue",
        anchor="center"
    )
    selected_file_label.pack(side="top", pady=10)

    # Log content display
    log_frame = tk.Frame(results_window, bg="white", relief=tk.RAISED, borderwidth=2)
    log_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(log_frame, bg="white")
    scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=canvas.yview, bg="#80CFA9")
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    text_widget = tk.Text(scrollable_frame, wrap="none", width=100, height=35, font=("Courier", 12), bg="beige")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_widget.insert(tk.END, "".join(lines))
    text_widget.config(state=tk.DISABLED)

    # Highlight functionality for selected lines
    def highlight_line(line_num):
        """Highlight the selected OutputMessage line in the log content."""
        text_widget.config(state=tk.NORMAL)
        text_widget.tag_remove("highlight", "1.0", tk.END)
        text_widget.tag_add("highlight", f"{line_num + 1}.0", f"{line_num + 1}.0 lineend")
        text_widget.tag_configure("highlight", background="orange", foreground="black")
        text_widget.see(f"{line_num + 1}.0")
        text_widget.config(state=tk.DISABLED)

    # OutputMessage lines display
    OutputMessage_frame = tk.Frame(results_window, bg="white", relief=tk.RAISED, borderwidth=2)
    OutputMessage_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    OutputMessage_canvas = tk.Canvas(OutputMessage_frame, bg="white")
    OutputMessage_scrollbar = tk.Scrollbar(OutputMessage_frame, orient="vertical", command=OutputMessage_canvas.yview, bg="#80CFA9")
    OutputMessage_scrollable_frame = tk.Frame(OutputMessage_canvas, bg="white")

    OutputMessage_scrollable_frame.bind("<Configure>", lambda e: OutputMessage_canvas.configure(scrollregion=OutputMessage_canvas.bbox("all")))
    OutputMessage_canvas.create_window((0, 0), window=OutputMessage_scrollable_frame, anchor="nw")
    OutputMessage_canvas.configure(yscrollcommand=OutputMessage_scrollbar.set)

    OutputMessage_canvas.pack(side="left", fill="both", expand=True)
    OutputMessage_scrollbar.pack(side="right", fill="y")

    total_lines = len(lines)
    total_OutputMessages = len(OutputMessage_lines)
    OutputMessage_percentage = (total_OutputMessages / total_lines * 100) if total_lines > 0 else 0

    # Labels for statistics at the top left corner of OutputMessage lines
    stats_frame = tk.Frame(OutputMessage_scrollable_frame, bg="lightblue")
    stats_frame.pack(fill="x", padx=5, pady=5)

    tk.Label(stats_frame, text=f"Total Lines: {total_lines}", font=("Times New Roman", 14, "italic"), bg="lightblue", anchor="w").pack(anchor="w", padx=5, pady=2)
    tk.Label(stats_frame, text=f"Total OutputMessage Lines: {total_OutputMessages}", font=("Times New Roman", 14, "italic"), bg="lightblue", anchor="w").pack(anchor="w", padx=5, pady=2)
    tk.Label(stats_frame, text=f"Percentage of OutputMessage Lines: {OutputMessage_percentage:.2f}%", font=("Times New Roman", 14, "italic"), bg="lightblue", anchor="w").pack(anchor="w", padx=5, pady=2)

    for index, message in OutputMessage_lines:
        def on_click(idx=index):
            highlight_line(idx)

        label = tk.Label(OutputMessage_scrollable_frame, text=f"Line {index + 1}: {message}", font=("Times New Roman", 12), anchor="w", fg="blue", cursor="hand2", bg="white")
        label.pack(anchor="w", padx=10, pady=2)
        label.bind("<Button-1>", lambda event, idx=index: on_click(idx))

    if not OutputMessage_lines:
        tk.Label(OutputMessage_scrollable_frame, text="No lines containing 'OutputMessage' found in the log file.", font=("Times New Roman", 14), bg="white").pack(pady=10)

    # Graph plotting functions
    def show_pie_chart():
        """Plot and display a pie chart."""
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['OutputMessage Lines', 'Other Lines']
        sizes = [total_OutputMessages, total_lines - total_OutputMessages]
        colors = ['pink', 'lightgreen']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        for text in ax.texts:
            text.set_fontsize(12)
            text.set_color("blue")
        ax.set_title('Pie Chart: Log Line Analysis', fontsize=16, color="darkred")

        display_graph(fig, "Pie Chart")

    def show_donut_chart():
        """Plot and display a donut chart."""
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['OutputMessage Lines', 'Other Lines']
        sizes = [total_OutputMessages, total_lines - total_OutputMessages]
        colors = ['pink', 'lightgreen']
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        for w in wedges:
            w.set_edgecolor('white')
        ax.set_title('Donut Chart: Log Line Analysis', fontsize=16, color="darkred")
        plt.setp(wedges, width=0.4)
        for text in autotexts + texts:
            text.set_fontsize(12)
            text.set_color("blue")
        display_graph(fig, "Donut Chart")

    def show_line_chart():
        """Plot and display a line chart."""
        fig, ax = plt.subplots(figsize=(6, 4))
        x = ['OutputMessage Lines', 'Other Lines']
        y = [total_OutputMessages, total_lines - total_OutputMessages]
        ax.plot(x, y, marker='o', linestyle='-', color='pink')
        ax.set_title('Line Chart: Log Line Analysis', fontsize=16, color="darkred")
        ax.set_ylabel('Count', fontsize=12, color="blue")
        ax.tick_params(axis='x', labelsize=12, colors="blue")
        ax.tick_params(axis='y', labelsize=12, colors="blue")

        display_graph(fig, "Line Chart")

    def show_bar_chart():
        """Plot and display a bar chart."""
        fig, ax = plt.subplots(figsize=(6, 4))
        categories = ['OutputMessage Lines', 'Other Lines']
        counts = [total_OutputMessages, total_lines - total_OutputMessages]
        ax.bar(categories, counts, color=['pink', 'lightgreen'])
        ax.set_title('Bar Chart: Log Line Analysis', fontsize=16, color="darkred")
        ax.set_ylabel('Count', fontsize=12, color="blue")
        ax.tick_params(axis='x', labelsize=12, colors="blue")
        ax.tick_params(axis='y', labelsize=12, colors="blue")

        display_graph(fig, "Bar Chart")

    def display_graph(fig, title):
        """Display the graph in a new window."""
        graph_window = tk.Toplevel(results_window)
        graph_window.title(title)
        graph_window.geometry("700x500")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        tk.Button(graph_window, text="Close Graph", command=graph_window.destroy, font=("Times New Roman", 12)).pack(pady=10)

    # Show Graph Button
    def show_graph_selection():
        """Ask the user to select the type of graph to display."""
        selection_window = tk.Toplevel(results_window)
        selection_window.title("Select Graph Type")
        selection_window.geometry("300x300")
        tk.Label(selection_window, text="Select the type of graph to display:", font=("Times New Roman", 14)).pack(pady=20)

        tk.Button(selection_window, text="Pie Chart", command=lambda: [show_pie_chart(), selection_window.destroy()], font=("Times New Roman", 18,"italic"), width=20,  bg="lightgreen").pack(pady=10)
        tk.Button(selection_window, text="Donut Chart", command=lambda: [show_donut_chart(), selection_window.destroy()], font=("Times New Roman", 18,"italic"), width=20,  bg="lightblue").pack(pady=10)
        tk.Button(selection_window, text="Line Chart", command=lambda: [show_line_chart(), selection_window.destroy()], font=("Times New Roman", 18,"italic"),  width=20, bg="orange").pack(pady=10)
        tk.Button(selection_window, text="Bar Chart", command=lambda: [show_bar_chart(), selection_window.destroy()], font=("Times New Roman", 18,"italic"),  width=20, bg="pink").pack(pady=10)

    # Report generation
    def generate_report():
        """Generate an Excel report with a fixed name in the same folder as the log file."""
        report_data = {
            "Category": ["OutputMessage Lines", "Other Lines", "Total Lines"],
            "Count": [total_OutputMessages, total_lines - total_OutputMessages, total_lines],
        }
        df = pd.DataFrame(report_data)

        try:
            report_path = os.path.join(os.path.dirname(log_file), "OutputMessage_report.xlsx")

            with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Report")
                workbook = writer.book
                worksheet = writer.sheets["Report"]

                for column_cells in worksheet.columns:
                    max_length = max(len(str(cell.value)) for cell in column_cells)
                    worksheet.column_dimensions[column_cells[0].column_letter].width = max_length + 5

            messagebox.showinfo("Success", f"Report saved at {report_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the report: {e}")

    # Add buttons to the top frame
    tk.Button(top_frame, text="Show Graph", command=show_graph_selection, font=("Times New Roman", 14), bg="orange").pack(side="left", padx=10)
    tk.Button(top_frame, text="Generate Report", command=generate_report, font=("Times New Roman", 14), bg="orange").pack(side="left", padx=10)

def process_log_file(log_file):
    """Process the log file and display OutputMessage lines."""
    OutputMessage_lines, lines = analyze_log_file(log_file)
    if OutputMessage_lines or lines:
        display_results(OutputMessage_lines, lines, log_file)

def main():
    """Main application to select and process a log file."""
    root = tk.Tk()
    root.title("Log File Analyzer")
    root.geometry("400x300")

    def open_file():
        log_file = filedialog.askopenfilename(filetypes=[("Log Files", "*.log"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if not log_file:
            messagebox.showwarning("Input Required", "Please select a log file.")
        else:
            process_log_file(log_file)

    tk.Label(root, text="Log File Analyzer", font=("Times New Roman", 18, "bold"), bg="lightblue").pack(pady=20)
    tk.Button(root, text="Select Log File", command=open_file, font=("Times New Roman", 12), bg="lightgreen").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
