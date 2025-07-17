# Risk Assessment Workflow API

Eine einfache FastAPI-Anwendung zur Erfassung und Simulation eines Gefährdungsbeurteilungs-Workflows mit automatischen Tasks.

---

## 🚀 Quickstart

### Option A: Lokale Python-Umgebung

```bash
# Repo klonen
git clone https://github.com/alikhalajii/risk_assessment_api.git
cd risk_assessment_api

# Virtuelle Umgebung  erstellen, aktivieren, Dependencies installieren
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt

# Server starten
uvicorn app.main:app --reload
```
Öffne im Browser:

http://localhost:8000/docs


### Option B: Docker
```bash
# Repo klonen
git clone https://github.com/alikhalajii/risk_assessment_api.git
cd risk_assessment_api

# Image bauen und Container starten
docker build -t risk-api .
docker run --rm -p 8000:8000 --name risk-api-container risk-api
```
Öffne im Browser:

http://localhost:8000/docs

---
### Unittests
Die Unittests werden automatisch bei jedem Push ins Repository ausgeführt. Manuell können sie wie folgt gestartet werden:

Im aktivierten Virtual Environment:
```bash
pytest -q
```
Im Docker-Container (Terminal öffnen)

```bash
docker exec -it risk-api-container bash
pytest -q
```
