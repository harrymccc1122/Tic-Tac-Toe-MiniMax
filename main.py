import streamlit as st
import math

# Initialize the board
if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]

# Function to check if a player has won
def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

# Function to check if the board is full
def is_full(board):
    return ' ' not in board

# Function to check if the game is over
def is_game_over(board):
    return check_win(board, 'X') or check_win(board, 'O') or is_full(board)

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(board, 'O'):
        return 1
    if check_win(board, 'X'):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Function to find the best move for the AI
def best_move(board):
    best_score = -math.inf
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# Function to handle user click
def on_click(index):
    if st.session_state.board[index] == ' ':
        st.session_state.board[index] = 'X'
        if is_game_over(st.session_state.board):
            check_game_over()
            return
        ai_move = best_move(st.session_state.board)
        st.session_state.board[ai_move] = 'O'
        check_game_over()

# Function to check if the game is over and display the result
def check_game_over():
    if check_win(st.session_state.board, 'X'):
        st.write("You win!")
        reset_game()
    elif check_win(st.session_state.board, 'O'):
        st.write("AI wins!")
        reset_game()
    elif is_full(st.session_state.board):
        st.write("It's a draw!")
        reset_game()

# Function to reset the game
def reset_game():
    st.session_state.board = [' ' for _ in range(9)]

# Streamlit app
st.title("Tic Tac Toe")

# Display the board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        cols[j].button(f"{st.session_state.board[i*3+j]}", key=f"button_{i*3+j}", on_click=on_click, args=(i*3+j,))

# Reset button
if st.button("Reset Game"):
    reset_game()

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Welcome to Tic Tac Toe!")
