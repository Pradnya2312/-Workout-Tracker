import streamlit as st
import os

class ExerciseLog:
    def __init__(self, log_date, activity, time_spent, calories):
        self.log_date = log_date
        self.activity = activity
        self.time_spent = time_spent
        self.calories = calories

    def __str__(self):
        return f"{self.log_date}: {self.activity} for {self.time_spent} minutes, {self.calories} calories burned"

class FitnessUser:
    def __init__(self, full_name, years, body_weight):
        self.full_name = full_name
        self.years = years
        self.body_weight = body_weight
        self.exercise_logs = []

    def record_exercise(self, log):
        self.exercise_logs.append(log)

    def display_logs(self):
        return "\n".join(str(log) for log in self.exercise_logs) if self.exercise_logs else "No workout logs available."

    def save_logs(self, file_name):
        try:
            with open(file_name, "w") as file:
                for log in self.exercise_logs:
                    file.write(f"{log.log_date},{log.activity},{log.time_spent},{log.calories}\n")
            return "Log saved successfully!"
        except Exception as e:
            return f"Error saving log: {e}"

    def load_logs(self, file_name):
        try:
            if not os.path.exists(file_name):
                return "File not found!"
            self.exercise_logs.clear()
            with open(file_name, "r") as file:
                for line in file:
                    log_date, activity, time_spent, calories = line.strip().split(",")
                    self.exercise_logs.append(ExerciseLog(log_date, activity, int(time_spent), int(calories)))
            return "Logs loaded successfully!"
        except Exception as e:
            return f"Error loading logs: {e}"

st.title("Fitness Tracker App")

if "fitness_user" not in st.session_state:
    st.session_state.fitness_user = None

with st.sidebar:
    st.header("User Registration")
    full_name = st.text_input("Full Name")
    years = st.number_input("Age", min_value=1, step=1)
    body_weight = st.number_input("Weight (kg)", min_value=1, step=1)
    if st.button("Register User"):
        st.session_state.fitness_user = FitnessUser(full_name, years, body_weight)
        st.success(f"User {full_name} registered successfully!")

st.header("Log Your Exercise")
log_date = st.text_input("Date (YYYY-MM-DD)")
activity = st.text_input("Workout Type")
time_spent = st.number_input("Duration (minutes)", min_value=1, step=1)
calories = st.number_input("Calories Burned", min_value=1, step=1)
if st.button("Log Exercise"):
    if st.session_state.fitness_user:
        exercise_log = ExerciseLog(log_date, activity, time_spent, calories)
        st.session_state.fitness_user.record_exercise(exercise_log)
        st.success("Workout logged successfully!")
    else:
        st.error("Please register a user first!")

st.header("View Exercise History")
if st.button("Show Logs"):
    if st.session_state.fitness_user:
        st.text(st.session_state.fitness_user.display_logs())
    else:
        st.error("Please register a user first!")

st.header("Save & Load Logs")
file_name = st.text_input("Enter filename")
col1, col2 = st.columns(2)
with col1:
    if st.button("Save Logs"):
        if st.session_state.fitness_user:
            st.success(st.session_state.fitness_user.save_logs(file_name))
        else:
            st.error("Please register a user first!")
with col2:
    if st.button("Load Logs"):
        if st.session_state.fitness_user:
            st.success(st.session_state.fitness_user.load_logs(file_name))
        else:
            st.error("Please register a user first!")
