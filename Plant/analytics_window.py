import tkinter as tk
from tkinter import ttk, messagebox
from db.combined_database import PlantDatabase


class AnalyticsWindow:
    """Okno z danymi analitycznymi z bazy danych"""
    
    def __init__(self, parent, database: PlantDatabase):
        self.database = database
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.load_data()
    
    def setup_window(self):
        """Konfiguruje okno analityczne"""
        self.window.title("Dane analityczne - Historia pomiarów")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Centrowanie okna
        self.window.transient()
        self.window.grab_set()
    
    def create_widgets(self):
        """Tworzy widżety w oknie analitycznym"""
        # Główna ramka
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Nagłówek
        header = ttk.Label(main_frame, text="Historia pomiarów czujników", 
                          font=('Arial', 16, 'bold'))
        header.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Ramka ze statystykami
        stats_frame = ttk.LabelFrame(main_frame, text="Statystyki", padding=10)
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="Ładowanie statystyk...", 
                                   font=('Arial', 10))
        self.stats_label.grid(row=0, column=0, sticky="w")
        
        # Ramka z tabelą danych
        data_frame = ttk.LabelFrame(main_frame, text="Dane pomiarowe", padding=10)
        data_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        data_frame.rowconfigure(0, weight=1)
        data_frame.columnconfigure(0, weight=1)
        
        # Treeview z danymi
        columns = ('Czas', 'Wilgotność (%)', 'Światło (%)', 'Temperatura (°C)', 'Godzina dnia')
        self.tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=15)
        
        # Konfiguracja kolumn z sortowaniem
        self.sort_reverse = {}  # Słownik do śledzenia kierunku sortowania dla każdej kolumny
        
        self.tree.heading('Czas', text='Data i czas ↕', command=lambda: self.sort_column('Czas', False))
        self.tree.heading('Wilgotność (%)', text='Wilgotność (%) ↕', command=lambda: self.sort_column('Wilgotność (%)', True))
        self.tree.heading('Światło (%)', text='Światło (%) ↕', command=lambda: self.sort_column('Światło (%)', True))
        self.tree.heading('Temperatura (°C)', text='Temperatura (°C) ↕', command=lambda: self.sort_column('Temperatura (°C)', True))
        self.tree.heading('Godzina dnia', text='Godzina dnia ↕', command=lambda: self.sort_column('Godzina dnia', True))
        
        # Szerokość kolumn
        self.tree.column('Czas', width=150)
        self.tree.column('Wilgotność (%)', width=120)
        self.tree.column('Światło (%)', width=120)
        self.tree.column('Temperatura (°C)', width=140)
        self.tree.column('Godzina dnia', width=120)
        
        # Scrollbary
        v_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout dla treeview i scrollbarów
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Ramka z przyciskami
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        self.refresh_button = ttk.Button(button_frame, text="Odśwież dane", 
                                       command=self.load_data)
        self.refresh_button.grid(row=0, column=0, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Wyczyść bazę danych", 
                                     command=self.clear_database)
        self.clear_button.grid(row=0, column=1, padx=(0, 10))

    def sort_column(self, col, is_numeric):
        """Sortuje kolumnę w Treeview z trzema stanami: nieposortowane → rosnąco → malejąco → nieposortowane"""
        # Pobierz wszystkie elementy z drzewa
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        
        # Określ stan sortowania (0=nieposortowane, 1=rosnąco, 2=malejąco)
        current_state = self.sort_reverse.get(col, 0)
        next_state = (current_state + 1) % 3
        self.sort_reverse[col] = next_state
        
        if next_state == 0:
            # Stan nieposortowany - przywróć oryginalną kolejność (sortuj po timestamp)
            self.load_data()  # Przeładuj dane w oryginalnej kolejności
            direction = "↕"
        else:
            # Sortuj dane
            reverse = (next_state == 2)  # True dla malejąco, False dla rosnąco
            
            if is_numeric:
                # Dla kolumn numerycznych
                try:
                    data.sort(key=lambda x: float(x[0]), reverse=reverse)
                except ValueError:
                    # Jeśli konwersja na float nie powiedzie się, sortuj jako tekst
                    data.sort(key=lambda x: x[0], reverse=reverse)
            else:
                # Dla kolumn tekstowych (data/czas)
                data.sort(key=lambda x: x[0], reverse=reverse)
            
            # Przeorganizuj elementy w drzewie
            for index, (val, child) in enumerate(data):
                self.tree.move(child, '', index)
            
            direction = "↓" if reverse else "↑"
        
        # Aktualizuj nagłówek kolumny ze wskaźnikiem kierunku sortowania
        current_text = self.tree.heading(col)['text']
        # Usuń poprzedni wskaźnik kierunku
        base_text = current_text.replace(" ↑", "").replace(" ↓", "").replace(" ↕", "")
        self.tree.heading(col, text=f"{base_text} {direction}")
        
        # Resetuj wskaźniki innych kolumn do stanu nieposortowanego
        for column in ['Czas', 'Wilgotność (%)', 'Światło (%)', 'Temperatura (°C)', 'Godzina dnia']:
            if column != col:
                self.sort_reverse[column] = 0  # Reset do stanu nieposortowanego
                other_text = self.tree.heading(column)['text']
                other_base_text = other_text.replace(" ↑", "").replace(" ↓", "").replace(" ↕", "")
                self.tree.heading(column, text=f"{other_base_text} ↕")
    
    def load_data(self):
        """Ładuje dane z bazy danych"""
        try:
            # Wyczyść istniejące dane
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Pobierz dane z bazy
            readings = self.database.get_all_readings()
            
            # Dodaj dane do treeview
            for reading in readings:
                timestamp, moisture, light, temperature, time_of_day = reading
                self.tree.insert('', 'end', values=(timestamp, moisture, light, temperature, time_of_day))
            
            # Aktualizuj statystyki
            self.update_statistics()
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można załadować danych: {str(e)}")
    
    def update_statistics(self):
        """Aktualizuje statystyki"""
        try:
            stats = self.database.get_database_stats()
            
            if stats['total_records'] > 0:
                stats_text = f"""Łączna liczba pomiarów: {stats['total_records']}
Zakres dat: {stats['date_range'][0]} - {stats['date_range'][1]}
Średnie wartości:
  • Wilgotność: {stats['averages']['moisture']}%
  • Światło: {stats['averages']['light']}%
  • Temperatura: {stats['averages']['temperature']}°C"""
            else:
                stats_text = "Brak danych w bazie danych"
            
            self.stats_label.config(text=stats_text)
            
        except Exception as e:
            self.stats_label.config(text=f"Błąd podczas ładowania statystyk: {str(e)}")
    
    def clear_database(self):
        """Czyści bazę danych po potwierdzeniu"""
        result = messagebox.askyesno(
            "Potwierdzenie", 
            "Czy na pewno chcesz usunąć wszystkie dane z bazy danych?\n\nTej operacji nie można cofnąć!",
            icon='warning'
        )
        
        if result:
            try:
                self.database.clear_database()
                self.load_data()  # Odśwież widok
                messagebox.showinfo("Sukces", "Baza danych została wyczyszczona.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można wyczyścić bazy danych: {str(e)}")