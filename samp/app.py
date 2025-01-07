from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__, static_folder='static')

# Load and prepare data
data = pd.read_csv("E:/covid data sets/covid_19_india.csv")
covid_df = pd.DataFrame(data)
covid_df['Active_Cases'] = covid_df['Confirmed'] - (covid_df['Cured'] + covid_df['Deaths'])

# Convert 'Date' to datetime for proper plotting
covid_df['Date'] = pd.to_datetime(covid_df['Date'], errors='coerce')

# Statewise Pivot Table
statewise = pd.pivot_table(covid_df, values=["Confirmed", "Deaths", "Cured"], 
                           index="State/UnionTerritory", aggfunc=max)

# Add Recovery and Mortality Rates
statewise["Recovery Rate"] = statewise["Cured"] * 100 / statewise["Confirmed"]
statewise["Mortality Rate"] = statewise["Deaths"] * 100 / statewise["Confirmed"]
statewise = statewise.sort_values(by="Confirmed", ascending=False)

@app.route('/')
def home():
    table_html = statewise.to_html(classes="table table-striped", index=True)
    return render_template("index.html", table_html=table_html)

@app.route('/vaccine')
def vaccine_data():
    vaccine_df = pd.read_csv("E:/covid data sets/covid_vaccine_statewise.csv")
    vaccine_table_html = vaccine_df.head(11).to_html(classes="table table-striped", index=False)
    return render_template("vaccine.html", vaccine_table_html=vaccine_table_html)

@app.route('/statewise')
def statewise_data():
    styled_html = statewise.style.background_gradient(cmap="twilight").to_html()
    return render_template("statewise.html", styled_html=styled_html)

@app.route('/top10active')
def top10_active():
    # Generate the plot
    top_10_active_cases = covid_df.groupby(by='State/UnionTerritory').max()[['Active_Cases', 'Date']] \
        .sort_values(by=['Active_Cases'], ascending=False).reset_index()
    
    plt.figure(figsize=(16, 9))
    sns.barplot(
        data=top_10_active_cases.iloc[:10], 
        y="Active_Cases", 
        x="State/UnionTerritory", 
        linewidth=2, 
        edgecolor='black', 
        palette='Dark2'
    )
    plt.title("Top 10 States with Most Active Cases in India", size=25)
    plt.xlabel("States")
    plt.ylabel("Total Active Cases")
    plot_path = "static/top10_active_cases.png"
    plt.savefig(plot_path)  # Save the plot as an image
    plt.close()  # Close the plot to free memory
    return render_template("top10active.html", plot_path=plot_path)

@app.route('/top10deaths')
def top10_deaths():
    # Generate the plot
    top_10_deaths = covid_df.groupby(by='State/UnionTerritory').max()[['Deaths', 'Date']] \
        .sort_values(by=['Deaths'], ascending=False).reset_index()
    
    plt.figure(figsize=(18, 5))
    sns.barplot(
        data=top_10_deaths.iloc[:12], 
        y="Deaths", 
        x="State/UnionTerritory", 
        linewidth=2, 
        edgecolor='black', 
        palette='viridis'
    )
    plt.title("Top 10 States with Most Deaths", size=25)
    plt.xlabel("States")
    plt.ylabel("Total Death Cases")
    
    # Ensure the static directory exists
    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    plot_path = os.path.join(static_dir, "top10_deaths.png")
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free memory
    return render_template("top10deaths.html", plot_path="static/top10_deaths.png")

@app.route('/top5states')
def top5_states():
    # Generate the line plot
    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(
        data=covid_df[covid_df['State/UnionTerritory'].isin(
            ['Maharashtra', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Uttar Pradesh']
        )],
        x='Date',
        y='Active_Cases',
        hue='State/UnionTerritory'
    )
    ax.set_title("Top 5 Affected States in India", size=16)
    plt.xlabel("Date")
    plt.ylabel("Active Cases")

    # Ensure the static directory exists
    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save the plot in the static directory
    plot_path = os.path.join(static_dir, "top5_states.png")
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free memory
    
    return render_template("top5states.html", plot_path="static/top5_states.png")

if __name__ == "__main__":
    app.run(debug=True)
