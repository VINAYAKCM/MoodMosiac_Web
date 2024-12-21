# MoodMosiac_Web
A Python-based application that helps users track their daily moods and generates valuable insights about their emotional patterns. The system provides both daily comparisons and weekly analysis summaries.

![overall](https://github.com/user-attachments/assets/818a2fcd-1957-4f17-a982-079c4f76cd23)

## How to use MoodMosiac?
 ### Step 01: Create an Account
  1.	Open the web application in your browser via the link.
  2.	Click on the Sign Up or Create Account button.
  3.	Fill in the required details (username, email and password).
  4.	Submit the form to create your account.
     
![Get Started](https://github.com/user-attachments/assets/d71df759-aebb-475f-bcfa-9b5993df6a7e)

![Acc Creation](https://github.com/user-attachments/assets/b83e6d45-dd73-499b-af6b-5135dc467def)

### Step 02: Log In
  1.	Go to the Login page.
  2.	Enter your registered username or email and password.
  3.	Click on the Login button to access your dashboard.
     
![Login](https://github.com/user-attachments/assets/fb2d9551-e317-4ad5-9996-b4dffc2cfdb9)

### Step 03: Log Your Mood
  1.	Select the current date or a past date (if you missed logging a mood).
  2.	Choose your mood from the provided options (Happy, Excited, Neutral, Stressed, Sad)
  3.	Optionally, enter a reason or note about why you’re feeling this way.
  4.	Click Save or Update to log your mood.

![Log mood](https://github.com/user-attachments/assets/f20d682d-6e62-4385-a746-b3b5148627e0)

### Step 04: View the Heatmap
  1.	Scroll down to view Heatmap section.
  2.	Observe how your logged moods are reflected on the heatmap. Each day is color-coded based on the mood you logged.
  3.	Use the navigation buttons to explore moods from previous weeks or months.

![heatmap](https://github.com/user-attachments/assets/6682a14a-ba99-4f6f-8519-8000fd6c7cdb)

### Step 05: Analyze Weekly Insights
  1.	Navigate to the Weekly Insights section through the nav bar.
  2.	Review the summarized analysis of your moods for the past week.
  3.	Identify patterns or trends in your emotional well-being.

![Weekly Insights](https://github.com/user-attachments/assets/ce524591-9a1b-44ca-92a7-222cc1860157)


### Tips for Effective Use

  - Log your moods regularly to get the most accurate insights.
  - Reflect on the reasons behind your moods to better understand your emotional patterns.
  - Use the weekly insights to identify triggers or events that may affect your mood positively or negatively.

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
