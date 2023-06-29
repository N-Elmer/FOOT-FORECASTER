# FOOT-FORECASTER
TOP 🏆 WINNING FOOTBALL 🏆 TEAMS

FOOT-FORECASTER is a web application that provides forecasted wins for each team in the African Cup of Nations (AFCON) tournament. It utilizes historical data and machine learning models to predict the performance of teams in future tournaments. The application offers visualizations of the forecasted wins through a forecast chart, a team wins map and a ranking table.

## Folder Structure

📂 FOOT-FORECASTER
   
   |
   
   ├── 📄 README.md
   
   ├── 📂 data
   
   │   ├── 📄 afcon.csv
   
   │   └── 📄 results.csv
   
   ├── 📂 documentation
   
   │   ├── 📄 Documentation [EN].docx
   
   │   └── 📄 Documentation [EN].pdf
   
   ├── 📂 models
   
   │   └── 📄 model.pkl
   
   ├── 📂 static
   
   │   ├── 📂 css
   
   │   │   └── 📄 styles.css
   
   │   ├── 📂 js
   
   │   │   ├── 📄 jquery.min.js
   
   │   │   ├── 📄 plotly.min.js
   
   │   │   └── 📄 script.js
   
   │   └── 📄 favicon.ico
   
   ├── 📂 templates
   
   │   └── 📄 index.html
   
   ├── 📄 preprocessing.ipynb
   
   ├── 📄 training.ipynb
   
   ├── 📄 prediction.ipynb
   
   ├── 📄 app.py
   
   └── 📄 requirements.txt

The project folder structure consists of the following files and folders:

- 📄 README.md: This file contains the documentation and information about the FOOT-FORECASTER web application, including how to use it and any additional details.

- 📂 data: This folder contains the data files used for preprocessing and training the machine learning models, including `afcon.csv` and `results.csv`.

- 📂 documentation: This folder contains the documentation files related to the FOOT-FORECASTER web application, including `Documentation [EN].docx` and `Documentation [EN].pdf`.

- 📂 models: This folder contains the trained machine learning models in the form of a pickle file named `model.pkl`.

- 📂 static: This folder contains the static assets used in the web application, including CSS files, JavaScript files, and a favicon.ico file.

   - 📂 css: This subfolder contains the CSS stylesheets used for styling the web application, specifically the `styles.css` file.

   - 📂 js: This subfolder contains the JavaScript files used for the web application's functionality, including the `jquery.min.js`, `plotly.min.js`, and `script.js` files.

- 📂 templates: This folder contains the HTML templates used for rendering the web pages, specifically the `index.html` file.

- 📄 preprocessing.ipynb: This Jupyter Notebook file is used for preprocessing the data before training the machine learning models.

- 📄 training.ipynb: This Jupyter Notebook file is used for training the machine learning models using the preprocessed data.

- 📄 prediction.ipynb: This Jupyter Notebook file is used for forecasting the top teams based on the trained machine learning models.

- 📄 app.py: This file contains the Flask microservice backend for the FOOT-FORECASTER web application. It includes the machine learning model and handles the data requests and responses.

- 📄 requirements.txt: This file lists the project's dependencies and their versions for easy installation.

## Usage

To use the FOOT-FORECASTER web application, follow these steps:

1. Clone or download this project repository.

2. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Open the `preprocessing.ipynb` notebook and execute it to preprocess the data.

4. Open the `training.ipynb` notebook and execute it to train the machine learning models.

5. Open the `prediction.ipynb` notebook and execute it to generate the forecasted wins for the top teams.

6. Run the Flask microservice backend by executing the following command:

   ```
   python app.py
   ```

7. Open a web browser and access the FOOT-FORECASTER web application by navigating to `http://localhost:5000`.

8. Use the year slider to select a specific year and view the forecasted wins for each team in the forecast chart.

9. Explore the team wins map to see the forecasted wins for African teams.

10. Check the top countries table for a summary of the top-performing countries based on the forecast.

## Code Explanation

The FOOT-FORECASTER web application is implemented using JavaScript, jQuery, Plotly, and Flask. Here's a breakdown of the different components:

- **JavaScript**: The `FootForecaster` class in the `script.js` file handles the interactivity of the web application, including attaching event listeners, updating the dashboard based on user input, and managing scroll behavior.

- **jQuery**: jQuery is used to select and manipulate HTML elements in the web application. It simplifies event handling and DOM manipulation.

- **Plotly**: The Plotly library is used for creating the forecast chart and team wins map visualizations. The `updateForecastChart()` and `updateTeamWinsMap()` functions in the `script.js` file update the respective visualizations using data retrieved from the Flask backend.

- **Flask**: The Flask microservice backend is implemented in the `app.py` file. It handles the routing and data requests for the web application. The `/update_dashboard` endpoint receives the selected year from the frontend and returns the necessary data for updating the forecast chart, team wins map, and top countries table.

## Troubleshooting

If you encounter any issues or errors while using the FOOT-FORECASTER web application, consider the following:

- Double-check that all the necessary files and folders are present in the correct locations, as described in the folder structure section.

- Ensure that you have Python installed on your system, and the required dependencies are installed by running `pip install -r requirements.txt`.

- Verify that the data files (`afcon.csv` and `results.csv`) are located in the `data` folder and are correctly formatted.

- If you encounter any issues with the machine learning models, make sure you have successfully preprocessed the data and trained the models using the provided Jupyter Notebook files (`preprocessing.ipynb` and `training.ipynb`).

- If the Flask microservice backend fails to run, check that there are no errors in the `app.py` file and that the required dependencies are installed.

If the problem persists, feel free to open an issue in the GitHub repository for further assistance.

---

This README file provides an overview of the FOOT-FORECASTER web application, its folder structure, usage instructions, code explanation, and troubleshooting tips. Use it as a guide to understand and utilize the FOOT-FORECASTER app.
