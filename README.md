# Bangalore House Price Prediction

A machine learning web application that predicts house prices in Bangalore based on location, size, number of bedrooms (BHK), and bathrooms. Built with Flask, scikit-learn, and XGBoost.

## 🚀 Features

- **Real-time Price Prediction**: Get instant house price estimates based on user inputs
- **Location-based Pricing**: Supports 240+ locations across Bangalore
- **User-friendly Web Interface**: Clean, responsive UI with Tailwind CSS
- **Machine Learning Model**: Trained on real Bangalore housing data using XGBoost
- **RESTful API**: JSON endpoints for integration with other applications
- **Data Processing Pipeline**: Comprehensive data cleaning and feature engineering

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Machine Learning**: scikit-learn, XGBoost
- **Data Processing**: pandas, numpy
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Deployment**: Flask development server (production-ready with WSGI)

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bangalore-house-price-prediction
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure model artifacts exist**
   - The trained model (`models/banglore_home_prices_model.pickle`) and column data (`models/columns.json`) should be present
   - If not, run the training pipeline (see Model Training section)

## 🚀 Usage

### Running the Web Application

1. **Start the Flask server**
   ```bash
   python src/app.py
   ```

2. **Open your browser**
   - Navigate to `http://127.0.0.1:5000`
   - The application will load the home page with the prediction form

3. **Make Predictions**
   - Select a location from the dropdown
   - Enter total square feet, BHK, and number of bathrooms
   - Click "Predict Price" to get the estimated price

### API Usage

The application provides REST API endpoints:

#### Get Location Names
```http
GET /get_location_names
```
Returns a JSON array of available location names.

**Response:**
```json
{
  "locations": ["1st block jayanagar", "2nd phase jp nagar", ...]
}
```

#### Predict House Price
```http
POST /predict_home_price
Content-Type: application/x-www-form-urlencoded

total_sqft=1200&location=1st%20block%20jayanagar&bhk=2&bath=2
```

**Response:**
```json
{
  "estimated_price": 85.5
}
```

## 📁 Project Structure

```
bangalore-house-price-prediction/
│
├── data/
│   ├── raw/
│   │   └── Bengaluru_House_Data.csv      # Raw housing data
│   └── processed/
│       └── cleaned_data.csv              # Processed training data
│
├── models/
│   ├── banglore_home_prices_model.pickle # Trained XGBoost model
│   └── columns.json                      # Feature columns metadata
│
├── notebooks/
│   └── Banglore House Price Prediction.ipynb  # Data exploration & modeling
│
├── src/
│   ├── __init__.py
│   ├── app.py                            # Flask web application
│   ├── data_processing.py                # Data cleaning pipeline
│   ├── model_training.py                 # Model training script
│   ├── utils.py                          # Utility functions for predictions
│   ├── logger.py                         # Logging configuration
│   └── exception.py                      # Custom exception handling
│
├── templates/
│   └── app.html                          # Web interface template
│
├── logs/                                 # Application logs
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
```

## 📊 Data

The model is trained on Bangalore housing data with the following features:
- **Location**: Categorical feature with 240+ unique locations
- **Total Sqft**: Numerical feature (square footage)
- **BHK**: Number of bedrooms/hall/kitchen
- **Bath**: Number of bathrooms

### Data Processing Steps
1. Remove irrelevant columns (area_type, availability, society, balcony)
2. Handle missing values
3. Extract BHK from size descriptions
4. Convert total_sqft ranges to averages
5. Remove outliers based on price per sqft
6. One-hot encode location features

## 🤖 Model

- **Algorithm**: XGBoost Regressor
- **Performance**: Selected through GridSearchCV comparing Linear Regression, Lasso, and Decision Tree
- **Features**: 243 total (3 numerical + 240 location dummies)
- **Training Data**: ~7,000 cleaned samples

### Model Training

To retrain the model:

1. **Run the Jupyter notebook**
   ```bash
   jupyter notebook notebooks/Banglore\ House\ Price\ Prediction.ipynb
   ```

2. **Or use the training script**
   ```bash
   python src/model_training.py
   ```

The script will:
- Load processed data
- Perform feature engineering
- Train and save the best model
- Save column information for predictions

## 🔍 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with prediction form |
| GET | `/get_location_names` | Get list of available locations |
| POST | `/predict_home_price` | Predict house price based on inputs |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bangalore housing data from Kaggle/real estate sources
- UI inspiration from modern web design patterns
- Machine learning best practices from scikit-learn documentation

---

**Note**: This is a demonstration project. For production deployment, consider using a WSGI server like Gunicorn and adding proper authentication/security measures.