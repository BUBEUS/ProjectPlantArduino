import tkinter as tk
from tkinter import ttk, messagebox
from db.combined_database import PlantDatabase


class AnalyticsWindow:
    """Analytics window with database data"""
    
    def __init__(self, parent, database: PlantDatabase):
        self.database = database
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.load_data()
    
    def setup_window(self):
        """Configures analytics window"""
        self.window.title("Analytics Data - Measurement History")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Center window
        self.window.transient()
        self.window.grab_set()
    
    def create_widgets(self):
        """Creates widgets in analytics window"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Header
        header = ttk.Label(main_frame, text="Sensor Measurement History", 
                          font=('Arial', 16, 'bold'))
        header.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="Loading statistics...", 
                                   font=('Arial', 10))
        self.stats_label.grid(row=0, column=0, sticky="w")
        
        # Data table frame
        data_frame = ttk.LabelFrame(main_frame, text="Measurement Data", padding=10)
        data_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        data_frame.rowconfigure(0, weight=1)
        data_frame.columnconfigure(0, weight=1)
        
        # Treeview with data
        columns = ('Time', 'Moisture (%)', 'Light (%)', 'Temperature (°C)', 'Hour of Day')
        self.tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=15)
        
        # Column configuration with sorting
        self.sort_reverse = {}  # Dictionary to track sorting direction for each column
        
        self.tree.heading('Time', text='Date and Time ↕', command=lambda: self.sort_column('Time', False))
        self.tree.heading('Moisture (%)', text='Moisture (%) ↕', command=lambda: self.sort_column('Moisture (%)', True))
        self.tree.heading('Light (%)', text='Light (%) ↕', command=lambda: self.sort_column('Light (%)', True))
        self.tree.heading('Temperature (°C)', text='Temperature (°C) ↕', command=lambda: self.sort_column('Temperature (°C)', True))
        self.tree.heading('Hour of Day', text='Hour of Day ↕', command=lambda: self.sort_column('Hour of Day', True))
        
        # Column widths
        self.tree.column('Time', width=150)
        self.tree.column('Moisture (%)', width=120)
        self.tree.column('Light (%)', width=120)
        self.tree.column('Temperature (°C)', width=140)
        self.tree.column('Hour of Day', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        self.refresh_button = ttk.Button(button_frame, text="Refresh Data", 
                                       command=self.load_data)
        self.refresh_button.grid(row=0, column=0, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear Database", 
                                     command=self.clear_database)
        self.clear_button.grid(row=0, column=1, padx=(0, 10))

    def sort_column(self, col, is_numeric):
        """Sorts column in Treeview with three states: unsorted → ascending → descending → unsorted"""
        # Get all elements from tree
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        
        # Determine sorting state (0=unsorted, 1=ascending, 2=descending)
        current_state = self.sort_reverse.get(col, 0)
        next_state = (current_state + 1) % 3
        self.sort_reverse[col] = next_state
        
        if next_state == 0:
            # Unsorted state - restore original order (sort by timestamp)
            self.load_data()  # Reload data in original order
            direction = "↕"
        else:
            # Sort data
            reverse = (next_state == 2)  # True for descending, False for ascending
            
            if is_numeric:
                # For numeric columns
                try:
                    data.sort(key=lambda x: float(x[0]), reverse=reverse)
                except ValueError:
                    # If float conversion fails, sort as text
                    data.sort(key=lambda x: x[0], reverse=reverse)
            else:
                # For text columns (date/time)
                data.sort(key=lambda x: x[0], reverse=reverse)
            
            # Reorganize elements in tree
            for index, (val, child) in enumerate(data):
                self.tree.move(child, '', index)
            
            direction = "↓" if reverse else "↑"
        
        # Update column header with sorting direction indicator
        current_text = self.tree.heading(col)['text']
        # Remove previous direction indicator
        base_text = current_text.replace(" ↑", "").replace(" ↓", "").replace(" ↕", "")
        self.tree.heading(col, text=f"{base_text} {direction}")
        
        # Reset other column indicators to unsorted state
        for column in ['Time', 'Moisture (%)', 'Light (%)', 'Temperature (°C)', 'Hour of Day']:
            if column != col:
                self.sort_reverse[column] = 0  # Reset to unsorted state
                other_text = self.tree.heading(column)['text']
                other_base_text = other_text.replace(" ↑", "").replace(" ↓", "").replace(" ↕", "")
                self.tree.heading(column, text=f"{other_base_text} ↕")
    
    def load_data(self):
        """Loads data from database"""
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get data from database
            readings = self.database.get_all_readings()
            
            # Add data to treeview
            for reading in readings:
                timestamp, moisture, light, temperature, time_of_day = reading
                self.tree.insert('', 'end', values=(timestamp, moisture, light, temperature, time_of_day))
            
            # Update statistics
            self.update_statistics()
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load data: {str(e)}")
    
    def update_statistics(self):
        """Updates statistics"""
        try:
            stats = self.database.get_database_stats()
            
            if stats['total_records'] > 0:
                stats_text = f"""Total measurements: {stats['total_records']}
Date range: {stats['date_range'][0]} - {stats['date_range'][1]}
Average values:
  • Moisture: {stats['averages']['moisture']}%
  • Light: {stats['averages']['light']}%
  • Temperature: {stats['averages']['temperature']}°C"""
            else:
                stats_text = "No data in database"
            
            self.stats_label.config(text=stats_text)
            
        except Exception as e:
            self.stats_label.config(text=f"Error loading statistics: {str(e)}")
    
    def clear_database(self):
        """Clears database after confirmation"""
        result = messagebox.askyesno(
            "Confirmation", 
            "Are you sure you want to delete all data from the database?\n\nThis operation cannot be undone!",
            icon='warning'
        )
        
        if result:
            try:
                self.database.clear_database()
                self.load_data()  # Refresh view
                messagebox.showinfo("Success", "Database has been cleared.")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot clear database: {str(e)}")