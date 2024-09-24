import streamlit as st
import pandas as pd
import datetime

# Define evaluation tasks with descriptions
evaluation_tasks = [
    {
        "task": "Dusting",
        "description": "Thoroughly dust all surfaces, including furniture, shelves, and baseboards."
    },
    {
        "task": "Floor Cleaning",
        "description": "Sweep and mop the floors to remove dirt and stains."
    },
    {
        "task": "Window Cleaning",
        "description": "Clean windows inside and outside, ensuring they are streak-free."
    },
    {
        "task": "Bathroom Cleaning",
        "description": "Clean toilets, sinks, mirrors, and floors. Ensure all surfaces are sanitized."
    },
    {
        "task": "Kitchen Cleaning",
        "description": "Clean countertops, sinks, and appliances. Wipe down cabinet doors and clean the floor."
    },
    {
        "task": "Trash Removal",
        "description": "Empty all trash bins and replace with fresh liners."
    },
    {
        "task": "Vacuuming",
        "description": "Vacuum carpets and rugs to remove dust and debris."
    },
    {
        "task": "Organizing",
        "description": "Organize items in designated areas to maintain cleanliness."
    },
]

# Initialize or load employee evaluations
if 'employee_evaluations' not in st.session_state:
    st.session_state['employee_evaluations'] = []

# Define function to add an evaluation
def add_evaluation(employee_name, evaluation_date, tasks, comment, evaluator):
    evaluation = {
        "Employee Name": employee_name,
        "Evaluation Date": evaluation_date,
        "Tasks": ', '.join(tasks),
        "Comment": comment,
        "Evaluator": evaluator
    }
    st.session_state['employee_evaluations'].append(evaluation)

# Set the title of the app
st.title("Employee Cleaning Task Evaluation")

# Input section for evaluation
st.subheader("Add Evaluation")
employee_name = st.text_input("Employee Name")
evaluation_date = st.date_input("Evaluation Date", datetime.date.today())

# Checklist for task selection
selected_tasks = st.multiselect(
    "Select Tasks",
    [task['task'] for task in evaluation_tasks],
    format_func=lambda task: task
)

# Display descriptions for selected tasks
if selected_tasks:
    st.write("Selected Tasks Descriptions:")
    for task in selected_tasks:
        description = next(item['description'] for item in evaluation_tasks if item['task'] == task)
        st.write(f"- **{task}**: {description}")

comment = st.text_area("Comment")
evaluator = st.text_input("Evaluator's Name")

if st.button("Add Evaluation"):
    if not selected_tasks:
        st.error("Please select at least one task.")
    elif not employee_name or not evaluator:
        st.error("Please provide the employee's name and evaluator's name.")
    else:
        add_evaluation(employee_name, evaluation_date, selected_tasks, comment, evaluator)
        st.success("Evaluation added successfully!")

# Display evaluations in a table
st.subheader("Evaluations")
if st.session_state['employee_evaluations']:
    evaluations_df = pd.DataFrame(st.session_state['employee_evaluations'])
    st.dataframe(evaluations_df)
else:
    st.write("No evaluations added yet.")
