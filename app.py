import streamlit as st
import pandas as pd
import datetime

# Define evaluation tasks with descriptions and categories
evaluation_tasks = {
    "General Cleaning": [
        {
            "task": "Dusting",
            "description": "Thoroughly dust all surfaces, including furniture, shelves, baseboards, and light fixtures."
        },
        {
            "task": "Floor Cleaning",
            "description": "Sweep, vacuum, and mop the floors to remove dirt, stains, and allergens. Include corners and edges."
        },
        {
            "task": "Window Cleaning",
            "description": "Clean windows inside and outside, ensuring they are streak-free. Don't forget the window sills."
        },
        {
            "task": "Trash Removal",
            "description": "Empty all trash bins in each room and replace them with fresh liners. Recycle where applicable."
        },
        {
            "task": "Vacuuming",
            "description": "Vacuum carpets and rugs to remove dust, dirt, and debris. Ensure to vacuum under furniture and in corners."
        },
        {
            "task": "Organizing",
            "description": "Organize items in designated areas to maintain cleanliness. Tidy up any clutter to improve overall aesthetics."
        },
        {
            "task": "Furniture Polishing",
            "description": "Polish wooden furniture to maintain shine and protect against wear. Use appropriate cleaners for different surfaces."
        },
        {
            "task": "Air Vent Cleaning",
            "description": "Dust and clean air vents and filters to ensure proper air circulation and improve indoor air quality."
        },
        {
            "task": "Light Fixture Cleaning",
            "description": "Dust and clean all light fixtures and ceiling fans to enhance illumination and maintain cleanliness."
        },
        {
            "task": "Baseboard Cleaning",
            "description": "Wipe down baseboards to remove dust and dirt accumulation. Ensure to reach all corners and joints."
        },
        {
            "task": "Wall Washing",
            "description": "Clean walls to remove fingerprints, stains, and dust buildup. Use appropriate cleaning solutions for different wall types."
        },
    ],
    "Kitchen": [
        {
            "task": "Kitchen Cleaning",
            "description": "Clean countertops, sinks, appliances, and the inside of the microwave. Wipe down cabinet doors and clean the floor."
        },
        {
            "task": "Appliance Cleaning",
            "description": "Wipe down and clean all appliances, including the fridge, oven, and dishwasher, both inside and out."
        },
    ],
    "Bathroom": [
        {
            "task": "Bathroom Cleaning",
            "description": "Clean toilets, sinks, mirrors, and floors. Ensure all surfaces are sanitized and freshened, paying attention to details."
        },
    ],
    "Outdoor": [
        {
            "task": "Exterior Cleaning",
            "description": "If applicable, clean the exterior surfaces, including patios and outdoor furniture, to maintain curb appeal."
        },
    ]
}

# Initialize or load employee evaluations
if 'employee_evaluations' not in st.session_state:
    st.session_state['employee_evaluations'] = []

# Define function to add an evaluation
def add_evaluation(employee_name, evaluation_date, tasks, comments, evaluator):
    evaluation = {
        "Employee Name": employee_name,
        "Evaluation Date": evaluation_date,
        "Tasks": ', '.join(tasks),
        "Comments": comments,
        "Evaluator": evaluator
    }
    st.session_state['employee_evaluations'].append(evaluation)

# Set the title of the app
st.title("Employee Cleaning Task Evaluation System")

# Input section for evaluation
st.subheader("Add Evaluation")
employee_name = st.text_input("Employee Name")
evaluation_date = st.date_input("Evaluation Date", datetime.date.today())

# Task selection and performance rating
selected_tasks = {}
for category, tasks in evaluation_tasks.items():
    st.write(f"### {category}")
    for task in tasks:
        is_selected = st.checkbox(task['task'], value=False, key=task['task'])
        if is_selected:
            selected_tasks[task['task']] = {
                'description': task['description'],
                'rating': st.select_slider(
                    f"Performance Rating for {task['task']}",
                    options=[1, 2, 3, 4, 5],
                    value=3,
                    format_func=lambda x: f"{x} - {'Poor' if x == 1 else 'Fair' if x == 2 else 'Good' if x == 3 else 'Very Good' if x == 4 else 'Excellent'}"
                )
            }

comments = st.text_area("Additional Comments")
evaluator = st.text_input("Evaluator's Name")

if st.button("Add Evaluation"):
    # Validate inputs
    if not selected_tasks:
        st.error("Please select at least one task.")
    elif not employee_name or not evaluator:
        st.error("Please provide the employee's name and evaluator's name.")
    else:
        add_evaluation(employee_name, evaluation_date, selected_tasks.keys(), comments, evaluator)
        st.success("Evaluation added successfully!")

# Filter evaluations
st.subheader("Evaluations")
filter_name = st.text_input("Filter by Employee Name", "")
if st.session_state['employee_evaluations']:
    evaluations_df = pd.DataFrame(st.session_state['employee_evaluations'])
    
    # Apply filter if provided
    if filter_name:
        evaluations_df = evaluations_df[evaluations_df['Employee Name'].str.contains(filter_name, case=False)]
    
    st.dataframe(evaluations_df)

    # Additional stats on evaluations
    st.write("### Evaluation Statistics")
    total_evaluations = len(evaluations_df)
    st.write(f"- Total Evaluations: {total_evaluations}")
else:
    st.write("No evaluations added yet.")

# Instructions for users
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Enter the employee's name and the evaluator's name.
2. Select the cleaning tasks from the checklist provided.
3. Rate the performance of each task from 1 (Poor) to 5 (Excellent).
4. Add any additional comments if necessary.
5. Click 'Add Evaluation' to save the evaluation.
6. All evaluations will be displayed below, and you can filter evaluations by employee name.
""")

# Conclusion note
st.sidebar.header("Notes")
st.sidebar.write("""
- Ensure that all tasks are well-defined and clearly understood by employees.
- Regular evaluations help maintain high cleaning standards and identify areas for improvement.
- Consider conducting evaluations regularly to keep track of employee performance and motivation.
""")
