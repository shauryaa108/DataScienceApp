# Experiment 10 — Gapminder Interactive Data Web App

An interactive Streamlit app for exploring the Gapminder World Development dataset (1,704 country-year rows; 142 countries; five continents; 1952–2007).

## Project files

- `app.py` — Streamlit web app.
- `exp10_gapminder.csv` — provided dataset.
- `requirements.txt` — Python dependencies for the app and notebook.
- `Experiment10_Gapminder_Analysis.ipynb` — analysis notebook for VS Code Jupyter.
- `screenshots/` — output figures used in the lab report and README.

## Run locally in VS Code

1. Open this folder in VS Code and install the **Python** and **Jupyter** extensions.
2. Open the integrated terminal.
3. Create and activate a virtual environment (Windows PowerShell):

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Open `Experiment10_Gapminder_Analysis.ipynb`, select the `.venv` Python kernel, and run all cells.
6. Start the web app from the terminal:

   ```bash
   streamlit run app.py
   ```

   Streamlit normally opens `http://localhost:8501` in your browser.

## App features

- Sidebar filters: continent multi-select, year slider and country search.
- KPI cards: number of selected countries, average life expectancy, total population and median GDP per capita.
- Bubble chart: GDP per capita (log scale) vs life expectancy; bubble size = population; colour = continent.
- Trend lines: selected countries and selected metric (life expectancy, GDP per capita or population).
- Top-N ranking for the selected year.
- Filtered data table with CSV download.

## Six questions answered from the supplied CSV

1. **Largest gain in average life expectancy:** Asia, +24.414 years from 1952 to 2007 (continent means).
2. **GDP per capita and life expectancy:** overall Pearson correlation = 0.584, a positive association. It is positive in every continent: Africa 0.426, Americas 0.558, Asia 0.382, Europe 0.781, Oceania 0.956. Correlation is not proof of causation.
3. **Life-expectancy declines:** 52 countries had at least one five-year decline (102 declining country-period observations). See the notebook output or `life_expectancy_declines.csv` after running the notebook for the country-period list.
4. **Population ranking:** China, India and the United States were the top three in both 1952 and 2007. In 2007, Pakistan, Nigeria and Mexico entered the top ten; Germany, the United Kingdom and Italy were no longer in it.
5. **India vs China:** between 1952 and 2007 life expectancy rose from 37.373 to 64.698 years in India and from 44.000 to 72.961 in China. In 2007, China had higher GDP per capita and life expectancy than India; the notebook provides the full time series for life expectancy, GDP per capita and population.
6. **High GDP but below-average life expectancy in 2007:** using the 2007 country averages (GDP per capita $11,680.07; life expectancy 67.007 years), the qualifying countries are Gabon, Botswana, Equatorial Guinea.

The decline periods by country are computed directly from adjacent five-year observations in the notebook. Results depend on the supplied dataset and the threshold definitions above.

## Deploy to Streamlit Community Cloud

1. Push `app.py`, `exp10_gapminder.csv`, `requirements.txt` and `README.md` to a public GitHub repository.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Create an app, choose the repository and branch, and set the main file path to `app.py`.
4. Deploy, test the public app and add the generated URL here.

**Public app URL:** _Add your deployed Streamlit URL here._  
**GitHub repository:** _Add your public GitHub repository URL here._

## Screenshots

![Input dataset preview](screenshots/figure1_dataset_preview.png)

![Continent life expectancy gain](screenshots/figure2_continent_gain.png)

![2007 bubble chart](screenshots/figure3_bubble_2007.png)

![India and China trends](screenshots/figure4_india_china_trends.png)

![Top population comparison](screenshots/figure5_population_top10.png)
