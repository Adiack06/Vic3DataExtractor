import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import mplcursors
from qbstyles import mpl_style
from Extractor import *


mpl_style(dark=True)





def plot_graph(csv_file):
    data = {}
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)[2:]
        for row in reader:
            data_type = row[0]
            country = row[1]
            values = [float(val) if val else 0 for val in row[2:]]
            key = (data_type, country)
            data[key] = values

    plt.figure(figsize=(12, 8))

    # Plot every 20th data point for each data type and country
    for key, values in data.items():
        reduced_values = values[::20]  # Take every 20th value
        reduced_headers = headers[::20]  # Corresponding reduced headers
        plt.plot(reduced_headers, reduced_values, label=f'{key[0]} - {key[1]}', picker=5)  # Enable picking for mplcursors

    plt.xlabel('Time Points')
    plt.ylabel('Values')
    plt.title('Economic Data Over Time (Reduced Data Points)')
    plt.grid(True)
    plt.xticks([])  # Hide x-axis labels

    # Add interactive cursor
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'{sel.artist.get_label()} : {sel.target[1]:.2f}'))

    plt.savefig('output_graph.png')
    plt.show()


def run_program(zip_files, selected_data_type):
    extract_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Extracted_saves")
    os.makedirs(extract_dir, exist_ok=True)

    progress_var.set(0)
    progress_bar['maximum'] = len(zip_files)

    for i, zip_file in enumerate(zip_files):
        file_name, _ = os.path.splitext(os.path.basename(zip_file))
        save_path = os.path.join(extract_dir, file_name)
        os.makedirs(save_path, exist_ok=True)
        unzip(zip_file, save_path)
        extract_eco(save_path, selected_data_type)
        progress_var.set(i + 1)
        root.update_idletasks()

    merged_csv = mergecsv(extract_dir)
    plot_graph(merged_csv)
    messagebox.showinfo("Completed", "The processing is complete and the graph has been saved as output_graph.png")


def select_files():
    files = filedialog.askopenfilenames(filetypes=[("ZIP files", "*.v3")])
    if files:
        def on_select_data_type():
            selected_data_type = data_type_var.get()
            if selected_data_type:
                data_type_window.destroy()
                run_program(files, selected_data_type)
            else:
                messagebox.showwarning("Selection Error", "Please select a data type.")

        data_type_window = tk.Toplevel(root)
        data_type_window.title("Select Data Type")
        label = tk.Label(data_type_window, text="Select a Data Type")
        label.pack(pady=10)

        data_type_var = tk.StringVar(value="gdp")
        dropdown = ttk.Combobox(data_type_window, textvariable=data_type_var, values=["gdp", "prestige","trend_population","literacy"])
        dropdown.pack(pady=10)

        select_button = tk.Button(data_type_window, text="Select", command=on_select_data_type)
        select_button.pack(pady=10)


root = tk.Tk()
root.title("Vic3 Save Processor")

canvas = tk.Canvas(root, height=400, width=600)
canvas.pack()

frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

label = tk.Label(frame, text="Select Vic3 Save ZIP files to process", bg='white')
label.pack(pady=20)

select_button = tk.Button(frame, text="Select Files", padx=10, pady=5, fg="white", bg="#263D42", command=select_files)
select_button.pack()

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
progress_bar.pack(pady=20)

root.mainloop()
