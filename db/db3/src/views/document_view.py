import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection
# Potřebujeme dvě brány: jednu pro uložení dokumentu, druhou pro načtení seznamu oddělení
from gateways.document_gateway import DocumentGateway
from gateways.department_gateway import DepartmentGateway

class DocumentView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        
        # Inicializace bran
        self.doc_gateway = DocumentGateway(self.db)
        self.dep_gateway = DepartmentGateway(self.db)
        
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        # --- Nadpis a vstupy ---
        tk.Label(self.frame, text="Nový dokument").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.frame, text="Titulek:").grid(row=1, column=0, sticky="e")
        self.title_entry = tk.Entry(self.frame, width=40)
        self.title_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self.frame, text="Obsah:").grid(row=2, column=0, sticky="ne")
        self.content_text = tk.Text(self.frame, height=5, width=30)
        self.content_text.grid(row=2, column=1, sticky="w")

        # --- Výběr oddělení (Listbox pro Multi-select) ---
        tk.Label(self.frame, text="Přiřadit k oddělením:").grid(row=3, column=0, sticky="ne")
        
        self.dep_listbox = tk.Listbox(self.frame, selectmode="multiple", height=6)
        self.dep_listbox.grid(row=3, column=1, sticky="w", pady=5)
        
        # Načteme oddělení do seznamu, aby bylo co vybírat
        self.load_departments()

        # --- Tlačítko ---
        self.save_btn = tk.Button(self.frame, text="Vytvořit dokument (Transakce)", command=self.create_document)
        self.save_btn.grid(row=4, column=1, pady=20, sticky="e")

    def load_departments(self):
        # Načtení oddělení z databáze do Listboxu
        try:
            departments = self.dep_gateway.fetch_all()
            for dep in departments:
                # dep[0] je ID, dep[1] je Jméno. Zobrazíme: "ID: Jméno"
                self.dep_listbox.insert(tk.END, f"{dep[0]}: {dep[1]}")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst oddělení: {e}")

    def create_document(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        
        # Získání vybraných oddělení z Listboxu
        selected_indices = self.dep_listbox.curselection()
        
        if not title or not content:
            messagebox.showwarning("Varování", "Vyplňte titulek a obsah.")
            return

        if not selected_indices:
            messagebox.showwarning("Varování", "Vyberte alespoň jedno oddělení.")
            return

        # Převod vybraných řádků na seznam ID
        selected_ids = []
        for index in selected_indices:
            item_text = self.dep_listbox.get(index) # Text např. "5: IT Oddělení"
            dep_id = item_text.split(":")[0]        # Vezmeme jen to "5"
            selected_ids.append(int(dep_id))

        # Volání transakce v Gateway
        try:
            self.doc_gateway.create_document_with_transaction(title, content, selected_ids)
            
            messagebox.showinfo("Úspěch", "Dokument byl uložen a přiřazen oddělením.")
            
            # Vyčištění formuláře
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.dep_listbox.selection_clear(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Transakce selhala: {e}")