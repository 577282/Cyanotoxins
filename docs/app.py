from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Path to Excel file
EXCEL_FILE_PATH = 'static/data/cyanodatabase.xlsx'

# Dictionary to map toxin names to their KEGG URLs
TOXIN_URLS = {
    "Saxitoxins": "https://www.kegg.jp/entry/C13757",
    "Microcystins": "https://www.genome.jp/entry/C05371",
    "Anatoxin-a(s)": "https://www.genome.jp/entry/C19998",
    "Anatoxin-a": "https://www.genome.jp/entry/C10841",
    "Nodularin": "https://www.genome.jp/entry/C15713",
    "Cylindrospermopsin": "https://www.genome.jp/entry/C19999"

}

@app.route('/')
def view_tables():
    # Load the Excel file into pandas
    excel_data = pd.ExcelFile(EXCEL_FILE_PATH)
    sheets_data = {}

    for i, sheet_name in enumerate(excel_data.sheet_names):
        df = excel_data.parse(sheet_name)

        # Modify the "Toxin" column to add hyperlinks for specific toxins
        if 'Toxin' in df.columns:
            df['Toxin'] = df['Toxin'].apply(
                lambda cell: f'<a href="{TOXIN_URLS.get(cell.strip(), "#")}" target="_blank">{cell}</a>'
                if pd.notna(cell) and cell.strip() in TOXIN_URLS else cell
            )

        # Modify the "Toxin type(s)" column for the first sheet
        if i == 0 and "Toxin type(s)" in df.columns:
            df["Toxin type(s)"] = df["Toxin type(s)"].apply(
                lambda cell: ', '.join(
                    f'<span class="clickable-toxin">{toxin.strip()}</span>'
                    for toxin in str(cell).split(',')
                ) if pd.notna(cell) else cell
            )
        df = df.applymap(lambda cell: str(cell).replace('\n', '<br>') if pd.notna(cell) else cell)

        # Convert DataFrame to HTML, allowing embedded HTML with escape=False
        sheets_data[sheet_name] = df.to_html(classes="table table-bordered", index=False, escape=False)

    return render_template('tables.html', sheets=sheets_data)


@app.route("/neurotoxins")
def neurotoxins():
    return render_template("neurotoxins.html")
@app.route("/hepatotoxins")
def hepatotoxins():
    return render_template("hepatotoxins.html")
@app.route("/dermatotoxins")
def dermatotoxins():
    return render_template("dermatotoxins.html")

@app.route("/anatoxins")
def anatoxins():
    return render_template("anatoxins.html")
@app.route("/anatoxins(s)")
def anatoxinss():
    return render_template("anatoxins(s).html")
@app.route("/saxitoxins")
def saxitoxins():
    return render_template("saxitoxins.html")
@app.route("/BMAA")
def BMAA():
    return render_template("BMAA.html")

if __name__ == '__main__':
    app.run(debug=True)
