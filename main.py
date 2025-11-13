import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from data_analyzer import WasteDataAnalyzer
from waste_classifier import WasteClassifier
from PIL import Image, ImageTk

class WasteManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Waste Classification & Analysis System")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.classifier = WasteClassifier()
        self.analyzer = WasteDataAnalyzer()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_classification_tab()
        self.create_analytics_tab()
        self.create_prediction_tab()
        
    def create_classification_tab(self):
        """Tab for image classification"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Image Classification")
        
        # Title
        title = tk.Label(tab, text="Waste Image Classification", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # Image display frame
        self.img_frame = tk.Frame(tab, width=400, height=400, bg='gray')
        self.img_frame.pack(pady=10)
        self.img_frame.pack_propagate(False)
        
        self.img_label = tk.Label(self.img_frame, text="No image loaded", 
                                 bg='gray', fg='white')
        self.img_label.pack(expand=True)
        
        # Buttons
        btn_frame = tk.Frame(tab)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Select Image", command=self.load_image,
                 bg='#4CAF50', fg='white', padx=20, pady=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Classify", command=self.classify_image,
                 bg='#2196F3', fg='white', padx=20, pady=10).pack(side='left', padx=5)
        
        # Result display
        self.result_label = tk.Label(tab, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        self.selected_image = None
        
    def create_analytics_tab(self):
        """Tab for data analytics and visualization"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Waste Analytics")
        
        # Control panel
        control_frame = tk.Frame(tab)
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Select Zone:", font=("Arial", 12)).pack(side='left', padx=5)
        
        self.zone_var = tk.StringVar()
        zones = self.analyzer.get_all_zones()
        self.zone_combo = ttk.Combobox(control_frame, textvariable=self.zone_var, 
                                       values=zones, state='readonly')
        self.zone_combo.pack(side='left', padx=5)
        self.zone_combo.current(0)
        
        tk.Button(control_frame, text="Show Trends", command=self.show_trends,
                 bg='#FF9800', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(control_frame, text="Show Distribution", command=self.show_distribution,
                 bg='#9C27B0', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        # Chart frame
        self.chart_frame = tk.Frame(tab)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_prediction_tab(self):
        """Tab for predictive analysis"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Predictions")
        
        # Control panel
        control_frame = tk.Frame(tab)
        control_frame.pack(pady=20)
        
        tk.Label(control_frame, text="Select Zone:", font=("Arial", 12)).pack(side='left', padx=5)
        
        self.pred_zone_var = tk.StringVar()
        zones = self.analyzer.get_all_zones()
        pred_combo = ttk.Combobox(control_frame, textvariable=self.pred_zone_var,
                                  values=zones, state='readonly')
        pred_combo.pack(side='left', padx=5)
        pred_combo.current(0)
        
        tk.Label(control_frame, text="Days:", font=("Arial", 12)).pack(side='left', padx=5)
        self.days_var = tk.StringVar(value="7")
        tk.Entry(control_frame, textvariable=self.days_var, width=5).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="Predict", command=self.show_predictions,
                 bg='#F44336', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        # Prediction chart frame
        self.pred_chart_frame = tk.Frame(tab)
        self.pred_chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_image(self):
        """Load image for classification"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.selected_image = file_path
            # Display image
            img = Image.open(file_path)
            img.thumbnail((380, 380))
            photo = ImageTk.PhotoImage(img)
            self.img_label.configure(image=photo, text="")
            self.img_label.image = photo
            self.result_label.config(text="")
    
    def classify_image(self):
        """Classify the loaded image"""
        if not self.selected_image:
            messagebox.showwarning("No Image", "Please select an image first!")
            return
        
        try:
            waste_type, confidence = self.classifier.predict(self.selected_image)
            result_text = f"Classification: {waste_type}\nConfidence: {confidence:.2f}%"
            color = '#4CAF50' if waste_type == 'Biodegradable' else '#FF5722'
            self.result_label.config(text=result_text, fg=color)
        except Exception as e:
            messagebox.showerror("Error", f"Classification failed: {str(e)}")
    
    def show_trends(self):
        """Show waste generation trends"""
        zone = self.zone_var.get()
        data = self.analyzer.get_trend_data(zone)
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create new chart
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(data['Date'], data['Waste_kg'], marker='o', linewidth=2, color='#2196F3')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Waste (kg)', fontsize=12)
        ax.set_title(f'Waste Generation Trend - {zone}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def show_distribution(self):
        """Show waste type distribution pie chart"""
        zone = self.zone_var.get()
        distribution = self.analyzer.get_waste_distribution(zone)
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create pie chart
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        colors = ['#4CAF50', '#FF5722']
        ax.pie(distribution.values(), labels=distribution.keys(), autopct='%1.1f%%',
               colors=colors, startangle=90, textprops={'fontsize': 12})
        ax.set_title(f'Waste Distribution - {zone}', fontsize=14, fontweight='bold')
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def show_predictions(self):
        """Show future waste predictions"""
        zone = self.pred_zone_var.get()
        try:
            days = int(self.days_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of days!")
            return
        
        predictions = self.analyzer.predict_future_waste(zone, days)
        historical_data = self.analyzer.get_trend_data(zone)
        
        # Clear previous chart
        for widget in self.pred_chart_frame.winfo_children():
            widget.destroy()
        
        # Create prediction chart
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Plot historical data
        ax.plot(historical_data['Date'], historical_data['Waste_kg'], 
               marker='o', label='Historical', linewidth=2, color='#2196F3')
        
        # Plot predictions
        pred_dates = [p[0] for p in predictions]
        pred_values = [p[1] for p in predictions]
        ax.plot(pred_dates, pred_values, marker='s', label='Predicted', 
               linewidth=2, linestyle='--', color='#FF9800')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Waste (kg)', fontsize=12)
        ax.set_title(f'Waste Prediction - {zone} (Next {days} days)', 
                    fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, self.pred_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = WasteManagementApp(root)
    root.mainloop()
