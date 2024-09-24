import streamlit as st
import pandas as pd
import datetime

# Define the list of tasks for employee evaluation
evaluation_tasks = [
    # General Cleaning
    {
        "task": "Consistently empties trash bins and replaces liners",
        "description": "Ensure trash bins are emptied regularly and liners are replaced to maintain hygiene and prevent odors."
    },
    {
        "task": "Cleans and disinfects restrooms (toilets, sinks, mirrors, floors)",
        "description": "Thoroughly clean and disinfect all restroom fixtures and surfaces, ensuring a hygienic environment for users."
    },
    {
        "task": "Wipes and sanitizes door handles and light switches",
        "description": "Regularly sanitize high-touch areas to prevent the spread of germs and ensure employee health."
    },
    {
        "task": "Cleans kitchen surfaces and appliances thoroughly",
        "description": "Ensure all kitchen surfaces, including counters and appliances, are cleaned daily to promote cleanliness."
    },
    {
        "task": "Dusts and wipes down all furniture surfaces",
        "description": "Keep furniture free of dust and dirt to maintain a clean appearance and contribute to a healthy workspace."
    },
    {
        "task": "Vacuums carpets and rugs properly",
        "description": "Vacuum carpets and rugs thoroughly to remove dust, dirt, and allergens, ensuring a healthier environment."
    },
    {
        "task": "Mops hard floors using appropriate cleaning solutions",
        "description": "Use suitable cleaning solutions to mop and maintain hard floor surfaces, ensuring they are safe and clean."
    },
    {
        "task": "Cleans glass doors and windows streak-free",
        "description": "Ensure all glass surfaces are cleaned to a streak-free shine, enhancing the appearance of the facility."
    },
    {
        "task": "Sanitizes shared equipment (printers, copiers, etc.)",
        "description": "Regularly sanitize equipment that is shared among employees to reduce the risk of contamination."
    },
    {
        "task": "Restocks cleaning supplies and reports low inventory",
        "description": "Keep track of cleaning supply levels and report any shortages to ensure uninterrupted cleaning operations."
    },
    # Safety and Compliance
    {
        "task": "Follows safety protocols while handling chemicals",
        "description": "Adhere to safety guidelines when using cleaning chemicals to protect personal safety and compliance."
    },
    {
        "task": "Uses personal protective equipment (PPE) consistently",
        "description": "Always wear appropriate PPE when performing cleaning tasks to ensure personal safety and health."
    },
    {
        "task": "Reports safety hazards or maintenance issues promptly",
        "description": "Report any safety hazards or maintenance issues immediately to maintain a safe working environment."
    },
    {
        "task": "Ensures proper labeling of cleaning supplies",
        "description": "Make sure all cleaning supplies are clearly labeled for safety and to prevent misuse."
    },
    {
        "task": "Keeps work areas clean and organized",
        "description": "Maintain cleanliness and organization in work areas at all times to promote efficiency."
    },
    # Specialized Cleaning
    {
        "task": "Conducts deep cleaning of carpets and upholstery regularly",
        "description": "Perform deep cleaning on carpets and upholstery to maintain hygiene and extend the life of the materials."
    },
    {
        "task": "Performs floor stripping and waxing as needed",
        "description": "Stripping and waxing floors as part of the maintenance schedule to maintain their appearance and durability."
    },
    {
        "task": "Cleans air conditioning vents and filters",
        "description": "Regularly clean AC vents and change filters to ensure optimal air quality and equipment efficiency."
    },
    {
        "task": "Maintains and sanitizes gym equipment (if applicable)",
        "description": "Regularly clean and sanitize gym equipment for user safety and satisfaction."
    },
    {
        "task": "Cleans kitchen appliances (microwave, refrigerator, etc.) thoroughly",
        "description": "Ensure all kitchen appliances are cleaned to remove dirt and stains for hygiene and functionality."
    },
    # Customer Service
    {
        "task": "Responds promptly to client requests or concerns",
        "description": "Address client requests and concerns in a timely manner to ensure client satisfaction."
    },
    {
        "task": "Maintains a professional demeanor when interacting with clients",
        "description": "Always be courteous and professional when dealing with clients to uphold the company's reputation."
    },
    {
        "task": "Reports client feedback and suggestions to management",
        "description": "Relay client feedback and suggestions to improve service quality and client relations."
    },
    {
        "task": "Demonstrates attention to detail in cleaning tasks",
        "description": "Ensure all cleaning tasks are performed with a high level of detail to meet quality standards."
    },
    {
        "task": "Follows client-specific cleaning protocols or preferences",
        "description": "Adhere to any specific cleaning protocols requested by clients to ensure their satisfaction."
    },
    # Equipment Maintenance
    {
        "task": "Cleans and maintains cleaning equipment after use",
        "description": "Clean and maintain all cleaning equipment after each use to ensure longevity and performance."
    },
    {
        "task": "Reports malfunctioning equipment immediately",
        "description": "Report any equipment malfunctions to management as soon as possible to avoid disruptions."
    },
    {
        "task": "Checks and replaces vacuum bags and filters as needed",
        "description": "Regularly check and replace vacuum bags and filters for optimal cleaning performance."
    },
    {
        "task": "Keeps janitor's closet organized and stocked",
        "description": "Maintain organization and stock levels in the janitor's closet for efficiency and access."
    },
    {
        "task": "Inspects cleaning equipment regularly for wear and tear",
        "description": "Inspect cleaning equipment regularly to identify any maintenance needs and prevent breakdowns."
    },
    # Time Management
    {
        "task": "Completes assigned tasks within the scheduled time",
        "description": "Ensure all tasks are completed within the designated time frame to meet operational needs."
    },
    {
        "task": "Prioritizes tasks effectively based on urgency",
        "description": "Assess and prioritize tasks based on their urgency and importance for efficient workflow."
    },
    {
        "task": "Manages breaks and work hours appropriately",
        "description": "Take breaks at appropriate times to maintain productivity and compliance with labor laws."
    },
    {
        "task": "Adjusts schedule based on immediate cleaning needs",
        "description": "Be flexible and adjust the cleaning schedule as needed to address urgent situations."
    },
    {
        "task": "Communicates progress on tasks to supervisors",
        "description": "Keep supervisors informed about the progress of assigned tasks to ensure accountability."
    },
    # Teamwork and Communication
    {
        "task": "Works collaboratively with other team members",
        "description": "Foster a collaborative work environment by working effectively with team members."
    },
    {
        "task": "Participates in team meetings and training sessions",
        "description": "Actively participate in all team meetings and training to improve team cohesion and skills."
    },
    {
        "task": "Communicates clearly with team regarding cleaning needs",
        "description": "Ensure clear communication regarding cleaning needs with the team for seamless operations."
    },
    {
        "task": "Assists team members when they require help",
        "description": "Provide assistance to team members when they need support to foster teamwork."
    },
    {
        "task": "Shares cleaning tips and techniques with colleagues",
        "description": "Share effective cleaning methods and tips with the team to enhance overall performance."
    },
    # Quality of Work
    {
        "task": "Demonstrates thoroughness in all cleaning tasks",
        "description": "Complete all cleaning tasks with thoroughness and attention to detail to exceed expectations."
    },
    {
        "task": "Ensures high standards of cleanliness are met",
        "description": "Maintain high cleanliness standards in all areas of work to reflect positively on the organization."
    },
    {
        "task": "Double-checks work for missed areas or details",
        "description": "Review work to ensure no areas were missed and rectify any oversights."
    },
    {
        "task": "Receives positive feedback from clients and management",
        "description": "Collect and maintain records of positive feedback received to track performance."
    },
    {
        "task": "Implements feedback to improve cleaning techniques",
        "description": "Use feedback to continuously improve cleaning methods for better results."
    },
    # Adaptability and Learning
    {
        "task": "Adapts to new cleaning methods and technologies",
        "description": "Be open and adaptable to new cleaning techniques and technologies to stay current."
    },
    {
        "task": "Takes initiative to learn about new products",
        "description": "Proactively seek information about new cleaning products to enhance cleaning effectiveness."
    },
    {
        "task": "Shows willingness to take on additional responsibilities",
        "description": "Be willing to take on extra tasks as needed to support the team."
    },
    {
        "task": "Participates in ongoing training and development",
        "description": "Engage in ongoing training to improve skills and adapt to changing needs."
    },
    {
        "task": "Provides suggestions for improving cleaning processes",
        "description": "Offer suggestions for enhancing current cleaning processes to improve efficiency."
    },
    # Miscellaneous
    {
        "task": "Follows the company's code of conduct",
        "description": "Adhere to all company policies and procedures to maintain professionalism."
    },
    {
        "task": "Respects the privacy of clients and coworkers",
        "description": "Maintain confidentiality regarding all client and coworker information."
    },
    {
        "task": "Demonstrates punctuality and reliability",
        "description": "Arrive on time and be dependable to ensure smooth operations."
    },
    {
        "task": "Maintains a positive attitude towards work",
        "description": "Keep a positive demeanor while performing duties to contribute to a healthy workplace."
    },
    {
        "task": "Embraces feedback as a tool for improvement",
        "description": "Accept feedback graciously and use it as an opportunity to grow and enhance performance."
    },
]

def create_employee_evaluation_df(employee_name, evaluation_date):
    """Create a DataFrame to hold employee evaluation data."""
    return pd.DataFrame({
        "Task": [task["task"] for task in evaluation_tasks],
        "Description": [task["description"] for task in evaluation_tasks],
        "Completed": [False] * len(evaluation_tasks),
        "Evaluator": [None] * len(evaluation_tasks),
        "Comments": [None] * len(evaluation_tasks),
    })

def main():
    st.title("Employee Cleaning Task Evaluation")

    # Input employee name and evaluation date
    employee_name = st.text_input("Employee Name", "")
    evaluation_date = st.date_input("Evaluation Date", datetime.date.today())

    if employee_name:
        df = create_employee_evaluation_df(employee_name, evaluation_date)
        
        # Display the tasks for evaluation
        st.write(f"### Evaluation Tasks for {employee_name} on {evaluation_date}")
        st.dataframe(df)

        # Task completion section
        st.write("### Task Completion")
        for index, row in df.iterrows():
            col1, col2 = st.columns([1, 4])
            with col1:
                completed = st.checkbox(f"Complete {row['task']}", value=row['Completed'], key=f"completed_{index}")
            with col2:
                evaluator = st.text_input(f"Evaluator for {row['task']}", key=f"evaluator_{index}")
                comments = st.text_area(f"Comments for {row['task']}", value=row['Comments'], key=f"comments_{index}")

            if completed:
                df.at[index, 'Completed'] = True
                df.at[index, 'Evaluator'] = evaluator
                df.at[index, 'Comments'] = comments

        # Save button
        if st.button("Save Evaluation"):
            st.success("Evaluation saved successfully!")
            st.write(df)

if __name__ == "__main__":
    main()
