import streamlit as st
import random
import matplotlib.pyplot as plt


def reset_session():
    """Resets the game session variables."""
    st.session_state.colors = [
        # List of colors with their names, hex values, and light/dark category
        ('Aqua', '#00FFFF', 'light'),
        ('Pink', '#FFB6C1', 'light'),
        ('Blue', '#AFEEEE', 'light'),
        ('Coral', '#F08080', 'light'),
        ('Khaki', '#F0E68C', 'light'),

        ('Navy', '#000080', 'dark'),
        ('Maroon', '#800000', 'dark'),
        ('Purple', '#483D8B', 'dark'),
        ('Black', '#000000', 'dark'),
        ('Cyan', '#008B8B', 'dark'),
    ]

    # Randomly select a secret color from the list of colors
    st.session_state.secret_color = random.choice(st.session_state.colors)
    st.session_state.guesses = 0  # Initialize number of guesses
    st.session_state.history = []   # Initialize history of messages

    if 'games' not in st.session_state:
        # Initialize the list of games and guess counts if not already present
        st.session_state.games = []
        st.session_state.guess_counts = []

    st.session_state.game_active = True  # Set the game as active


# Check if the game has been initialized; if not, reset the session
if 'secret_color' not in st.session_state:
    reset_session()

# Sidebar for page navigation
page = st.sidebar.radio("Select a page", ["Game", "Stats"])

if page == "Game":
    # Game page layout and design
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&display=swap');
    </style>
    <h1 style="font-family: 'Mochiy Pop One', sans-serif; background: linear-gradient(to right, #0072FF, #FFD700, #00FF7F, #6A0AD6, #FF0000);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;">
        Color Challenge!
    </h1>
    """, unsafe_allow_html=True)

    if st.session_state.game_active:
        # Assistant prompt for guessing the color
        with st.chat_message("assistant"):
            st.markdown('I have a color in mind. Can you guess it?')

        # Display all possible colors for guessing
        st.markdown("### Possible colors:")
        color_boxes = "".join(
            f"<div style='display: inline-block; margin-right: 10px; text-align: center;'>"
            f"<div style='width: 30px; height: 30px; background-color: {color[1]}; border: 1px solid black;'></div>"
            f"<span style='margin-top: 5px; display: block;'><strong>{color[0]}</strong></span>"
            f"</div>" for color in st.session_state.colors
        )

        st.markdown(color_boxes, unsafe_allow_html=True)

        # Display messages from the chat history
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Allow the user to make a guess if they have remaining attempts
        if st.session_state.guesses < 4:
            guess = st.chat_input(
                'Enter your guess (e.g., Aqua, Navy):', key='guess')

            if guess:
                guess = guess.strip()

                # Validate the guess against the list of available colors
                valid_colors = [color[0].lower()
                                for color in st.session_state.colors]

                if guess.lower() not in valid_colors:
                    st.chat_message("assistant").markdown(
                        "Please enter only one name of a possible color.")
                else:
                    st.session_state.guesses += 1  # Increment guess count
                    user_msg = f'I think the secret color would be {guess}.'
                    st.session_state.history.append(
                        {"role": "user", "content": user_msg})

                    with st.chat_message("user"):
                        st.markdown(user_msg)

                    # Get the name and category of the secret color
                    secret_color_name = st.session_state.secret_color[0].lower(
                    )
                    secret_color_category = st.session_state.secret_color[2]

                    attempts_remaining = 4 - st.session_state.guesses  # Calculate remaining attempts

                    # Check if the guessed color matches the secret color
                    if guess.lower() == secret_color_name:
                        with st.chat_message("assistant"):
                            msg = f'Great job! You revealed the secret color on your {st.session_state.guesses} guess.'
                            st.success(msg)  # Show success message
                            st.balloons()  # Balloons animation
                            st.session_state.history.append(
                                {"role": "assistant", "content": msg})
                            st.session_state.games.append(1)  # Record win
                            st.session_state.guess_counts.append(
                                st.session_state.guesses)  # Record guess count
                            st.session_state.game_active = False  # End the game
                    else:
                        # Provide feedback only if this is NOT the last guess
                        if st.session_state.guesses < 4:
                            msg = f'The color is not {guess}.'
                            msg += f" You have {attempts_remaining} attempt(s) remaining."
                            msg += f" The secret color is a **{secret_color_category}** color. Try again!"

                            st.session_state.history.append(
                                {'role': 'assistant', 'content': msg})
                            with st.chat_message("assistant"):
                                st.markdown(msg)

        # If maximum guesses reached without success, reveal the secret color
        if st.session_state.guesses == 4 and st.session_state.secret_color[0].lower() != guess:
            with st.chat_message("assistant"):
                msg = f"You've reached the maximum number of guesses. The secret color was **{st.session_state.secret_color[0]}**."
                st.warning(msg)  # Show warning message
                st.session_state.history.append(
                    {'role': 'assistant', 'content': msg})
            st.session_state.games.append(0)  # Record loss
            st.session_state.guess_counts.append(
                st.session_state.guesses)  # Record guess count
            st.session_state.game_active = False  # End the game

    # Show button to start a new game if the current game has ended
    if not st.session_state.game_active:
        st.button("Start over", on_click=reset_session)

elif page == "Stats":
    # Stats page layout and design
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&display=swap');
    </style>
    <h1 style="font-family: 'Mochiy Pop One', sans-serif; background: linear-gradient(to right, #0072FF, #FFD700, #00FF7F, #6A0AD6, #FF0000);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;">
        Game Summary
    </h1>
    """, unsafe_allow_html=True)

    total_games = len(st.session_state.games)  # Total number of games played
    if total_games > 0:
        wins = st.session_state.games.count(1)  # Count wins
        losses = st.session_state.games.count(0)  # Count losses
        avg_guesses = sum(st.session_state.guess_counts) / \
            total_games  # Calculate average guesses

        # Styles for the stats display
        st.markdown(
            """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Spice&family=Parkinsans:wght@300..800&display=swap');

    .custom-font-bungee {
        font-family: 'Bungee Spice', cursive;
        color: #FF800080;
        font-size: 24px;
    }

    </style>
    """,
            unsafe_allow_html=True
        )

        # Display the summary statistics
        st.markdown(
            f"""
    <h3 class='custom-font-bungee'>Total Games Played: {total_games}</h3>
    <h3 class='custom-font-bungee'>Wins: {wins}, Losses: {losses}</h3>
    <h3 class='custom-font-bungee'>Average Guesses per Game: {avg_guesses:.2f}</h3>
    """,
            unsafe_allow_html=True
        )

        # Pie chart for Wins and Losses
        labels = ['Win', 'Loss']
        sizes = [wins, losses]
        colors = ['#008080', '#E6E6FA']
        explode = (0.1, 0)  # "explode" the first slice

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', startangle=90)  # Display pie chart
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        plt.title('Game Result', fontdict={
            'fontname': 'Comic Sans MS', 'fontsize': 16, 'color': '#ADD8E6', 'fontweight': 'bold'})

        st.pyplot(fig)  # Display the pie chart

        # Function to generate a random color
        def random_color():
            return f'#{random.randint(0, 0xFFFFFF):06x}'

        # Bar chart for number of guesses per game
        plt.figure()
        guess_labels = [f'Game {i+1}' for i in range(total_games)]
        guess_counts = st.session_state.guess_counts

        # Generate random colors for each bar in the chart
        bar_colors = [random_color() for _ in range(total_games)]

        plt.bar(guess_labels, guess_counts,
                color=bar_colors)  # Create bar chart
        plt.xlabel('Games', fontdict={
            'fontname': 'Comic Sans MS', 'fontsize': 16, 'color': '#000080', 'fontweight': 'bold'})
        plt.ylabel('Number of Guesses', fontdict={
            'fontname': 'Comic Sans MS', 'fontsize': 16, 'color': '#000080', 'fontweight': 'bold'})
        plt.title('Number of Guesses per Game', fontdict={
            'fontname': 'Comic Sans MS', 'fontsize': 16, 'color': '#ADD8E6', 'fontweight': 'bold'})
        plt.xticks(rotation=45)
        plt.ylim(0, max(guess_counts) + 1)  # Set y-axis limits

        st.pyplot(plt)  # Display the bar chart
    else:
        # Message for users when they haven't started the game yet
        st.markdown("### Ready to Begin ...")
