# 💬 Support-Chatbot für ein IT-Dienstleistungsunternehmen

Ein Support-Chatbot, der typische Anfragen rund um Services, Kontaktmöglichkeiten, Öffnungszeiten, Termine und Rückrufwünsche eines IT-Dienstleisters automatisch beantwortet. Entwickelt mit [Rasa](https://rasa.com/) und Python.

---

## 📁 Projektübersicht

**Hauptfunktionen des Chatbots:**
- Beantwortet Fragen zu Leistungen bzw. Service des Unternehmens
- Gibt Auskunft über Kontaktmöglichkeiten und Öffnungszeiten
- Anfragen auf Passwort-Zurücksetzen oder auch Beschwerden
- Erfasst Rückrufwünsche und fragt gezielt nach Uhrzeit & Anliegen
- Reagiert freundlich auf Grußformeln, Small Talk & Danke
- Unterstützt Wiederholung von Rückrufdaten & Korrekturen

---

## ⚙️ Technologien
- 🧠 **Rasa** (NLU + Core)
- 🐍 **Python** (für Custom Actions)
- 🧪 **YAML** für Konfig & Story Definition
- 🧪 **Rasa Test Framework** für Unit Tests

---

## 🚀 So startest du den Bot lokal
```bash
# Repo klonen
git clone https://github.com/Mesut6300/it-support-chatbot.git
cd it-support-chatbot

# Virtuelle Umgebung aktivieren (optional, empfohlen)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Trainingsdaten verarbeiten
rasa train

# Bot starten
rasa shell


🧪 Tests ausführen
rasa test

🧠 NLU-Trainingdaten
Die Datei nlu.yml enthält alle Intents, Beispiel-Äußerungen und benutzten Entities. Darin steckt das sprachliche Herz des Chatbots:)

✅ Status
- Grundlegende Intents & Stories
- Rückruffunktion mit Slot-Füllung
- Custom Actions für Bestätigung & Korrektur
- Tests & Evaluierung
- Erweiterung für FAQ & Dokumentenservice (optional)

👨‍💻 Autor
Mesut Dilber
Studienprojekt im Rahmen der Lehrveranstaltung Natural Language Processing

📄 Lizenz
Dieses Projekt ist unter der MIT License veröffentlicht.
