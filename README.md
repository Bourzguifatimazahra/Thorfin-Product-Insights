 # Thorfin Product Insights - Pro Dashboard

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Professional-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-blue)

## 📊 Overview

**Thorfin Product Insights - Pro** is a comprehensive, enterprise-grade dashboard for product analysis, customer feedback evaluation, and business intelligence reporting. Built with Streamlit, this application enables data teams and product managers to extract actionable insights from customer reviews and sales data through advanced analytics, visualizations, and AI-powered report generation.

## ✨ Key Features

### 📈 **Interactive Data Analytics**
- **Multi-format Support**: Upload CSV, Excel, or JSON files with automatic column normalization
- **Real-time Filtering**: Dynamic filters for date range, price, rating, and product search
- **Live KPIs**: Real-time metrics tracking including review count, average rating, price analysis, and top-rated products

### 📊 **Advanced Visualizations**
- **Multi-library Support**: Plotly for interactive charts, Seaborn/Matplotlib for static analytics
- **Comprehensive Charts**: Histograms, box plots, violin plots, scatter plots, pie/donut charts, Pareto analysis
- **Word Clouds**: Automated generation from review texts with custom stopwords
- **Correlation Analysis**: Heatmaps and pair plots for numerical data exploration

### 🤖 **AI-Powered Insights**
- **Azure OpenAI Integration**: GPT-based sentiment analysis and summary generation
- **Smart Text Processing**: Natural language analysis of customer reviews
- **Customizable Prompts**: Flexible AI analysis with user-defined constraints and tones

### 📄 **Professional Reporting**
- **Automated Report Generation**: Create comprehensive PDF reports with charts and insights
- **HTML Export**: Interactive HTML reports for web sharing
- **Multi-format Support**: Export data in both PDF and HTML formats
- **Branded Templates**: Professional report templates with consistent styling

### 🎨 **User Experience**
- **Modern UI**: Professional gradient design with dark theme
- **Responsive Layout**: Wide-screen optimized dashboard
- **Intuitive Navigation**: Sidebar-based controls and filters
- **Real-time Updates**: Instant feedback on data changes

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Azure OpenAI API access (for AI features)
- Required Python packages (see requirements below)

### Installation

1. **Clone and setup environment**
```bash
# Clone repository
git clone <repository-url>
cd thorfin-product-insights

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install streamlit pandas numpy seaborn matplotlib plotly fpdf openai wordcloud python-dotenv
```

3. **Configure environment variables**
Create a `.env` file in the project root:
```env
AZURE_API_KEY=your_azure_openai_api_key_here
# Optional additional configurations
```

4. **Run the application**
```bash
streamlit run app.py
```

## 📋 Required Python Packages

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

## 📁 Expected Dataset Structure

The application is designed to work with datasets containing the following columns:

| Column Name | Type | Description |
|------------|------|-------------|
| `client_id` | String | Unique customer identifier |
| `product` | String | Product name |
| `product_description` | String | Product description |
| `price` | Numeric | Product price |
| `rating` | Numeric (1-5) | Customer rating |
| `review_text` | String | Customer review content |
| `review_language` | String | Review language |
| `purchase_date` | Date | Date of purchase |

## 🏗️ Architecture

### Application Structure
```
thorfin-product-insights/
│
├── app.py                    # Main application file
├── .env                      # Environment variables (not in version control)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── README.md               # This documentation file
│
├── data/                   # Sample datasets (optional)
│   ├── sample_reviews.csv
│   └── sample_products.json
│
└── exports/                # Generated reports (created at runtime)
    ├── html_reports/
    └── pdf_reports/
```

### Core Modules

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

### Application Configuration
The main configuration is located in the `app.py` file:

```python
# API Configuration
API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = "https://bourz-mihhzl50-eastus2.cognitiveservices.azure.com/"
DEPLOYMENT_NAME = "gpt-5-chat"
API_VERSION = "2024-12-01-preview"

# Streamlit Configuration
st.set_page_config(
    page_title="Thorfin Product Insights - Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 📖 Usage Guide

### Step 1: Data Upload
1. Navigate to the sidebar section "1) Dataset & filtres"
2. Click "Uploader dataset (CSV / Excel / JSON)"
3. Select your data file
4. Wait for automatic processing and column normalization

### Step 2: Apply Interactive Filters
- **Date Range**: Filter by purchase date using the date picker
- **Price Slider**: Adjust price range using the interactive slider
- **Rating Filter**: Select rating range (1-5)
- **Product Search**: Search for specific products using partial names
- All filters apply in real-time and update all visualizations

### Step 3: Analyze Key Metrics
View the main dashboard section to see:
- Total number of reviews
- Average product rating
- Average price across products
- Top-rated product identification

### Step 4: Explore Visualizations
Navigate through different chart types:
1. **Distribution Charts**: Histograms for price distribution
2. **Comparison Charts**: Box plots and violin plots for rating comparison
3. **Relationship Charts**: Scatter plots for price vs rating analysis
4. **Composition Charts**: Pie and donut charts for product distribution
5. **Analytical Charts**: Pareto analysis for top products

### Step 5: Generate AI Insights
1. Select a specific product from the dropdown
2. Click "Générer résumé AI pour le produit sélectionné"
3. Customize the analysis prompt if needed
4. View the AI-generated summary with pros, cons, and suggestions

### Step 6: Export Reports
1. **HTML Report**: Click "Générer rapport HTML" for an interactive web report
2. **PDF Report**: Click "Générer PDF pro" for a printable professional report
3. Both reports include:
   - Product KPIs
   - Visualizations
   - AI summary
   - Review excerpts
   - Generation timestamp

## 🛠️ Advanced Features

### Custom Visualizations
The application supports adding custom visualizations by extending the visualization functions:

```python
def create_custom_chart(df, column_name):
    """Example of a custom chart function"""
    fig = px.density_heatmap(df, x=column_name, title=f"Density Heatmap for {column_name}")
    return fig
```

### Extending AI Analysis
Customize the AI prompt engineering for specific use cases:

```python
custom_prompt = """
Analyze the following product reviews and provide:
1. Top 3 positive aspects with sentiment score
2. Top 3 areas for improvement
3. Trending topics over the last 30 days
4. Customer sentiment evolution
5. Actionable recommendations for product team
"""
```

### Adding New Data Sources
To support additional file formats:

1. Modify the `load_data` function in `app.py`
2. Add new file type handlers
3. Update column mapping logic
4. Test with sample data

## 🔒 Security Considerations

- **API Keys**: Stored securely in environment variables
- **Data Privacy**: No data persistence on server; all processing is client-side
- **Input Validation**: Comprehensive validation for uploaded files
- **Secure File Handling**: Temporary file cleanup after processing
- **Error Handling**: Graceful degradation for API failures

## 📈 Performance Optimization

- **Caching**: Data loading cached with `@st.cache_data` decorator
- **Lazy Loading**: Large datasets processed in chunks
- **Batch Processing**: AI calls optimized for multiple reviews
- **Chart Optimization**: Plotly for interactive, Seaborn for static charts
- **Memory Management**: Efficient PDF generation with temporary file cleanup

## 🚨 Error Handling

The application includes comprehensive error handling for:

- **File Upload Errors**: Invalid formats, corrupted files
- **API Errors**: Azure OpenAI connectivity issues
- **Data Processing Errors**: Missing columns, invalid data types
- **Memory Errors**: Large file handling
- **Export Errors**: File system permissions, disk space

## 📊 Sample Use Cases

### E-commerce Product Analysis
- Analyze customer feedback across product categories
- Identify pricing sweet spots
- Detect quality issues through review patterns
- Generate competitor analysis reports

### SaaS Product Management
- Track feature adoption through user feedback
- Monitor customer satisfaction trends
- Generate product improvement roadmaps
- Create investor-ready performance reports

### Market Research
- Aggregate customer sentiment across markets
- Identify emerging trends in customer feedback
- Generate market intelligence reports
- Support product launch decisions with data

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```
3. **Commit your changes**
```bash
git commit -m 'Add amazing feature'
```
4. **Push to the branch**
```bash
git push origin feature/amazing-feature
```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Include error handling for new features
- Update documentation for API changes
- Test with sample datasets

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Generate coverage report
pytest --cov=app tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **Azure API Error** | Check API key, endpoint, and deployment name in .env file |
| **File Upload Fails** | Verify file format and column names match expected structure |
| **Slow Performance** | Reduce dataset size or enable sampling in visualizations |
| **PDF Generation Error** | Ensure write permissions in export directory |
| **Chart Display Issues** | Check Plotly/Matplotlib compatibility and update libraries |

### Getting Help
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check the comprehensive usage guide
- **Community**: Join Streamlit community forums
- **Email**: Contact project maintainers for enterprise support

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web application framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) for AI capabilities
- [Plotly](https://plotly.com/) for interactive visualizations
- [FPDF](http://www.fpdf.org/) for PDF generation
- All open-source libraries and communities that made this project possible

---

<div align="center">
<strong>Thorfin Product Insights - Pro Dashboard</strong><br>
Professional Product Analytics | AI-Powered Insights | Enterprise Reporting
</div>

<p align="center">
  <em>Transform raw data into actionable business intelligence</em>
</p>
