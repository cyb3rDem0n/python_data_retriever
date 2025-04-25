import tkinter as tk
from tkinter import ttk

def show_grouped_results(grouped_results):
    root = tk.Tk()
    root.title("Contratti per Partner")
    root.geometry("700x400")
    root.configure(bg="#23272f")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", 
                    background="#2c313c", 
                    foreground="#e1e1e6", 
                    fieldbackground="#23272f",
                    rowheight=28,
                    font=('Segoe UI', 11))
    style.configure("Treeview.Heading", 
                    background="#23272f", 
                    foreground="#ffb86c", 
                    font=('Segoe UI', 12, 'bold'))

    tree = ttk.Treeview(root)
    tree["columns"] = ("Contract", "Status", "Type")
    tree.heading("#0", text="Partner Name")
    tree.heading("Contract", text="Contract")
    tree.heading("Status", text="Status")
    tree.heading("Type", text="Type")

    tree.column("#0", width=200)
    tree.column("Contract", width=180)
    tree.column("Status", width=120)
    tree.column("Type", width=120)

    # Inserisci i dati raggruppati
    for name, contracts in grouped_results.items():
        parent = tree.insert("", "end", text=name, open=True)
        for contract in contracts:
            tree.insert(parent, "end", 
                        values=(contract["Contract"], contract["Status"], contract["Type"]))

    tree.pack(expand=True, fill="both", padx=20, pady=20)

    # Effetto cool: titolo animato
    def animate_title(i=0):
        colors = ["#ffb86c", "#8be9fd", "#50fa7b", "#bd93f9", "#ff79c6"]
        style.configure("Treeview.Heading", foreground=colors[i % len(colors)])
        root.after(300, animate_title, i+1)
    animate_title()

    root.mainloop()

# Esempio di dati raggruppati (sostituisci con i tuoi risultati)
if __name__ == "__main__":
    grouped_results = {
        "Partner A": [
            {"Contract": "C-001", "Status": "Active", "Type": "Gold"},
            {"Contract": "C-002", "Status": "Expired", "Type": "Silver"},
        ],
        "Partner B": [
            {"Contract": "C-003", "Status": "Active", "Type": "Platinum"},
        ]
    }
    show_grouped_results(grouped_results)