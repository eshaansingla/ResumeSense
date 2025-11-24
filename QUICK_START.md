# ResumeSense Quick Start Guide

Get ResumeSense up and running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python3 --version

# Check MySQL is installed
mysql --version
```

## Quick Setup (5 Steps)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Start MySQL

```bash
# macOS
brew services start mysql

# Linux
sudo systemctl start mysql

# Windows: Start MySQL service from Services panel
```

### 3. Configure Environment

```bash
# Copy example env file
cp env.example .env

# Edit .env and set your MySQL password
# MYSQL_PASSWORD=your_password_here
```

### 4. Train Model (Optional)

```bash
python backend/ml/train_model.py
```

**Note:** App works without this step (uses rule-based scoring).

### 5. Run Application

```bash
python run.py
```

Open browser: http://localhost:5000

## First Test

1. Go to http://localhost:5000
2. Upload a PDF resume (or use sample in `data/resumes/`)
3. Optionally paste a job description
4. Click "Analyze Resume"
5. View results!

## Troubleshooting

**Database Error?**
- Check MySQL is running: `mysql -u root -p`
- Verify `.env` has correct password

**Import Error?**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

**Port 5000 in use?**
- Change port in `run.py`: `app.run(port=5001)`

## Next Steps

- Read full [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Review [README.md](README.md)

---

**That's it! You're ready to analyze resumes! 🚀**


