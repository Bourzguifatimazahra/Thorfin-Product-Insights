# Thorfin Product Insights - Pro Dashboard

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Professional-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📊 Overview

**Thorfin Product Insights - Pro** is a comprehensive, enterprise-grade dashboard for product analysis, customer feedback evaluation, and business intelligence reporting. Built with Streamlit, this application enables data teams and product managers to extract actionable insights from customer reviews and sales data through advanced analytics, visualizations, and AI-powered report generation.

## ✨ Features

### 📈 **Core Analytics**
- **Interactive Data Exploration**: Upload CSV, Excel, or JSON files with automatic column normalization
- **Dynamic Filtering**: Real-time filtering by date range, price, rating, and product search
- **Key Performance Indicators**: Real-time metrics tracking (reviews count, average rating, average price, top-rated products)

### 📊 **Advanced Visualizations**
- **Sentiment Analysis**: AI-powered sentiment classification using Azure OpenAI
- **Word Clouds**: Automated generation from review texts with custom stopwords
- **Multi-format Charts**:
  - Seaborn/Matplotlib for static analytics
  - Plotly for interactive visualizations
  - Geographic distribution maps (if location data available)
  - Time-series trend analysis

### 📄 **Professional Reporting**
- **Automated Report Generation**: Create comprehensive PDF reports with:
  - Executive summary
  - Key findings
  - Charts and visualizations
  - Recommendations
- **HTML Export**: Interactive HTML reports for web sharing
- **Customizable Templates**: Professional report templates with branding

### 🤖 **AI-Powered Insights**
- **Azure OpenAI Integration**: GPT-based analysis for:
  - Sentiment classification
  - Trend identification
  - Automated recommendations
  - Summary generation
- **Smart Text Analysis**: Natural language processing of customer reviews

### 🎨 **User Experience**
- **Professional UI**: Modern gradient design with dark theme
- **Responsive Layout**: Wide-screen optimized dashboard
- **Intuitive Navigation**: Sidebar-based controls and filters
- **Real-time Updates**: Instant feedback on data changes

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Azure OpenAI API access (for AI features)
- Required Python packages (see requirements.txt)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/thorfin-product-insights.git
cd thorfin-product-insights
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
AZURE_API_KEY=your_azure_openai_api_key_here
# Optional: Add other configurations
```

5. **Run the application**
```bash
streamlit run app.py
```

### Sample Dataset Structure
The application expects datasets with columns like:
- `client_id`: Unique customer identifier
- `product`: Product name
- `product_description`: Product description
- `price`: Product price (numeric)
- `rating`: Customer rating (1-5 scale)
- `review_text`: Customer review content
- `review_language`: Review language
- `purchase_date`: Date of purchase

## 📋 Requirements

### Core Dependencies
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
seaborn>=0.12.0
matplotlib>=3.7.0
plotly>=5.17.0
fpdf>=1.7.2
openai>=1.3.0
wordcloud>=1.9.0
python-dotenv>=1.0.0
```

### Optional Dependencies
- `scikit-learn`: For advanced ML features
- `nltk`: For NLP preprocessing
- `geopandas`: For geographic visualizations

## 🏗️ Architecture

### Application Structure
```
thorfin-product-insights/
│
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── README.md                # This file
├── assets/                  # Static assets
│   ├── logo.png            # Application logo
│   └── samples/            # Sample datasets
│
├── modules/                 # Modular components
│   ├── data_loader.py      # Data loading and preprocessing
│   ├── visualizations.py   # Chart generation functions
│   ├── report_generator.py # PDF/HTML report generation
│   └── ai_analyzer.py      # Azure OpenAI integration
│
└── templates/               # Report templates
    ├── pdf_template.html   # PDF template
    └── html_template.html  # HTML report template
```

### Key Components

1. **Data Processing Module**
   - Automatic file type detection (CSV, Excel, JSON)
   - Column normalization and cleaning
   - Missing value handling
   - Date parsing and formatting

2. **Visualization Engine**
   - Multi-library support (Seaborn, Matplotlib, Plotly)
   - Responsive chart sizing
   - Export capabilities (PNG, SVG)
   - Themed visualizations

3. **AI Integration Layer**
   - Azure OpenAI client configuration
   - Prompt engineering for product insights
   - Batch processing optimization
   - Error handling and fallbacks

4. **Report Generation System**
   - PDF creation with FPDF
   - HTML report templating
   - Image embedding and formatting
   - Custom styling and branding

## 🔧 Configuration

### Azure OpenAI Setup
1. Create an Azure OpenAI resource in the Azure Portal
2. Deploy a GPT model (gpt-4 or gpt-35-turbo)
3. Obtain your API endpoint and key
4. Configure in `.env` file:
```env
AZURE_API_KEY=your_api_key_here
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
DEPLOYMENT_NAME=your-deployment-name
API_VERSION=2024-12-01-preview
```

### Customization Options
- **UI Colors**: Modify gradient colors in the header section
- **Chart Themes**: Adjust seaborn/plotly themes
- **Report Templates**: Customize PDF/HTML templates
- **Stop Words**: Add language-specific stopwords for word clouds

## 📖 Usage Guide

### 1. Data Upload
1. Navigate to the sidebar
2. Click "Upload dataset"
3. Select CSV, Excel, or JSON file
4. Wait for automatic processing

### 2. Apply Filters
- Adjust date range sliders
- Filter by price or rating
- Search for specific products
- All filters apply in real-time

### 3. Generate Insights
- View KPIs in the main dashboard
- Explore interactive charts
- Generate word clouds from reviews
- Use AI analysis for sentiment

### 4. Create Reports
1. Click "Generate Report" button
2. Choose report type (PDF/HTML)
3. Select included sections
4. Download or preview report

## 🛠️ Advanced Features

### Custom Visualizations
```python
# Example: Adding custom charts
def create_custom_visualization(df):
    # Your visualization code here
    return fig
```

### Extending AI Analysis
```python
# Example: Custom prompt engineering
custom_prompt = """
Analyze the following product reviews and provide:
1. Top 3 positive aspects
2. Top 3 areas for improvement
3. Sentiment trend over time
"""
```

### Adding New Data Sources
1. Modify `data_loader.py`
2. Add new file type handler
3. Update column mapping logic
4. Test with sample data

## 🔒 Security Considerations

- API keys stored in environment variables
- No data persistence on server
- Client-side processing where possible
- Secure file handling
- Input validation and sanitization

## 📈 Performance Optimization

- Cached data loading with `@st.cache_data`
- Lazy loading for large datasets
- Batch processing for AI calls
- Optimized chart rendering
- Memory management for PDF generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black app.py modules/
```
 

## 🆘 Support

- **Documentation**: [Full documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/Bourzguifatimazahra/Thorfin-Product-Insights)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/thorfin-product-insights/discussions)
- **Email**: bourzguifatimazahra@gmail.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) for AI capabilities
- [FPDF](http://www.fpdf.org/) for PDF generation
- All open-source libraries used in this project

---

<div align="center">
<strong>Thorfin Product Insights - Pro Dashboard</strong><br>
Professional Product Analytics | AI-Powered Insights | Enterprise Reporting
</div>
