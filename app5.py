import os
import glob
import streamlit as st
import plotly.express as px
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
from collections import Counter
import random

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Set up sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Directory to store diary and mood entries
diary_directory = "diary/"
os.makedirs(diary_directory, exist_ok=True)  # Create directory if it doesn't exist

# Motivational quotes for tough days
positive_messages = [
    "The greatest glory in living lies not in never falling, but in rising every time we fall. – Nelson Mandela",
    "Your present circumstances don’t determine where you can go; they merely determine where you start. – Nido Qubein",
    "In the depth of winter, I finally learned that within me lay an invincible summer. – Albert Camus",
    "Strength does not come from winning. Your struggles develop your strengths. – Arnold Schwarzenegger",
    "Sometimes when things are falling apart, they may actually be falling into place. – Tashabee",
    "One small crack does not mean that you are broken, it means that you were put to the test and didn’t fall apart. – Linda Poindexter",
    "Out of suffering have emerged the strongest souls; the most massive characters are seared with scars. – Khalil Gibran",
    "Don’t give up because you had a bad day. Forgive yourself and do better tomorrow.",
    "The best is yet to be. – Robert Browning",
    "You are never too old to set another goal or to dream a new dream. – C.S. Lewis",
    "Positivity always wins… Always. – Gary Vaynerchuk",
    "Keep your face always toward the sunshine—and shadows will fall behind you. – Walt Whitman",
    "When things go wrong, don't go with them. – Elvis Presley",
    "Train your mind to see the good in every situation. – Unknown",
    "If opportunity doesn’t knock, build a door. – Milton Berle",
    "Believe you can, and you're halfway there. – Theodore Roosevelt",
    "A goal is not always meant to be reached, it often serves simply as something to aim at. – Bruce Lee",
    "Shoot for the moon. Even if you miss, you'll land among the stars. – Norman Vincent Peale",
    "Once you replace negative thoughts with positive ones, you’ll start having positive results. – Willie Nelson",
    "Positive thinking will let you do everything better than negative thinking will. – Zig Ziglar",
    "When you are enthusiastic about what you do, you feel this positive energy. It’s very simple. – Paolo Coelho",
    "It makes a big difference in your life when you stay positive. Cultivate an optimistic mind, use your imagination, always consider alternatives, and dare to believe that you can make possible what others think is impossible. – Rodolfo Costa",
    "Positive thinking is more than just a tagline. It changes the way we behave. And I firmly believe that when I am positive, it not only makes me better, but it also makes those around me better. – Harvey Mackay",
    "What is the difference between an obstacle and an opportunity? Our attitude toward it. Every opportunity has a difficulty, and every difficulty has an opportunity. – J. Sidlow Baxter",
    "An attitude of positive expectation is the mark of the superior personality. – Brian Tracy",
    "Keep your face to the sunshine and you cannot see a shadow. – Helen Keller",
    "Even though you’re fed up, you gotta keep your head up. – Tupac Shakur",
    "The positive thinker sees the invisible, feels the intangible, and achieves the impossible. – Oscar Wilde",
    "You need to be able to manage stress because hard times will come, and a positive outlook is what gets you through. – Marie Osmond",
    "You have to train your brain to be positive just like you work out your body. – Shawn Achor"
]

# Function to display a random positive message
def display_positive_message():
    st.info(random.choice(positive_messages))

# Streamlit app title
st.title("FeelTrack - Your Diary and Mood Tracker")

# Step 1: User selects a date
selected_date = st.date_input("Select a date")

# Convert the selected date to a string in YYYY-MM-DD format
date_str = selected_date.strftime("%Y-%m-%d")

# Step 2: Dropdown to choose between 'Diary' or 'Mood'
option = st.selectbox("Choose between 'Diary' or 'Mood'", ["Diary", "Mood"])

# Step 3: Depending on the selection, show relevant inputs and graphs
if option == "Diary":
    st.subheader("Diary Entry")

    # Text input area for writing the diary
    diary_content = st.text_area("Write your diary entry for " + selected_date.strftime("%B %d, %Y"))

    # Button to save the diary entry
    if st.button("Save Diary Entry"):
        if diary_content:
            # Save the diary entry to a text file named after the selected date
            file_path = os.path.join(diary_directory, f"{date_str}.txt")
            with open(file_path, "w") as file:
                file.write(diary_content)

            st.success(f"Diary entry for {selected_date.strftime('%B %d, %Y')} saved successfully!")

            # Perform sentiment analysis on the entry
            scores = analyzer.polarity_scores(diary_content)
            compound_score = scores['compound']

            # Display whether the day was positive, negative, or neutral based on the compound score
            if compound_score > 0:
                st.success("Your day has been **positive**!")
            elif compound_score < 0:
                st.error("Your day has been **negative**.")
                display_positive_message()  # Show positive message for negative sentiment
            else:
                st.info("Your day has been **neutral**.")

        else:
            st.error("Please write something in the diary before saving.")

# Mood selection and mood history plotting
elif option == "Mood":
    st.subheader("Mood Tracker")

    moods = {
        "Happy": "😊",
        "Neutral": "😐",
        "Sad": "😢",
        "Angry": "😠",
        "Relaxed": "😌"
    }
    selected_mood = st.selectbox("How do you feel today?", list(moods.keys()), format_func=lambda x: moods[x])

    # Button to save the mood entry
    if st.button("Save Mood"):
        # Save the mood entry with today's date
        mood_file_path = os.path.join(diary_directory, f"{date_str}.txt")

        # Check if entry for today already exists
        if os.path.exists(mood_file_path):
            # If exists, append mood
            with open(mood_file_path, "a", encoding='utf-8') as file:
                file.write(f"Mood: {selected_mood}\n")
            st.success("Your mood has been saved successfully!")
        else:
            # If not exists, create new entry
            with open(mood_file_path, "w", encoding='utf-8') as file:
                file.write(f"Mood: {selected_mood}\n\n")  # Placeholder for diary content
                file.write("No diary entry for today.\n")
            st.success("Mood for today saved successfully!")

        # Display positive message if the mood is 'Sad' or 'Angry'
        if selected_mood in ["Sad", "Angry"]:
            display_positive_message()

# Load all diary entries to visualize sentiment history
filepaths = sorted(glob.glob(os.path.join(diary_directory, "*.txt")))

# Lists to store sentiment analysis scores and dates
dates = []
positivity = []
negativity = []
mood_entries = []

for filepath in filepaths:
    # Read the content of the diary entry
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Get sentiment scores
    scores = analyzer.polarity_scores(content)

    # Append the sentiment scores to the lists
    positivity.append(scores['pos'])
    negativity.append(scores['neg'])

    # Extract the date from the filename
    filename = os.path.basename(filepath)
    date_str = filename.strip(".txt")

    # Format the date for display
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%B %d, %Y")
    dates.append(formatted_date)

    # Extract mood from content if available
    if "Mood:" in content:
        mood_line = content.split("Mood:")[1].split("\n")[0].strip()
        mood_entries.append(mood_line)

# Plot positivity and negativity over time if entries exist
if dates:
    if option == "Diary":
        st.subheader("Positivity Over Time")
        pos_figure = px.line(x=dates, y=positivity, labels={"x": "Date", "y": "Positivity"})
        st.plotly_chart(pos_figure)

        st.subheader("Negativity Over Time")
        neg_figure = px.line(x=dates, y=negativity, labels={"x": "Date", "y": "Negativity"})
        st.plotly_chart(neg_figure)

    elif option == "Mood":
        st.subheader("Mood History (Sentiment Over Time)")
        mood_figure = px.line(x=dates, y=positivity, labels={"x": "Date", "y": "Mood Positivity"})
        st.plotly_chart(mood_figure)

        # Display mood pie chart if mood entries exist
        if mood_entries:
            st.subheader("Mood Distribution")
            mood_counter = Counter(mood_entries)
            mood_labels = list(mood_counter.keys())
            mood_values = list(mood_counter.values())

            # Create a pie chart for the mood distribution
            pie_chart = px.pie(
                values=mood_values,
                names=mood_labels,
                title="Mood Distribution in %",
                labels={"label": "Mood", "value": "Percentage"}
            )
            st.plotly_chart(pie_chart)
else:
    st.write("No entries found.")
