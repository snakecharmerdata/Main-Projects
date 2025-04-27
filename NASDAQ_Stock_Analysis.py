import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Rectangle, Patch
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from scipy import stats

class StockAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NASDAQ Stock Analyzer")
        self.root.geometry("1200x800")  # Increased window size for better visualization
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.stock_symbol = ""
        self.start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')  # Default to 1 year ago
        self.end_date = datetime.now().strftime('%Y-%m-%d')  # Default to today
        self.view_type = "Weekly"  # Default view type
        self.stock_data = None
        self.chart_type = "Price Change"  # Default chart type
        
        # Chart types available in the application
        self.chart_types = [
            "Price Change",
            "Candlestick",
            "Moving Averages",
            "Volume Analysis",
            "Volatility",
            "Price Distribution",
            "Return Distribution",
            "Correlation with Index"
        ]

        # Create frames
        self.create_search_frame()
        self.create_controls_frame()
        self.create_chart_selection_frame()  # New frame for chart type selection
        self.create_graph_frame()

    def create_search_frame(self):
        # Search frame
        search_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        search_frame.pack(fill="x")

        # Search button
        search_btn = tk.Button(search_frame, text="Search Stock", command=self.open_search, 
                              bg="#4CAF50", fg="blue", padx=10, pady=5)
        search_btn.pack(side="left", padx=10)

        # Display selected stock
        self.stock_label = tk.Label(search_frame, text="No stock selected", bg="#f0f0f0", font=("Arial", 12))
        self.stock_label.pack(side="left", padx=10)

    def create_controls_frame(self):
        # Controls frame
        controls_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        controls_frame.pack(fill="x")

        # Analysis button
        analysis_btn = tk.Button(controls_frame, text="Analysis", command=self.analyze_stock,
                                bg="#2196F3", fg="blue", padx=10, pady=5)
        analysis_btn.pack(side="left", padx=10)

        # Range button
        range_btn = tk.Button(controls_frame, text="Range", command=self.open_date_range,
                             bg="#FFC107", fg="blue", padx=10, pady=5)
        range_btn.pack(side="left", padx=10)

        # Date range labels
        date_frame = tk.Frame(controls_frame, bg="#f0f0f0")
        date_frame.pack(side="left", padx=10)
        
        tk.Label(date_frame, text="From:", bg="#f0f0f0").pack(side="left")
        self.from_date_label = tk.Label(date_frame, text=self.start_date, bg="orange", width=10)
        self.from_date_label.pack(side="left", padx=5)
        
        tk.Label(date_frame, text="To:", bg="#f0f0f0").pack(side="left")
        self.to_date_label = tk.Label(date_frame, text=self.end_date, bg="orange", width=10)
        self.to_date_label.pack(side="left", padx=5)

        # View Type button with dropdown
        view_frame = tk.Frame(controls_frame, bg="#f0f0f0")
        view_frame.pack(side="left", padx=10)
        
        view_btn = tk.Button(view_frame, text="View Type", command=self.toggle_view_menu,
                            bg="#9C27B0", fg="blue", padx=10, pady=5)
        view_btn.pack(side="left")
        
        self.view_type_var = tk.StringVar()
        self.view_type_var.set(self.view_type)
        self.view_menu = tk.OptionMenu(view_frame, self.view_type_var, "Daily", "Weekly", "Monthly", 
                                      command=self.change_view_type)
        self.view_menu.pack(side="left", padx=5)

    def create_graph_frame(self):
        # Graph frame
        self.graph_frame = tk.Frame(self.root, bg="white", padx=10, pady=10)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial message in graph area
        self.message_label = tk.Label(self.graph_frame, text="Search for a stock to view analysis",
                                     bg="white", font=("Arial", 14))
        self.message_label.pack(expand=True)

    def open_search(self):
        # Create a popup window for search
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Stock")
        search_window.geometry("300x150")
        search_window.configure(bg="white")
        search_window.grab_set()  # Make window modal
        
        tk.Label(search_window, text="Enter Stock Symbol:", bg="white").pack(pady=10)
        
        # Search entry with white background
        search_entry = tk.Entry(search_window, bg="white", width=20)
        search_entry.pack(pady=10)
        search_entry.focus_set()
        
        # Submit button
        submit_btn = tk.Button(search_window, text="Submit", 
                              command=lambda: self.set_stock(search_entry.get(), search_window))
        submit_btn.pack(pady=10)

    def set_stock(self, symbol, window=None):
        if symbol:
            self.stock_symbol = symbol.upper()
            self.stock_label.config(text=f"Selected Stock: {self.stock_symbol}")
            
            # Close the search window if it exists
            if window:
                window.destroy()
                
            # Automatically analyze the stock
            self.analyze_stock()

    def open_date_range(self):
        # Create a popup window for date selection
        date_window = tk.Toplevel(self.root)
        date_window.title("Select Date Range")
        date_window.geometry("600x380")  # Increased size for better calendar visibility
        date_window.configure(bg="white")
        date_window.grab_set()  # Make window modal
        
        # Main container for the date picker
        main_frame = tk.Frame(date_window, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create frame for calendars side by side
        calendars_frame = tk.Frame(main_frame, bg="white")
        calendars_frame.pack(fill="both", expand=True)
        
        # From date calendar
        from_frame = tk.LabelFrame(calendars_frame, text="From Date", bg="white", padx=10, pady=10)
        from_frame.grid(row=0, column=0, padx=20)
        
        # Use larger Calendar widget instead of DateEntry for better visibility
        from_cal = Calendar(from_frame, selectmode='day', date_pattern='yyyy-mm-dd',
                           background='darkblue', foreground='white', 
                           borderwidth=2, year=int(self.start_date[:4]), 
                           month=int(self.start_date[5:7]), day=int(self.start_date[8:]))
        from_cal.pack(padx=10, pady=10)
        
        # To date calendar
        to_frame = tk.LabelFrame(calendars_frame, text="To Date", bg="white", padx=10, pady=10)
        to_frame.grid(row=0, column=1, padx=20)
        
        to_cal = Calendar(to_frame, selectmode='day', date_pattern='yyyy-mm-dd',
                         background='orange', foreground='white', 
                         borderwidth=2, year=int(self.end_date[:4]), 
                         month=int(self.end_date[5:7]), day=int(self.end_date[8:]))
        to_cal.pack(padx=10, pady=10)
        
        # Buttons frame at the bottom
        buttons_frame = tk.Frame(main_frame, bg="white")
        buttons_frame.pack(pady=20)
        
        # Apply button next to calendars
        apply_btn = tk.Button(buttons_frame, text="Apply", command=lambda: self.set_date_range(
                              from_cal.get_date(),
                              to_cal.get_date(),
                              date_window),
                             bg="#4CAF50", fg="black", padx=20, pady=5)
        apply_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(buttons_frame, text="Cancel", command=date_window.destroy,
                              bg="#F44336", fg="black", padx=20, pady=5)
        cancel_btn.pack(side="left", padx=10)

    def set_date_range(self, start, end, window=None):
        self.start_date = start
        self.end_date = end
        
        # Update date labels
        self.from_date_label.config(text=self.start_date)
        self.to_date_label.config(text=self.end_date)
        
        # Close the date window if it exists
        if window:
            window.destroy()
            
        # Reanalyze the stock with new date range if a stock is selected
        if self.stock_symbol:
            self.analyze_stock()

    def toggle_view_menu(self):
        # This function is just a placeholder for the View Type button
        # The actual menu is already visible
        pass

    def change_view_type(self, view_type):
        self.view_type = view_type
        
        # Reanalyze the stock with new view type if a stock is selected
        if self.stock_symbol and self.stock_data is not None:
            self.update_graph()

    def analyze_stock(self):
        if not self.stock_symbol:
            tk.messagebox.showinfo("Info", "Please select a stock first.")
            self.open_search()
            return
            
        try:
            # Clear graph frame
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
                
            # Show loading message
            loading_label = tk.Label(self.graph_frame, text="Loading data...", bg="white", font=("Arial", 14))
            loading_label.pack(expand=True)
            self.root.update()
            
            # Fetch stock data
            self.stock_data = yf.download(self.stock_symbol, start=self.start_date, end=self.end_date)
            
            if self.stock_data.empty:
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()
                error_label = tk.Label(self.graph_frame, text=f"No data available for {self.stock_symbol}", 
                                      bg="white", font=("Arial", 14))
                error_label.pack(expand=True)
                return
                
            # Update graph
            self.update_graph()
            
        except Exception as e:
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            error_label = tk.Label(self.graph_frame, text=f"Error: {str(e)}", 
                                  bg="white", font=("Arial", 14))
            error_label.pack(expand=True)

    def create_chart_selection_frame(self):
        # Chart selection frame
        chart_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        chart_frame.pack(fill="x")
        
        # Chart type label
        tk.Label(chart_frame, text="Chart Type:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left", padx=10)
        
        # Chart type dropdown
        self.chart_type_var = tk.StringVar()
        self.chart_type_var.set(self.chart_type)
        
        chart_dropdown = ttk.Combobox(chart_frame, textvariable=self.chart_type_var, 
                                     values=self.chart_types, width=20, state="readonly")
        chart_dropdown.pack(side="left", padx=5)
        chart_dropdown.bind("<<ComboboxSelected>>", self.change_chart_type)
        
        # Info button for chart descriptions
        info_btn = tk.Button(chart_frame, text="?", command=self.show_chart_info, 
                            bg="#607D8B", fg="white", width=2, height=1, font=("Arial", 10, "bold"))
        info_btn.pack(side="left", padx=5)
        
    def change_chart_type(self, event=None):
        self.chart_type = self.chart_type_var.get()
        if self.stock_symbol and self.stock_data is not None:
            self.update_graph()
            
    def show_chart_info(self):
        # Dictionary of chart descriptions
        chart_info = {
            "Price Change": "Shows percentage price changes over time with color-coded bars.",
            "Candlestick": "Traditional candlestick chart showing open, high, low, close prices.",
            "Moving Averages": "Price chart with short and long-term moving averages.",
            "Volume Analysis": "Analysis of trading volume with price overlay.",
            "Volatility": "Historical volatility measurement using standard deviation.",
            "Price Distribution": "Histogram showing the distribution of closing prices.",
            "Return Distribution": "Distribution of daily returns with normal curve overlay.",
            "Correlation with Index": "Correlation between the stock and a market index."
        }
        
        # Create info window
        info_window = tk.Toplevel(self.root)
        info_window.title("Chart Type Information")
        info_window.geometry("500x400")
        info_window.configure(bg="white")
        
        # Create a frame for the content
        content_frame = tk.Frame(info_window, bg="white", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Add a title
        tk.Label(content_frame, text="Chart Types Explanation", 
                bg="white", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Create a frame for the chart descriptions
        desc_frame = tk.Frame(content_frame, bg="white")
        desc_frame.pack(fill="both", expand=True)
        
        # Add each chart type and its description
        row = 0
        for chart, desc in chart_info.items():
            tk.Label(desc_frame, text=chart + ":", bg="white", 
                    font=("Arial", 10, "bold"), anchor="w").grid(row=row, column=0, sticky="w", pady=5)
            
            # Use Text widget for description to enable wrapping
            text_widget = tk.Text(desc_frame, wrap="word", height=2, width=40, 
                                 bg="white", bd=0, font=("Arial", 9))
            text_widget.grid(row=row, column=1, sticky="w", pady=5, padx=5)
            text_widget.insert("1.0", desc)
            text_widget.config(state="disabled")  # Make read-only
            
            row += 1
        
        # Close button
        tk.Button(content_frame, text="Close", command=info_window.destroy,
                 bg="#4CAF50", fg="white", padx=20, pady=5).pack(pady=20)

    def update_graph(self):
        if self.stock_data is None or self.stock_data.empty:
            return
            
        # Clear graph frame
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Resample data based on view type
        if self.view_type == "Daily":
            df = self.stock_data.copy()  # Daily data is already in this format
            title_freq = "Daily"
        elif self.view_type == "Weekly":
            df = self.stock_data.resample('W').last()
            title_freq = "Weekly"
        elif self.view_type == "Monthly":
            df = self.stock_data.resample('M').last()
            title_freq = "Monthly"
        
        # Different chart types
        if self.chart_type == "Candlestick":
            # Candlestick chart handles its own display
            self.plot_candlestick(df, None, title_freq)
            return  # Return early as plot_candlestick handles its own embedding
        elif self.chart_type == "Volume Analysis":
            # Volume analysis handles its own display
            self.plot_volume_analysis(df, None, title_freq)
            return  # Return early as plot_volume_analysis handles its own embedding
        elif self.chart_type == "Price Distribution":
            # Price distribution handles its own display
            self.plot_price_distribution(df, None, title_freq)
            return  # Return early as plot_price_distribution handles its own embedding
        elif self.chart_type == "Correlation with Index":
            # Show loading message
            loading_label = tk.Label(self.graph_frame, text="Loading S&P 500 data for correlation analysis...", 
                                    bg="white", font=("Arial", 12))
            loading_label.pack(expand=True)
            self.root.update()
            
            # Get correlation plot
            fig, ax = self.plot_correlation(df, None, title_freq)
            
            # Remove loading label
            loading_label.destroy()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
            canvas.draw()
            
            # Add explanation text below the graph
            explanation_frame = tk.Frame(self.graph_frame, bg="white")
            explanation_frame.pack(fill="x", pady=5)
            
            explanation_text = (
                "Correlation measures the strength of the relationship between two variables (ranges from -1 to 1).\n"
                "Beta measures the volatility of a stock relative to the market (S&P 500)."
            )
            
            explanation_label = tk.Label(explanation_frame, text=explanation_text, 
                                        bg="white", font=("Arial", 10), justify="left")
            explanation_label.pack(pady=5)
        else:
            # For all other chart types, create figure and axis
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            
            if self.chart_type == "Price Change":
                self.plot_price_change(df, ax, title_freq)
            elif self.chart_type == "Moving Averages":
                self.plot_moving_averages(df, ax, title_freq)
            elif self.chart_type == "Volatility":
                self.plot_volatility(df, ax, title_freq)
            elif self.chart_type == "Return Distribution":
                self.plot_return_distribution(df, ax, title_freq)
            
            # Rotate date labels if applicable
            if hasattr(ax, 'xaxis') and hasattr(ax.xaxis, 'get_majorticklabels'):
                for label in ax.get_xticklabels():
                    label.set_rotation(45)
            
            # Tight layout
            fig.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
            canvas.draw()
        
    def plot_price_change(self, df, ax, title_freq):
        # Calculate price changes
        df['Change'] = df['Close'].pct_change() * 100
        
        # Remove the first row which has NaN for Change
        df = df.dropna()
        
        # Plot bar chart
        bars = ax.bar(df.index, df['Change'], color=['green' if x >= 0 else 'red' for x in df['Change']])
        
        # Plot average line
        avg_change = df['Change'].mean()
        ax.axhline(y=avg_change, color='blue', linestyle='--', label=f'Avg Change: {avg_change:.2f}%')
        
        # Set titles and labels
        ax.set_title(f'{self.stock_symbol} {title_freq} Performance ({self.start_date} to {self.end_date})')
        ax.set_xlabel('Date')
        ax.set_ylabel('Percentage Change (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def plot_candlestick(self, df, ax, title_freq):
        """
        Plot a candlestick chart showing OHLC prices.
        """
        # Import Rectangle from matplotlib.patches
        from matplotlib.patches import Rectangle, Patch
        
        # Clear the graph frame first
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
                
        # Create a new figure with 2 subplots
        fig = Figure(figsize=(10, 8))
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        
        # Format dates for matplotlib
        dates = mdates.date2num(df.index.to_pydatetime())
        
        # Plot candlesticks
        width = 0.6  # default width
        if len(df) > 50:
            width = 0.4  # thinner width for many data points
        if len(df) > 100:
            width = 0.2  # even thinner for lots of data points
        
        # Process each candlestick individually to avoid array shape issues
        for i in range(len(df)):
            try:
                date = float(dates[i])  # Convert to float to ensure scalar value
                
                # Check if the data is numeric before converting
                open_price = float(df['Open'].iloc[i])
                high_price = float(df['High'].iloc[i])
                low_price = float(df['Low'].iloc[i])
                close_price = float(df['Close'].iloc[i])
                    
                # Determine if it's an up or down candle
                if close_price >= open_price:
                    # Green candle (up)
                    color = 'green'
                    body_bottom = open_price
                    body_height = close_price - open_price
                else:
                    # Red candle (down)
                    color = 'red'
                    body_bottom = close_price
                    body_height = open_price - close_price
                
                # Plot the body
                rect = Rectangle(
                    (date - width/2, body_bottom),
                    width, body_height,
                    fill=True, color=color
                )
                ax1.add_patch(rect)
                
                # Plot the upper and lower wicks - use scalar values for coordinates
                ax1.plot(
                    [date, date],  # Already converted to float
                    [high_price, max(open_price, close_price)],  # Already converted to float
                    color='black', 
                    linewidth=1.0  # Explicitly use a scalar float
                )
                ax1.plot(
                    [date, date],  # Already converted to float
                    [min(open_price, close_price), low_price],  # Already converted to float
                    color='black', 
                    linewidth=1.0  # Explicitly use a scalar float
                )
            except (ValueError, TypeError):
                # Skip this candlestick if any of the OHLC values are not numeric
                continue
        
        # Format date axis
        date_format = mdates.DateFormatter('%Y-%m-%d')
        ax1.xaxis.set_major_formatter(date_format)
        
        # Plot volume - create colors list with explicit float conversion
        volume_colors = []
        valid_volumes = []
        valid_dates = []
        
        for i in range(len(df)):
            try:
                close_val = float(df['Close'].iloc[i])
                open_val = float(df['Open'].iloc[i])
                volume_val = float(df['Volume'].iloc[i])
                
                volume_colors.append('green' if close_val >= open_val else 'red')
                valid_volumes.append(volume_val)
                valid_dates.append(float(dates[i]))
            except (ValueError, TypeError):
                # Skip this volume bar if any values are not numeric
                continue
        
        # Only plot volume if we have valid data
        if valid_volumes:
            ax2.bar(valid_dates, valid_volumes, color=volume_colors, width=width, alpha=0.8)
            
            # Calculate average volume
            avg_volume = sum(valid_volumes) / len(valid_volumes)
            ax2.axhline(y=avg_volume, color='blue', linestyle='--', label=f'Avg Volume')
            
            # Format volume with K, M, B suffixes
            def volume_formatter(x, pos):
                if x >= 1e9:
                    return f'{x*1e-9:.1f}B'
                elif x >= 1e6:
                    return f'{x*1e-6:.1f}M'
                elif x >= 1e3:
                    return f'{x*1e-3:.1f}K'
                else:
                    return f'{x:.0f}'
                        
            ax2.yaxis.set_major_formatter(FuncFormatter(volume_formatter))
        
        # Set titles and labels
        ax1.set_title(f'{self.stock_symbol} {title_freq} Candlestick Chart ({self.start_date} to {self.end_date})')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, alpha=0.3)
        
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Volume')
        ax2.grid(True, alpha=0.3)
        
        # Legend for candlestick colors
        green_patch = Patch(color='green', label='Price Up')
        red_patch = Patch(color='red', label='Price Down')
        ax1.legend(handles=[green_patch, red_patch])
        
        # Rotate date labels
        for label in ax2.get_xticklabels():
            label.set_rotation(45)
        
        # Format y-axis to show dollar sign
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'${y:.2f}'))
        
        # Adjust layout
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        
        # Return None to indicate that we've handled the display
        return None, None
    def plot_moving_averages(self, df, ax, title_freq):
        # Calculate moving averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        
        # Plot price and moving averages
        ax.plot(df.index, df['Close'], label='Close Price', color='black', alpha=0.6)
        ax.plot(df.index, df['MA20'], label='20-day MA', color='blue')
        ax.plot(df.index, df['MA50'], label='50-day MA', color='green')
        ax.plot(df.index, df['MA200'], label='200-day MA', color='red')
        
        # Set titles and labels
        ax.set_title(f'{self.stock_symbol} {title_freq} Moving Averages ({self.start_date} to {self.end_date})')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format y-axis to show dollar sign
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'${y:.2f}'))
        
    def plot_volume_analysis(self, df, ax, title_freq):
        """
        Plot volume analysis with price overlay.
        """
        # Clear the graph frame first
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        # Create a new figure with 2 subplots
        fig = Figure(figsize=(10, 8))
        gs = fig.add_gridspec(2, 1, height_ratios=[2, 1])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        
        # Plot price on top subplot - handle non-numeric values
        valid_price_data = []
        valid_dates = []
        
        for i in range(len(df)):
            try:
                close_price = float(df['Close'].iloc[i])
                valid_price_data.append(close_price)
                valid_dates.append(df.index[i])
            except (ValueError, TypeError):
                # Skip non-numeric values
                continue
        
        if valid_price_data:
            ax1.plot(valid_dates, valid_price_data, label='Close Price', color='black')
        
        ax1.set_ylabel('Price ($)')
        ax1.set_title(f'{self.stock_symbol} {title_freq} Volume Analysis ({self.start_date} to {self.end_date})')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left')
        
        # Format y-axis to show dollar sign
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'${y:.2f}'))
        
        # Plot volume on bottom subplot with color based on price change
        valid_volume_data = []
        valid_volume_dates = []
        volume_colors = []
        
        for i in range(len(df)):
            try:
                close_val = float(df['Close'].iloc[i])
                open_val = float(df['Open'].iloc[i])
                volume_val = float(df['Volume'].iloc[i])
                
                valid_volume_data.append(volume_val)
                valid_volume_dates.append(df.index[i])
                
                if close_val >= open_val:
                    volume_colors.append('green')
                else:
                    volume_colors.append('red')
            except (ValueError, TypeError):
                # Skip non-numeric values
                continue
        
        if valid_volume_data:
            ax2.bar(valid_volume_dates, valid_volume_data, color=volume_colors, alpha=0.7)
            
            # Calculate average volume
            avg_volume = sum(valid_volume_data) / len(valid_volume_data)
            ax2.axhline(y=avg_volume, color='blue', linestyle='--', label=f'Avg Volume')
            
            # Add volume moving average if we have enough data points
            if len(valid_volume_data) >= 20:
                # Create a temporary DataFrame for the rolling calculation
                temp_df = pd.DataFrame({'Volume': valid_volume_data}, index=valid_volume_dates)
                temp_df['Volume_MA20'] = temp_df['Volume'].rolling(window=20).mean()
                
                # Plot the moving average
                ax2.plot(temp_df.index, temp_df['Volume_MA20'], color='orange', label='20-day MA')
        
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Volume')
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='upper left')
        
        # Format volume with K, M, B suffixes
        def volume_formatter(x, pos):
            if x >= 1e9:
                return f'{x*1e-9:.1f}B'
            elif x >= 1e6:
                return f'{x*1e-6:.1f}M'
            elif x >= 1e3:
                return f'{x*1e-3:.1f}K'
            else:
                return f'{x:.0f}'
                
        ax2.yaxis.set_major_formatter(FuncFormatter(volume_formatter))
        
        # Format date axis
        date_format = mdates.DateFormatter('%Y-%m-%d')
        ax2.xaxis.set_major_formatter(date_format)
        
        # Rotate date labels
        for label in ax2.get_xticklabels():
            label.set_rotation(45)
        
        # Adjust layout
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        
        # Return None to indicate that we've handled the display
        return None, None
        
    def plot_volatility(self, df, ax, title_freq):
        # Calculate daily returns
        df['Daily_Return'] = df['Close'].pct_change()
        
        # Calculate rolling volatility (standard deviation of returns)
        window = 21  # Approximately one month of trading days
        df['Volatility'] = df['Daily_Return'].rolling(window=window).std() * np.sqrt(252) * 100  # Annualized and in percentage
        
        # Plot volatility
        ax.plot(df.index, df['Volatility'], color='purple', linewidth=2)
        
        # Calculate and plot average volatility
        avg_vol = df['Volatility'].mean()
        ax.axhline(y=avg_vol, color='red', linestyle='--', label=f'Avg: {avg_vol:.2f}%')
        
        # Set titles and labels
        ax.set_title(f'{self.stock_symbol} {title_freq} Volatility ({self.start_date} to {self.end_date})')
        ax.set_xlabel('Date')
        ax.set_ylabel('Annualized Volatility (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_price_distribution(self, df, ax, title_freq):
        """
        Plot histogram showing the distribution of closing prices.
        """
        # Clear the graph frame first
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
                
        # Create a new figure
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Filter out non-numeric values and convert to list of floats
        valid_prices = []
        for i in range(len(df)):
            try:
                price = float(df['Close'].iloc[i])
                valid_prices.append(price)
            except (ValueError, TypeError):
                # Skip non-numeric values
                continue
        
        if not valid_prices:
            # If no valid prices, show an error message
            ax.text(0.5, 0.5, "No valid price data available for histogram", 
                   horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        else:
            # Create histogram of closing prices
            n, bins, patches = ax.hist(valid_prices, bins=30, alpha=0.7, color='blue', edgecolor='black')
            
            # Add vertical line for current price (last valid price)
            try:
                current_price = float(valid_prices[-1])
                ax.axvline(x=current_price, color='red', linestyle='--', 
                          label=f'Current: ${current_price:.2f}')
            except (IndexError, ValueError, TypeError):
                # No current price available or not numeric
                pass
            
            # Add vertical line for mean price
            try:
                mean_price = sum(valid_prices) / len(valid_prices)
                ax.axvline(x=mean_price, color='green', linestyle='--', 
                          label=f'Mean: ${mean_price:.2f}')
            except (ZeroDivisionError, ValueError, TypeError):
                # Error calculating mean
                pass
        
        # Set titles and labels
        ax.set_title(f'{self.stock_symbol} {title_freq} Price Distribution ({self.start_date} to {self.end_date})')
        ax.set_xlabel('Price ($)')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis to show dollar sign
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:.2f}'))
        
        # Adjust layout
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        
        # Return None to indicate that we've handled the display
        return None, None
        
    def plot_return_distribution(self, df, ax, title_freq):
        # Calculate daily returns
        df['Daily_Return'] = df['Close'].pct_change() * 100  # Convert to percentage
        df = df.dropna()  # Remove NaN values
        
        # Create histogram of returns
        n, bins, patches = ax.hist(df['Daily_Return'], bins=30, alpha=0.7, color='blue', edgecolor='black', density=True)
        
        # Fit normal distribution
        mu, std = stats.norm.fit(df['Daily_Return'])
        x = np.linspace(mu - 4*std, mu + 4*std, 100)
        p = stats.norm.pdf(x, mu, std)
        ax.plot(x, p, 'r--', linewidth=2, label=f'Normal: μ={mu:.2f}, σ={std:.2f}')
        
        # Add vertical line for mean return
        ax.axvline(x=mu, color='green', linestyle='--', label=f'Mean: {mu:.2f}%')
        
        # Add vertical line for zero return
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # Set titles and labels
        ax.set_title(f'{self.stock_symbol} {title_freq} Return Distribution ({self.start_date} to {self.end_date})')
        ax.set_xlabel('Daily Return (%)')
        ax.set_ylabel('Density')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_correlation(self, df, ax, title_freq):
        """
        Plot a scatter plot showing correlation between stock returns and market index.
        """
        # Create a new figure with a single subplot
        plt.close()  # Close the previous figure
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        try:
            # Download index data (S&P 500)
            index_symbol = "^GSPC"  # S&P 500
            index_data = yf.download(index_symbol, start=self.start_date, end=self.end_date)
            
            # Resample index data based on view type
            if self.view_type == "Weekly":
                index_data = index_data.resample('W').last()
            elif self.view_type == "Monthly":
                index_data = index_data.resample('M').last()
            
            # Calculate returns for both stock and index (as percentages)
            df['Stock_Return'] = df['Close'].pct_change() * 100
            index_data['Index_Return'] = index_data['Close'].pct_change() * 100
            
            # Align the data (removing any dates that don't exist in both)
            merged_data = pd.DataFrame({
                'Stock_Return': df['Stock_Return'],
                'Index_Return': index_data['Index_Return']
            }).dropna()
            
            # Calculate correlation
            correlation = merged_data['Stock_Return'].corr(merged_data['Index_Return'])
            
            # Create scatter plot
            ax.scatter(merged_data['Index_Return'], merged_data['Stock_Return'], alpha=0.6, color='blue')
            
            # Add regression line
            beta, alpha = np.polyfit(merged_data['Index_Return'], merged_data['Stock_Return'], 1)
            x = np.linspace(merged_data['Index_Return'].min(), merged_data['Index_Return'].max(), 100)
            y = beta * x + alpha
            ax.plot(x, y, 'r-', linewidth=2, label=f'β = {beta:.2f}, α = {alpha:.2f}, r = {correlation:.2f}')
            
            # Add zero lines
            ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
            
            # Set titles and labels
            ax.set_title(f'{self.stock_symbol} vs S&P 500 {title_freq} Correlation ({self.start_date} to {self.end_date})')
            ax.set_xlabel('S&P 500 Return (%)')
            ax.set_ylabel(f'{self.stock_symbol} Return (%)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Add annotation for beta interpretation
            beta_text = "More volatile than market" if beta > 1 else "Less volatile than market" if beta < 1 else "Same volatility as market"
            ax.annotate(f"Beta interpretation: {beta_text}", xy=(0.05, 0.05), xycoords='axes fraction', 
                       bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.3))
            
            # Adjust layout
            plt.tight_layout()
            
            return fig, ax
            
        except Exception as e:
            # In case of error, create a simple figure with error message
            ax.text(0.5, 0.5, f"Error retrieving correlation data:\n{str(e)}", 
                   horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            return fig, ax

def main():
    """
    Main function to run the NASDAQ Stock Analyzer application.
    """
    try:
        # Create the root window
        root = tk.Tk()
        
        # Create the application instance
        app = StockAnalyzerApp(root)
        
        # Start the main event loop
        root.mainloop()
    except Exception as e:
        # Show error message if application fails to start
        import traceback
        error_message = f"Error starting application: {str(e)}\n\n{traceback.format_exc()}"
        
        try:
            # Try to show error in GUI if possible
            tk.messagebox.showerror("Application Error", error_message)
        except:
            # Fall back to console output if GUI fails
            print("CRITICAL ERROR:")
            print(error_message)

# Run the application
if __name__ == "__main__":
    main()
