import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g
from passlib.hash import pbkdf2_sha256
import os
from apscheduler.schedulers.background import BackgroundScheduler
import google.generativeai as genai
from datetime import datetime, timedelta

# Flask app initialization
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure key in production
DATABASE = 'mood_tracker.db'

# Configure Gemini API
genai.configure(api_key="AIzaSyACD95Jt9oglhUY_iMyjxAet44zFt5hUwI")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_db():
    """Connect to the database and set row_factory."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def get_mood_data_for_period(db, user_id, start_date, end_date):
    """Get mood data for a specific time period."""
    return db.execute(
        '''SELECT mood, reason, date 
           FROM moods 
           WHERE user_id = ? AND date BETWEEN ? AND ? 
           ORDER BY date''',
        (user_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    ).fetchall()

# Add this function to handle weekly data fetching
def fetch_week_data(db, user_id, start_date, end_date):
    """Fetch mood data for a specific week."""
    return db.execute('''
        SELECT date, mood, reason 
        FROM moods 
        WHERE user_id = ? AND date BETWEEN ? AND ?
        ORDER BY date
    ''', (user_id, start_date, end_date)).fetchall()

# Add this function to check if a summary exists
def summary_exists(db, user_id, start_date, end_date):
    """Check if a weekly summary already exists."""
    result = db.execute('''
        SELECT COUNT(*) FROM weekly_insights
        WHERE user_id = ? AND start_date = ? AND end_date = ?
    ''', (user_id, start_date, end_date)).fetchone()
    return result[0] > 0

# Add this function to generate a weekly summary
def generate_daily_insight(current_mood, previous_mood=None):
    """Generate a daily insight based on current and previous mood data."""
    prompt = f"""
    Today's mood: {current_mood['mood']}
    Reason: {current_mood['reason']}
    
    {f"Yesterday's mood: {previous_mood['mood']} Reason: {previous_mood['reason']}" if previous_mood else "No data available for yesterday"}
    
    Please provide a brief, empathetic insight about today's mood{' compared to yesterday' if previous_mood else ''}.
    Keep it concise (2-3 sentences) and:
    1. Acknowledge the current emotional state
    2. If previous mood exists, note any changes
    3. Offer a gentle, supportive observation
    
    Use appropriate emojis and maintain a caring tone.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating daily insight: {e}")
        return "Unable to generate insight at this time."

def get_weekly_insight_data(db, user_id):
    """Get data needed for weekly insights."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    previous_insight = db.execute(
        '''SELECT insight_text, id FROM weekly_insights 
           WHERE user_id = ? ORDER BY created_at DESC LIMIT 1''',
        (user_id,)
    ).fetchone()
    
    mood_data = get_mood_data_for_period(db, user_id, start_date, end_date)
    
    return start_date, end_date, mood_data, previous_insight

@app.teardown_appcontext
def close_db(error):
    """Close the database connection when the app context is torn down."""
    if hasattr(g, 'db'):
        g.db.close()

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )''')
    
    db.execute('''CREATE TABLE IF NOT EXISTS moods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        mood TEXT NOT NULL,
        reason TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    # Add this new table
    db.execute('''CREATE TABLE IF NOT EXISTS weekly_insights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        insight_text TEXT NOT NULL,
        created_at TEXT NOT NULL,
        previous_insight_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(previous_insight_id) REFERENCES weekly_insights(id)
    )''')
    
    db.commit()

def get_previous_insight(user_id):
    db = get_db()
    return db.execute(
        '''SELECT insight_text FROM weekly_insights 
           WHERE user_id = ? ORDER BY created_at DESC LIMIT 1''',
        (user_id,)
    ).fetchone()

# Add this function to generate insights using Gemini
def generate_weekly_insight(data, previous_insight=None):
    """Generate weekly insight using Gemini model."""
    if not data:
        return "No mood data available for the week."

    formatted_data = "\n".join([
        f"Date: {row['date']}, Mood: {row['mood']}, Reason: {row['reason']}"
        for row in data
    ])
    
    prompt = f"""
    Previous week's insight:
    {previous_insight if previous_insight else "No previous insights available."}

    Here is the mood data for the week ({len(data)} entries):
    {formatted_data}

    Please provide a concise, freindly, positive and thoughtful summary that:
    1. Notes the overall mood pattern for the week
    2. Compares with last week if available
    3. Highlights any significant changes or consistencies
    4. Offers supportive observations and gentle suggestions
    
    Use emojis and maintain an encouraging and positive tone.
    Keep the response under 250 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating weekly insight: {e}")
        return "Unable to generate insight at this time."

@app.route('/')
def index():
    """Landing page."""
    if 'user_id' in session:
        return redirect(url_for('mood_input'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = pbkdf2_sha256.hash(password)

        try:
            db.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return "Username or Email already exists. Please try again."

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']

        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and pbkdf2_sha256.verify(password, user['password_hash']):
            session['user_id'] = user['id']
            return redirect(url_for('mood_input'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout route."""
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/api/calendar_data')
def calendar_data():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401

    db = get_db()
    user_id = session['user_id']

    now = datetime.now()
    start_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = now.strftime("%Y-%m-%d")

    rows = db.execute(
        'SELECT date, mood FROM moods WHERE user_id = ? AND date BETWEEN ? AND ?',
        (user_id, start_date, end_date)
    ).fetchall()

    mood_map = {
        "Sad": 1,
        "Stressed": 2,
        "Neutral": 3,
        "Happy": 4,
        "Excited": 5
    }

    data = {}
    for row in rows:
        date_str = row['date']
        mood_val = mood_map.get(row['mood'], 3)
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        timestamp = int(dt.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        data[timestamp] = mood_val

    return data

# Update the mood_input route to include daily insights
@app.route('/mood_input', methods=['GET', 'POST'])
def mood_input():
    """Mood input and update route with daily insights."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']
    selected_date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    daily_insight = None

    if request.method == 'POST':
        mood = request.form['mood']
        reason = request.form.get('reason', '')
        entry_date = request.form.get('entry_date', selected_date)

        # Handle mood entry update/insert
        existing_entry = db.execute(
            'SELECT * FROM moods WHERE user_id = ? AND date = ?',
            (user_id, entry_date)
        ).fetchone()

        if existing_entry:
            db.execute(
                'UPDATE moods SET mood = ?, reason = ? WHERE user_id = ? AND date = ?',
                (mood, reason, user_id, entry_date)
            )
        else:
            db.execute(
                'INSERT INTO moods (user_id, mood, reason, date) VALUES (?, ?, ?, ?)',
                (user_id, mood, reason, entry_date)
            )
        db.commit()

        # Generate daily insight after mood entry
        current_mood = {'mood': mood, 'reason': reason}
        previous_date = (datetime.strptime(entry_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        
        previous_mood = db.execute(
            'SELECT mood, reason FROM moods WHERE user_id = ? AND date = ?',
            (user_id, previous_date)
        ).fetchone()

        daily_insight = generate_daily_insight(current_mood, previous_mood)

    existing_entry = db.execute(
        'SELECT * FROM moods WHERE user_id = ? AND date = ?',
        (user_id, selected_date)
    ).fetchone()

    return render_template('mood_input.html', 
                         existing_entry=existing_entry, 
                         selected_date=selected_date,
                         daily_insight=daily_insight)

@app.route('/insights')
def insights():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']
    
    # Get current date and find the most recent Sunday
    today = datetime.now()
    days_since_sunday = today.weekday() + 1
    recent_sunday = today - timedelta(days=days_since_sunday)
    
    # Generate insights for the most recent complete week if not exists
    start_date = (recent_sunday - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = recent_sunday.strftime("%Y-%m-%d")
    
    if not summary_exists(db, user_id, start_date, end_date):
        # Get previous insight
        previous_insight = db.execute('''
            SELECT insight_text 
            FROM weekly_insights 
            WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 1
        ''', (user_id,)).fetchone()
        
        # Fetch week's data
        week_data = fetch_week_data(db, user_id, start_date, end_date)
        
        if week_data:
            insight_text = generate_weekly_insight(
                week_data,
                previous_insight['insight_text'] if previous_insight else None
            )
            
            # Store new insight
            db.execute('''
                INSERT INTO weekly_insights 
                (user_id, start_date, end_date, insight_text, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id, 
                start_date, 
                end_date, 
                insight_text,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            db.commit()
    
    # Fetch all insights for display
    insights = db.execute('''
        SELECT i1.*, i2.insight_text as previous_insight
        FROM weekly_insights i1
        LEFT JOIN weekly_insights i2 ON i1.created_at > i2.created_at
        WHERE i1.user_id = ?
        GROUP BY i1.id
        ORDER BY i1.created_at DESC 
        LIMIT 4
    ''', (user_id,)).fetchall()
    
    return render_template('insights.html', insights=insights)

# Modify the main block to include scheduler initialization
if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)