# MoodMosiac_Web
A Python-based application that helps users track their daily moods and generates valuable insights about their emotional patterns. The system provides both daily comparisons and weekly analysis summaries.
## Features :sparkles:
- **Daily Mood Logging**: Record your mood and the reason behind it
- **Daily Insights**: Compare your current mood with yesterday
- **Weekly Analysis**: Automatic weekly summaries of your emotional patterns
- **Flexible Data Handling**: Works even with missing daily entries
- **Data Persistence**: Securely stores your mood history and weekly insights
## Installation :rocket:
1. Clone the repository:
```bash
git clone https://github.com/yourusername/mood-tracker.git
cd mood-tracker
```
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Initialize the database:
```bash
python init_db.py
```
## Usage :bulb:
1. **Log Your Mood**:
```python
python log_mood.py
```
2. **View Daily Insight**:
```python
python daily_insight.py
```
3. **Generate Weekly Summary**:
```python
python weekly_insight.py
```
## Database Structure :bar_chart:
The application uses SQLite with two main tables:
### Moods Table
- id (Primary Key)
- user_id
- mood
- reason
- date
### Weekly Insights Table
- id (Primary Key)
- user_id
- start_date
- end_date
- week_insight
## Contributing :handshake:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request
## License :memo:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## Support :sos:
If you encounter any problems or have suggestions, please open an issue in the GitHub repository.
## Roadmap :world_map:
- [ ] Add mood visualization graphs
- [ ] Implement mood prediction
- [ ] Add export functionality
- [ ] Create mobile app version
## Acknowledgments :clap:
- Thanks to all contributors who have helped with the project
- Inspired by the need for better emotional self-awareness tools
