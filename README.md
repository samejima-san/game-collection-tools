# Steam Library Exporter

Export your entire Steam library to your own personal database with clean, customizable queries.

**Steam Library Exporter** is a simple utility designed to give you full control over your game collection data. Whether you're archiving, building a personal game tracker, or integrating with another project, this tool helps you move your library from Steam to your own system.

## ✨ Features

- 📦 Export your Steam library to your own database  
- 🔍 Easily customizable SQL queries  
- ⚙️ Clean, minimal design for integration with personal tools  
- 🧱 Ready for integration into game library websites, dashboards, or analytics tools  

## 🔧 Setup

1. **Clone the repository**

```bash   
   git clone https://github.com/samejima-san/steamlibraryexporter.git
   cd steamlibraryexporter
```
Install dependencies
(Make sure you have Python 3.8+ installed)

```bash
pip install -r requirements.txt
```
Configure your Steam API key
Set your key and Steam ID in a .env file:

```bash
  STEAM_API_KEY=your_steam_api_key
  STEAM_ID=your_steam_id
```
Choose your database

Update config.py to reflect the database you’re using (e.g., SQLite, PostgreSQL, MySQL).

🚀 Usage

Run the exporter:
```bash
  python export.py
```

This will fetch your Steam library and generate queries that you can directly run or modify for your database.
🗃 Example Output
```Postgresql
  INSERT INTO games (appid, name, year_played, completed, playtime, finished, want_to_return) VALUES (570, 'Dota 2', 2020, false, 3420, false, true);
```
📚 Integration Ideas
  Game tracking websites
  Personal dashboards
  Game time analytics
  Backups and archiving

🧠 Why This Exists

Steam’s official tools are limited. This project exists to give you your data, whether you're building something or just curious about your own play habits.

💬 Feedback & Contributions

Issues and PRs are welcome! If you have ideas or bugs to report, open an issue or drop a pull request.
📄 License

MIT License — do whatever you want, just don’t blame me if it breaks something.
