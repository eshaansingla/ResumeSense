# ResumeSense Setup Guide

Complete step-by-step setup guide for ResumeSense.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Training the ML Model](#training-the-ml-model)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Python 3.8+**
   - Check version: `python3 --version`
   - Download: https://www.python.org/downloads/

2. **MySQL 5.7+ or MariaDB**
   - macOS: `brew install mysql`
   - Linux: `sudo apt-get install mysql-server` (Ubuntu/Debian)
   - Windows: Download from https://dev.mysql.com/downloads/mysql/

3. **Git** (for version control)
   - Check: `git --version`
   - Download: https://git-scm.com/downloads

### System Requirements

- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: 500MB free space
- **OS**: macOS, Linux, or Windows

## Installation Steps

### Step 1: Clone/Navigate to Project

```bash
cd ResumeSense
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 PyMuPDF-1.23.8 ...
```

### Step 4: Verify Installation

```bash
python -c "import flask; import fitz; import pymysql; print('All dependencies installed!')"
```

## Database Setup

### Step 1: Start MySQL Server

**macOS (Homebrew):**
```bash
brew services start mysql
```

**Linux:**
```bash
sudo systemctl start mysql
# or
sudo service mysql start
```

**Windows:**
- Start MySQL service from Services panel
- Or use MySQL Workbench

### Step 2: Secure MySQL Installation (First Time Only)

```bash
mysql_secure_installation
```

Follow prompts to set root password and secure installation.

### Step 3: Create Database (Optional)

The application will create the database automatically if the MySQL user has permissions.

**Manual creation:**
```bash
mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS resumesense;
EXIT;
```

### Step 4: Verify Database Connection

```bash
mysql -u root -p -e "SHOW DATABASES;"
```

You should see `resumesense` in the list (after first run).

## Configuration

### Step 1: Create .env File

Create a `.env` file in the project root:

```bash
touch .env  # macOS/Linux
# or create manually on Windows
```

### Step 2: Configure Environment Variables

Edit `.env` file with your settings:

```env
# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production-12345

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DATABASE=resumesense

# File Upload Configuration
UPLOAD_FOLDER=data/resumes

# ML Model Configuration
ML_MODEL_PATH=backend/ml/resume_quality_model.pkl
```

**Important:**
- Replace `your_mysql_password_here` with your actual MySQL root password
- Change `SECRET_KEY` to a random string for production
- Ensure `UPLOAD_FOLDER` path exists (will be created automatically)

### Step 3: Create Upload Directory

```bash
mkdir -p data/resumes
```

## Running the Application

### Step 1: Train ML Model (First Time)

```bash
python backend/ml/train_model.py
```

**Expected output:**
```
Generating training data...
Training data shape: (30, 22), Labels shape: (30,)
Training Random Forest model...
Training R² score: 0.95
Test R² score: 0.88
Model saved to backend/ml/resume_quality_model.pkl
```

**Note:** If this step fails, the app will use rule-based scoring as fallback.

### Step 2: Start the Application

```bash
python run.py
```

**Expected output:**
```
Starting ResumeSense application...
Upload folder: data/resumes
Database: resumesense
 * Running on http://0.0.0.0:5000
```

### Step 3: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

You should see the ResumeSense homepage.

## Training the ML Model

### Automatic Training

Run the training script:
```bash
python backend/ml/train_model.py
```

### Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: 22 features extracted from resume
- **Output**: Quality score (0-100)
- **Model File**: `backend/ml/resume_quality_model.pkl`

### Retraining

To retrain with new data:
1. Add training data to `backend/ml/train_model.py`
2. Run training script again
3. Model will be overwritten

## Testing

### Run All Tests

```bash
python -m pytest backend/tests/ -v
```

### Run Specific Test

```bash
python -m pytest backend/tests/test_pdf_parser.py -v
```

### Run with Coverage

```bash
pip install pytest-cov
python -m pytest backend/tests/ --cov=backend --cov-report=html
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'backend'"

**Solution:**
- Ensure you're in the project root directory
- Verify virtual environment is activated
- Check Python path: `python -c "import sys; print(sys.path)"`

### Issue: "Error connecting to database"

**Solutions:**
1. Verify MySQL is running:
   ```bash
   mysql -u root -p -e "SELECT 1;"
   ```

2. Check `.env` file has correct credentials

3. Test connection manually:
   ```python
   import pymysql
   conn = pymysql.connect(
       host='localhost',
       user='root',
       password='your_password',
       database='resumesense'
   )
   ```

### Issue: "PDF parsing fails"

**Solutions:**
1. Ensure PDF contains text (not just images)
2. Check file size is reasonable (< 10MB)
3. Verify PyMuPDF is installed: `pip install PyMuPDF`

### Issue: "Model file not found"

**Solution:**
- This is normal on first run
- App will use rule-based scoring
- Train model: `python backend/ml/train_model.py`

### Issue: "Port 5000 already in use"

**Solution:**
1. Find process using port:
   ```bash
   lsof -i :5000  # macOS/Linux
   netstat -ano | findstr :5000  # Windows
   ```

2. Kill process or change port in `run.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Issue: "Permission denied" (macOS/Linux)

**Solution:**
```bash
chmod +x run.py
# or
python run.py
```

### Issue: Database tables not created

**Solution:**
1. Check MySQL user has CREATE TABLE permission
2. Verify database exists
3. Check application logs for errors
4. Manually create tables (see `backend/db/database.py`)

## Production Deployment

### Using Gunicorn

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Create `Procfile`:
   ```
   web: gunicorn run:app
   ```

3. Run:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### Environment Variables for Production

- Set `FLASK_ENV=production`
- Use strong `SECRET_KEY`
- Configure production database
- Set up proper logging
- Enable HTTPS
- Configure firewall rules

## Next Steps

1. ✅ Application is running
2. 📝 Upload a test resume
3. 🔍 Analyze against a job description
4. 📊 Review results
5. 🎯 Improve your resume based on feedback

## Getting Help

1. Check this guide
2. Review README.md
3. Check API_DOCUMENTATION.md
4. Review code comments
5. Check test files for examples

---

**Happy Resume Analyzing! 🚀**


