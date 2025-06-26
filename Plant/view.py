import tkinter as tk
from tkinter import ttk


class SystemView:

    def __init__(self, master: tk.Tk, controller):
        self.master = master
        self.controller = controller
        
        #Master window
        master.title("🌱 Plant Management Panel")
        master.geometry("650x700")
        master.minsize(550, 600)
        master.resizable(True, True)
        
        # Configure modern styling
        self.style = ttk.Style()
        self.configure_styles()

        #Main window with better padding
        self.main_frame = ttk.Frame(master, padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        # Better row configuration for proper scaling
        self.main_frame.rowconfigure(1, weight=0)  # Status frame - fixed height
        self.main_frame.rowconfigure(2, weight=0)  # Message frame - fixed height  
        self.main_frame.rowconfigure(3, weight=0)  # Control frame - fixed height
        self.main_frame.columnconfigure(0, weight=1)

        #Header
        header = ttk.Label(self.main_frame, text="🌱 Plant Management System", style='Header.TLabel')
        header.grid(row=0, column=0, pady=(0, 30), sticky="ew")

        #Status frame with modern styling
        status_frame = ttk.LabelFrame(self.main_frame, text="📊 Plant Status", padding=20)
        status_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        status_frame.columnconfigure(0, weight=1)
        
        # Status labels with icons and better styling
        self.moisture_label = ttk.Label(status_frame, 
                                      text=f"💧 Moisture: {self.controller.model.get_moisture()}%", 
                                      style='Status.TLabel')
        self.moisture_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.light_label = ttk.Label(status_frame, 
                                   text=f"☀️ Light: {self.controller.model.get_light()}%", 
                                   style='Status.TLabel')
        self.light_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.temperature_label = ttk.Label(status_frame, 
                                         text=f"🌡️ Temperature: {self.controller.model.get_temperature()}°C", 
                                         style='Status.TLabel')
        self.temperature_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.time_label = ttk.Label(status_frame, 
                                  text=f"🕐 System Time: {self.controller.model.get_SystemTimeSTR()}", 
                                  style='Status.TLabel')
        self.time_label.grid(row=3, column=0, sticky="w", pady=5)

        # Message frame with modern styling
        message_frame = ttk.LabelFrame(self.main_frame, text="💬 Messages", padding=15)
        message_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        message_frame.columnconfigure(0, weight=1)
        
        self.message_label = ttk.Label(message_frame, text=self.controller.model.get_message(), 
                                     style='Message.TLabel', foreground="#27ae60")
        self.message_label.grid(row=0, column=0, sticky="w")

        # Control buttons frame with better styling
        control_frame = ttk.LabelFrame(self.main_frame, text="🎛️ Control", padding=15)
        control_frame.grid(row=3, column=0, sticky="ew")
        
        # Configure button grid for better spacing
        control_frame.columnconfigure((0, 1, 2), weight=1)
        
        self.refresh_button = ttk.Button(control_frame, text="🔄 Refresh Data", 
                                       command=self.refresh_data, style='Action.TButton')
        self.refresh_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.simulate_button = ttk.Button(control_frame, text="🎲 Simulate Readings", 
                                        command=self.simulate_readings, style='Action.TButton')
        self.simulate_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.analytics_button = ttk.Button(control_frame, text="📊 Analytics Data", 
                                         command=self.open_analytics, style='Action.TButton')
        self.analytics_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    def configure_styles(self):
        """Configure modern styling for the application"""
        # Configure the theme
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Header.TLabel', 
                           font=('Segoe UI', 18, 'bold'),
                           foreground='#2c3e50')
        
        self.style.configure('Status.TLabel',
                           font=('Segoe UI', 11),
                           foreground='#34495e')
        
        self.style.configure('Message.TLabel',
                           font=('Segoe UI', 12, 'bold'))
        

        
        self.style.configure('Action.TButton',
                           font=('Segoe UI', 10),
                           padding=(15, 8))

    def refresh_data(self):
        """Refreshes displayed data"""
        self.moisture_label.config(text=f"💧 Moisture: {self.controller.model.get_moisture()}%")
        self.light_label.config(text=f"☀️ Light: {self.controller.model.get_light()}%")
        self.temperature_label.config(text=f"🌡️ Temperature: {self.controller.model.get_temperature()}°C")
        self.time_label.config(text=f"🕐 System Time: {self.controller.model.get_SystemTimeSTR()}")
        
    def simulate_readings(self):
        """Simulates new sensor readings"""
        self.controller.model.simulate_sensor_readings()
        self.refresh_data()
        self.update_message_based_on_conditions()
        
    def update_message_based_on_conditions(self):
        """Updates message based on plant conditions"""
        moisture = self.controller.model.get_moisture()
        light = self.controller.model.get_light()
        temperature = self.controller.model.get_temperature()
        
        if moisture < 30:
            message = "⚠️ Plant needs watering!"
            color = "red"
        elif light < 40:
            message = "💡 Plant needs more light!"
            color = "orange"
        elif temperature < 18 or temperature > 26:
            message = "🌡️ Temperature is not optimal!"
            color = "orange"
        else:
            message = "✅ Plant is feeling good!"
            color = "green"
            
        self.message_label.config(text=message, foreground=color)
    
    def open_analytics(self):
        """Opens analytics data window"""
        from .analytics_window import AnalyticsWindow
        AnalyticsWindow(self.master, self.controller.model.database)