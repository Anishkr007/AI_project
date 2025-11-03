# AI Project: Car Price Prediction

This project predicts the selling price of used cars using a machine learning model.

## Project Structure

-   `/data`: Contains the raw `car_data.csv`.
-   `/notebooks`: Contains the Jupyter Notebook `car_price_analysis.ipynb` for data analysis, model training, and comparison.
-   `/backend`: Contains the Flask API (`app.py`) that serves the trained model (`model.pkl`) and scaler (`scaler.pkl`).
-   `/frontend`: Contains the simple web interface (`index.html`, `style.css`, `script.js`) to interact with the model.

## How to Run

1.  **Setup Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Train the Model:**
    -   Run the `notebooks/car_price_analysis.ipynb` notebook from top to bottom.
    -   This will generate `backend/model.pkl` and `backend/scaler.pkl`.

4.  **Run the Backend Server:**
    ```bash
    cd backend
    python app.py
    ```
    The server will be running at `http://127.0.0.1:5000`.

5.  **Run the Frontend:**
    -   Open the `frontend/index.html` file directly in your web browser (e.g., Chrome, Firefox).
    -   Fill out the form and click "Predict Price" to see the results.