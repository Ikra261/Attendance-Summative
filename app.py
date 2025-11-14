import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, ui, render, reactive

# ---- Load data globally for UI choices ----
attendance_data = pd.read_csv(
    "/Users/ikrashoaib/Desktop/Data Science & ML/Assignments/Attendance-Summative/attendance_anonymised-1.csv"
)
attendance_data.columns = attendance_data.columns.str.strip()
attendance_data.rename(columns={
    'Person Code': 'Person code',
    'Unit Instance Code': 'Module Code',
    'Calocc Code': 'Year',
    'Surname': 'Surname',
    'Forename': 'Forename',
    'Long Description': 'Module Name',
    'Register Event ID': 'Event ID',
    'Object ID': 'Object ID',
    'Register Event Slot ID': 'Event Slot ID',
    'Planned Start Date': 'Date',
    'is Positive': 'Has Attended',
    'Postive Marks': 'Attended',
    'Negative Marks': 'NotAttended',
    'Usage Code': 'Attended Code'
}, inplace=True)
attendance_data["Date"] = pd.to_datetime(attendance_data["Date"])

module_choices = sorted(attendance_data["Module Name"].unique())

# ---------------- UI ----------------
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "module",
            "Select a module:",
            choices=module_choices,   
            selected='Arabic'
        ),
        ui.input_slider(
            "size",
            "Line thickness",
            min=1, max=5, value=2
        ),
        title="Filters"
    ),
    ui.h1("Module Attendance Over Time"),
    ui.output_plot("attendance_plot")
)

# ---------------- Server ----------------
def server(input, output, session):

    # ---- Reactive: filtered data for selected module ----
    @reactive.Calc
    def filtered_data():
        return attendance_data[attendance_data["Module Name"] == input.module()]

    # ---- Render plot ----
    @output
    @render.plot
    def attendance_plot():
        data = filtered_data()
        attendance_rate = data.groupby("Date")["Attended"].mean()
        
    
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(attendance_rate.index, attendance_rate.values, linewidth=input.size())
        ax.set_title(f"{input.module()} Attendance Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Attendance Rate")
        ax.set_ylim(0, 1)
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

# ---------------- Run App ----------------
app = App(app_ui, server)



