# NASDAQ Stock Analyzer

A Python GUI application for analyzing NASDAQ stocks with customizable date ranges and view options.

## Features

- Search for stocks by symbol
- Analyze stock performance with interactive charts
- Select custom date ranges using a calendar interface
- View performance in daily, weekly, or monthly formats
- Visualize price changes with color-coded bar charts
- See average performance with trend lines

## Installation

1. Clone this repository or download the source code

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

## Usage

1. **Search for a Stock**
   - Click the "Search Stock" button
   - Enter a valid stock symbol (e.g., AAPL, MSFT, GOOGL)
   - Click "Submit"

2. **Analyze Stock Performance**
   - After selecting a stock, the analysis will run automatically
   - Alternatively, click the "Analysis" button to refresh the chart

3. **Select a Date Range**
   - Click the "Range" button
   - Choose "From" and "To" dates using the calendar
   - Click "Apply" to update the chart

4. **Change View Type**
   - Use the "View Type" dropdown to select:
     - Daily: Shows daily price changes
     - Weekly: Shows weekly price changes
     - Monthly: Shows monthly price changes

## Data Visualization

- **Green bars** indicate positive price changes
- **Red bars** indicate negative price changes
- **Blue dashed line** shows the average change over the selected period

## Requirements

- Python 3.6+
- Tkinter (usually comes with Python)
- tkcalendar
- matplotlib
- yfinance
- pandas
- numpy