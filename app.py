import streamlit as st
import pandas as pd
import datetime
from collections import defaultdict
import json

# Page configuration
st.set_page_config(
    page_title="Employee Cleaning Evaluation System",
    page_icon="🧹",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .task-category {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Define evaluation tasks with descriptions and categories
evaluation_tasks = {
    "General Cleaning": [
        {
            "task": "Dusting",
            "description": "Thoroughly dust all surfaces, including furniture, shelves, baseboards, and light fixtures.",
            "frequency": "Daily"
        },
        {
            "task": "Floor Cleaning",
            "description": "Sweep, vacuum, and mop the floors to remove dirt, stains, and allergens. Include corners and edges.",
            "frequency": "Daily"
        },
        {
            "task": "Window Cleaning",
            "description": "Clean windows inside and outside, ensuring they are streak-free. Don't forget the window sills.",
            "frequency": "Weekly"
        },
        {
            "task": "Trash Removal",
            "description": "Empty all trash bins in each room and replace them with fresh liners. Recycle where applicable.",
            "frequency": "Daily"
        },
        {
            "task": "Vacuuming",
            "description": "Vacuum carpets and rugs to remove dust, dirt, and debris. Ensure to vacuum under furniture and in corners.",
            "frequency": "Daily"
        },
        {
            "task": "Organizing",
            "description": "Organize items in designated areas to maintain cleanliness. Tidy up any clutter to improve overall aesthetics.",
            "frequency": "Daily"
        },
        {
            "task": "Furniture Polishing",
            "description": "Polish wooden furniture to maintain shine and protect against wear. Use appropriate cleaners for different surfaces.",
            "frequency": "Weekly"
        },
        {
            "task": "Air Vent Cleaning",
            "description": "Dust and clean air vents and filters to ensure proper air circulation and improve indoor air quality.",
            "frequency": "Monthly"
        },
        {
            "task": "Light Fixture Cleaning",
            "description": "Dust and clean all light fixtures and ceiling fans to enhance illumination and maintain cleanliness.",
            "frequency": "Weekly"
        },
        {
            "task": "Baseboard Cleaning",
            "description": "Wipe down baseboards to remove dust and dirt accumulation. Ensure to reach all corners and joints.",
            "frequency": "Weekly"
        },
        {
            "task": "Wall Washing",
            "description": "Clean walls to remove fingerprints, stains, and dust buildup. Use appropriate cleaning solutions for different wall types.",
            "frequency": "Monthly"
        },
        {
            "task": "Door and Handle Sanitizing",
            "description": "Sanitize all door handles, knobs, and high-touch surfaces to prevent germ transmission.",
            "frequency": "Daily"
        },
    ],
    "Kitchen": [
        {
            "task": "Kitchen Cleaning",
            "description": "Clean countertops, sinks, appliances, and the inside of the microwave. Wipe down cabinet doors and clean the floor.",
            "frequency": "Daily"
        },
        {
            "task": "Appliance Cleaning",
            "description": "Wipe down and clean all appliances, including the fridge, oven, and dishwasher, both inside and out.",
            "frequency": "Weekly"
        },
        {
            "task": "Cabinet Organization",
            "description": "Organize kitchen cabinets and pantry. Check for expired items and maintain orderly arrangement.",
            "frequency": "Weekly"
        },
        {
            "task": "Sink Deep Cleaning",
            "description": "Deep clean and sanitize kitchen sink, including disposal and faucet fixtures.",
            "frequency": "Weekly"
        },
    ],
    "Bathroom": [
        {
            "task": "Bathroom Cleaning",
            "description": "Clean toilets, sinks, mirrors, and floors. Ensure all surfaces are sanitized and freshened, paying attention to details.",
            "frequency": "Daily"
        },
        {
            "task": "Shower and Tub Scrubbing",
            "description": "Scrub shower walls, tub, and glass doors to remove soap scum and mildew. Clean grout lines.",
            "frequency": "Weekly"
        },
        {
            "task": "Bathroom Fixtures Polishing",
            "description": "Polish chrome fixtures, handles, and towel racks to maintain shine and prevent water spots.",
            "frequency": "Weekly"
        },
        {
            "task": "Bathroom Supply Restocking",
            "description": "Check and restock toilet paper, paper towels, soap, and other bathroom essentials.",
            "frequency": "Daily"
        },
    ],
    "Outdoor": [
        {
            "task": "Exterior Cleaning",
            "description": "If applicable, clean the exterior surfaces, including patios and outdoor furniture, to maintain curb appeal.",
            "frequency": "Weekly"
        },
        {
            "task": "Entrance Area Maintenance",
            "description": "Clean entrance areas, sweep porches, and ensure welcome mats are clean and properly placed.",
            "frequency": "Daily"
        },
        {
            "task": "Outdoor Trash Management",
            "description": "Manage outdoor trash bins, ensure proper waste disposal, and maintain cleanliness around waste areas.",
            "frequency": "Daily"
        },
    ],
    "Specialized Tasks": [
        {
            "task": "Deep Carpet Cleaning",
            "description": "Perform deep carpet cleaning using specialized equipment to remove embedded dirt and stains.",
            "frequency": "Monthly"
        },
        {
            "task": "Upholstery Cleaning",
            "description": "Clean and sanitize upholstered furniture, including sofas, chairs, and cushions.",
            "frequency": "Monthly"
        },
        {
            "task": "Blind and Curtain Cleaning",
            "description": "Dust and clean window blinds, curtains, and drapes to remove accumulated dust and allergens.",
            "frequency": "Monthly"
        },
    ]
}

# Initialize session state
if 'employee_evaluations' not in st.session_state:
    st.session_state['employee_evaluations'] = []

if 'employees' not in st.session_state:
    st.session_state['employees'] = []

# Function to add an evaluation
def add_evaluation(employee_name, evaluation_date, tasks_data, comments, evaluator, overall_rating, time_spent):
    evaluation = {
        "Employee Name": employee_name,
        "Evaluation Date": str(evaluation_date),
        "Tasks": tasks_data,
        "Comments": comments,
        "Evaluator": evaluator,
        "Overall Rating": overall_rating,
        "Time Spent (hours)": time_spent,
        "Average Task Rating": sum([task['rating'] for task in tasks_data.values()]) / len(tasks_data) if tasks_data else 0
    }
    st.session_state['employee_evaluations'].append(evaluation)

# Function to calculate employee statistics
def calculate_employee_stats(employee_name):
    employee_evals = [e for e in st.session_state['employee_evaluations'] if e['Employee Name'] == employee_name]
    if not employee_evals:
        return None
    
    total_evals = len(employee_evals)
    avg_overall_rating = sum([e['Overall Rating'] for e in employee_evals]) / total_evals
    avg_task_rating = sum([e['Average Task Rating'] for e in employee_evals]) / total_evals
    total_hours = sum([e['Time Spent (hours)'] for e in employee_evals])
    
    # Task frequency analysis
    task_counts = defaultdict(int)
    task_ratings = defaultdict(list)
    for eval in employee_evals:
        for task_name, task_data in eval['Tasks'].items():
            task_counts[task_name] += 1
            task_ratings[task_name].append(task_data['rating'])
    
    return {
        'total_evaluations': total_evals,
        'avg_overall_rating': avg_overall_rating,
        'avg_task_rating': avg_task_rating,
        'total_hours': total_hours,
        'task_counts': dict(task_counts),
        'task_ratings': {k: sum(v)/len(v) for k, v in task_ratings.items()}
    }

# Main header
st.markdown('<div class="main-header">🧹 Employee Cleaning Task Evaluation System</div>', unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 New Evaluation", "📊 View Evaluations", "📈 Analytics", "👥 Employee Management", "⚙️ Settings"])

# TAB 1: NEW EVALUATION
with tab1:
    st.header("Create New Evaluation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        employee_name = st.text_input("Employee Name", key="eval_emp_name")
        evaluation_date = st.date_input("Evaluation Date", datetime.date.today())
        evaluator = st.text_input("Evaluator's Name")
    
    with col2:
        time_spent = st.number_input("Time Spent on Tasks (hours)", min_value=0.0, max_value=24.0, value=1.0, step=0.5)
        overall_rating = st.select_slider(
            "Overall Performance Rating",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: f"{x} - {'Poor' if x == 1 else 'Fair' if x == 2 else 'Good' if x == 3 else 'Very Good' if x == 4 else 'Excellent'}"
        )
    
    st.divider()
    st.subheader("Task Selection and Rating")
    
    # Task selection with better organization
    selected_tasks = {}
    
    for category, tasks in evaluation_tasks.items():
        with st.expander(f"📋 {category} ({len(tasks)} tasks)", expanded=True):
            for task in tasks:
                col_task, col_rating = st.columns([3, 2])
                
                with col_task:
                    is_selected = st.checkbox(
                        f"**{task['task']}** ({task['frequency']})",
                        value=False,
                        key=f"checkbox_{task['task']}",
                        help=task['description']
                    )
                
                with col_rating:
                    if is_selected:
                        rating = st.select_slider(
                            f"Rating",
                            options=[1, 2, 3, 4, 5],
                            value=3,
                            key=f"rating_{task['task']}",
                            format_func=lambda x: f"{x} ⭐" if x == 1 else f"{x} ⭐⭐" if x == 2 else f"{x} ⭐⭐⭐" if x == 3 else f"{x} ⭐⭐⭐⭐" if x == 4 else f"{x} ⭐⭐⭐⭐⭐"
                        )
                        selected_tasks[task['task']] = {
                            'description': task['description'],
                            'rating': rating,
                            'category': category,
                            'frequency': task['frequency']
                        }
    
    st.divider()
    comments = st.text_area("Additional Comments and Observations", height=150, 
                           placeholder="Enter any specific observations, suggestions for improvement, or commendations...")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("✅ Submit Evaluation", type="primary", use_container_width=True):
            if not selected_tasks:
                st.error("⚠️ Please select at least one task to evaluate.")
            elif not employee_name or not evaluator:
                st.error("⚠️ Please provide both employee's name and evaluator's name.")
            else:
                add_evaluation(employee_name, evaluation_date, selected_tasks, comments, evaluator, overall_rating, time_spent)
                st.success(f"✅ Evaluation for {employee_name} added successfully!")
                st.balloons()
    
    with col_btn2:
        if st.button("🔄 Reset Form", use_container_width=True):
            st.rerun()

# TAB 2: VIEW EVALUATIONS
with tab2:
    st.header("View All Evaluations")
    
    if st.session_state['employee_evaluations']:
        # Filter options
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            filter_name = st.text_input("🔍 Filter by Employee Name", "")
        
        with col_f2:
            filter_evaluator = st.text_input("🔍 Filter by Evaluator", "")
        
        with col_f3:
            min_rating = st.slider("Minimum Overall Rating", 1, 5, 1)
        
        # Create detailed view
        filtered_evals = st.session_state['employee_evaluations'].copy()
        
        # Apply filters
        if filter_name:
            filtered_evals = [e for e in filtered_evals if filter_name.lower() in e['Employee Name'].lower()]
        if filter_evaluator:
            filtered_evals = [e for e in filtered_evals if filter_evaluator.lower() in e['Evaluator'].lower()]
        
        filtered_evals = [e for e in filtered_evals if e['Overall Rating'] >= min_rating]
        
        st.write(f"**Showing {len(filtered_evals)} of {len(st.session_state['employee_evaluations'])} evaluations**")
        
        # Display evaluations
        for idx, eval in enumerate(reversed(filtered_evals)):
            with st.expander(f"📄 {eval['Employee Name']} - {eval['Evaluation Date']} (Rating: {eval['Overall Rating']}/5)", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Employee:** {eval['Employee Name']}")
                    st.write(f"**Date:** {eval['Evaluation Date']}")
                
                with col2:
                    st.write(f"**Evaluator:** {eval['Evaluator']}")
                    st.write(f"**Time Spent:** {eval['Time Spent (hours)']} hours")
                
                with col3:
                    st.write(f"**Overall Rating:** {eval['Overall Rating']}/5 ⭐")
                    st.write(f"**Avg Task Rating:** {eval['Average Task Rating']:.2f}/5")
                
                st.divider()
                
                st.write("**Tasks Completed:**")
                for task_name, task_data in eval['Tasks'].items():
                    st.write(f"- **{task_name}** ({task_data['category']}): {task_data['rating']}/5 ⭐ - {task_data['frequency']}")
                
                if eval['Comments']:
                    st.write(f"**Comments:** {eval['Comments']}")
                
                # Delete button
                if st.button(f"🗑️ Delete Evaluation", key=f"delete_{idx}"):
                    st.session_state['employee_evaluations'].remove(eval)
                    st.rerun()
    else:
        st.info("📭 No evaluations have been added yet. Create your first evaluation in the 'New Evaluation' tab.")

# TAB 3: ANALYTICS
with tab3:
    st.header("Performance Analytics")
    
    if st.session_state['employee_evaluations']:
        # Overall statistics
        st.subheader("📊 Overall Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_evals = len(st.session_state['employee_evaluations'])
        unique_employees = len(set([e['Employee Name'] for e in st.session_state['employee_evaluations']]))
        avg_rating = sum([e['Overall Rating'] for e in st.session_state['employee_evaluations']]) / total_evals
        total_hours = sum([e['Time Spent (hours)'] for e in st.session_state['employee_evaluations']])
        
        with col1:
            st.metric("Total Evaluations", total_evals)
        with col2:
            st.metric("Unique Employees", unique_employees)
        with col3:
            st.metric("Average Rating", f"{avg_rating:.2f}/5")
        with col4:
            st.metric("Total Hours Logged", f"{total_hours:.1f}")
        
        st.divider()
        
        # Employee-specific analytics
        st.subheader("👤 Employee Performance Analysis")
        
        employee_names = sorted(set([e['Employee Name'] for e in st.session_state['employee_evaluations']]))
        selected_employee = st.selectbox("Select Employee", ["All Employees"] + employee_names)
        
        if selected_employee != "All Employees":
            stats = calculate_employee_stats(selected_employee)
            
            if stats:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Evaluations", stats['total_evaluations'])
                with col2:
                    st.metric("Avg Overall Rating", f"{stats['avg_overall_rating']:.2f}/5")
                with col3:
                    st.metric("Avg Task Rating", f"{stats['avg_task_rating']:.2f}/5")
                with col4:
                    st.metric("Total Hours", f"{stats['total_hours']:.1f}")
                
                st.write("**Most Performed Tasks:**")
                sorted_tasks = sorted(stats['task_counts'].items(), key=lambda x: x[1], reverse=True)[:10]
                for task, count in sorted_tasks:
                    avg_rating = stats['task_ratings'].get(task, 0)
                    st.write(f"- {task}: {count} times (Avg Rating: {avg_rating:.2f}/5)")
        else:
            # Show comparison across all employees
            st.write("**Performance Comparison Across All Employees:**")
            
            comparison_data = []
            for emp_name in employee_names:
                stats = calculate_employee_stats(emp_name)
                if stats:
                    comparison_data.append({
                        'Employee': emp_name,
                        'Evaluations': stats['total_evaluations'],
                        'Avg Overall Rating': round(stats['avg_overall_rating'], 2),
                        'Avg Task Rating': round(stats['avg_task_rating'], 2),
                        'Total Hours': round(stats['total_hours'], 1)
                    })
            
            if comparison_data:
                df_comparison = pd.DataFrame(comparison_data)
                st.dataframe(df_comparison, use_container_width=True)
    else:
        st.info("📭 No data available for analytics. Add some evaluations first!")

# TAB 4: EMPLOYEE MANAGEMENT
with tab4:
    st.header("Employee Management")
    
    st.write("**Quick Employee Overview:**")
    
    if st.session_state['employee_evaluations']:
        employee_names = sorted(set([e['Employee Name'] for e in st.session_state['employee_evaluations']]))
        
        for emp in employee_names:
            stats = calculate_employee_stats(emp)
            if stats:
                with st.expander(f"👤 {emp}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Total Evaluations:** {stats['total_evaluations']}")
                        st.write(f"**Average Overall Rating:** {stats['avg_overall_rating']:.2f}/5")
                    with col2:
                        st.write(f"**Average Task Rating:** {stats['avg_task_rating']:.2f}/5")
                        st.write(f"**Total Hours Worked:** {stats['total_hours']:.1f}")
                    
                    if stats['avg_overall_rating'] >= 4.5:
                        st.success("⭐ Outstanding Performance!")
                    elif stats['avg_overall_rating'] >= 3.5:
                        st.info("✓ Good Performance")
                    else:
                        st.warning("⚠️ Needs Improvement")
    else:
        st.info("No employees have been evaluated yet.")

# TAB 5: SETTINGS
with tab5:
    st.header("System Settings")
    
    st.subheader("📥 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export All Evaluations (JSON)", use_container_width=True):
            if st.session_state['employee_evaluations']:
                json_str = json.dumps(st.session_state['employee_evaluations'], indent=2)
                st.download_button(
                    label="💾 Download JSON",
                    data=json_str,
                    file_name=f"evaluations_{datetime.date.today()}.json",
                    mime="application/json"
                )
            else:
                st.warning("No evaluations to export.")
    
    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.checkbox("⚠️ I confirm I want to delete all evaluations"):
                st.session_state['employee_evaluations'] = []
                st.success("All data cleared!")
                st.rerun()
    
    st.divider()
    
    st.subheader("ℹ️ System Information")
    st.write(f"**Total Evaluations Stored:** {len(st.session_state['employee_evaluations'])}")
    st.write(f"**Total Task Categories:** {len(evaluation_tasks)}")
    st.write(f"**Total Available Tasks:** {sum([len(tasks) for tasks in evaluation_tasks.values()])}")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150/1f77b4/ffffff?text=Clean+Pro", use_container_width=True)
    
    st.header("📖 User Guide")
    
    st.markdown("""
    ### How to Use This System
    
    **1. Creating Evaluations:**
    - Navigate to the "New Evaluation" tab
    - Enter employee and evaluator information
    - Select tasks from the organized categories
    - Rate each task from 1-5 stars
    - Add detailed comments
    - Submit the evaluation
    
    **2. Viewing Data:**
    - Use the "View Evaluations" tab to see all records
    - Filter by employee name, evaluator, or rating
    - Expand individual evaluations for details
    - Delete evaluations if needed
    
    **3. Analytics:**
    - View overall system statistics
    - Analyze individual employee performance
    - Compare employees side-by-side
    - Identify top performers and areas for improvement
    
    **4. Best Practices:**
    - Conduct evaluations regularly (daily/weekly)
    - Be specific in comments
    - Use the full rating scale appropriately
    - Follow up on areas needing improvement
    - Recognize exceptional performance
    """)
    
    st.divider()
    
    st.header("🎯 Rating Guide")
    st.markdown("""
    - ⭐ (1) - Poor: Task not completed satisfactorily
    - ⭐⭐ (2) - Fair: Completed but with significant issues
    - ⭐⭐⭐ (3) - Good: Meets basic expectations
    - ⭐⭐⭐⭐ (4) - Very Good: Exceeds expectations
    - ⭐⭐⭐⭐⭐ (5) - Excellent: Outstanding performance
    """)
    
    st.divider()
    
    st.info("💡 **Tip:** Regular evaluations help maintain high cleaning standards and boost employee motivation!")
    
    st.caption("v2.0 | Enhanced Cleaning Evaluation System")
