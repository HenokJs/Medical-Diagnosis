# MediDiagnose – AI Clinical Decision Support System

Professional AI-powered medical diagnosis platform with clinical reasoning, NLP symptom extraction, PDF reporting, and persistent patient history.

---

## Features

- AI-powered disease prediction (50+ diseases)
- Confidence-ranked top 3 diagnoses
- NLP symptom extraction from free text
- Forward & backward chaining inference
- Severity classification system
- Professional PDF medical reports
- Persistent PostgreSQL report history
- Modern React + Flask architecture

---

## Tech Stack

- Frontend: React + TypeScript
- Backend: Flask + Python
- Database: PostgreSQL
- ML/NLP: Scikit-learn + RapidFuzz
- Reports: ReportLab PDF Engine

---

## Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/HenokJs/Medical-Diagnosis.git
cd Medical-Diagnosis
```

### 2. Configure Environment

Create `.env` in the project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/medical_diagnosis
SECRET_KEY=your-secret-key
FLASK_ENV=development
VITE_API_URL=http://localhost:5000/api/v1
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
flask db upgrade
python -m backend.run
```

Backend:
```txt
http://localhost:5000
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend:
```txt
http://localhost:3000
```

---

### 5. Database Setup
Run the script the rootpath
```bash
docker-compose up -d
```
## Project Structure

```txt
Medical-Diagnosis/
├── backend/
├── frontend/
├── ml/
```

---

## Core Capabilities

- Symptom checkbox + free text input
- Clinical decision support engine
- Disease severity analysis
- Age & gender risk modifiers
- Persistent diagnosis sessions
- Downloadable clinical reports
- Historical report tracking

---