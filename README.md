# MoodMosiac_Web
A Python-based application that helps users track their daily moods and generates valuable insights about their emotional patterns. The system provides both daily comparisons and weekly analysis summaries.

## Features:
  - Daily Mood Logging: Easily record your mood and the reasons behind it.
  - Personalized Insights: Receive daily comparisons of your mood with yesterday’s, helping you track changes.
  - Weekly Analysis: Automatically generates summaries to show trends in your emotional patterns.
  - Flexible Logging: Works seamlessly, even if you miss a few days.
  - Secure Data Storage: Your mood history and weekly summaries are securely saved for future reference.
 
## Installation:
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
## Database Structure:
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
  
## Contributing:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support:
If you encounter any problems or have suggestions, please open an issue in the GitHub repository.

## Roadmap:
• Add mood visualization graphs
• Implement mood prediction
• Add export functionality
• Create mobile app version

## Acknowledgments:
- Thanks to all contributors who have helped with the project
- Inspired by the need for better emotional self-awareness tools
