import gradio as gr
import pandas as pd
import joblib

# Load the trained pipeline
pipeline_path = 'src/Asset/ML/randomforest_pipeline.pkl'
model_pipeline = joblib.load(pipeline_path)

# Define your prediction function
def deposit_subscription_prediction(age, job, marital, education, default, housing, loan, contact, month, 
                                    day_of_week, duration, campaign, pdays, previous, poutcome, emp_var_rate, cons_price_idx,
                                    cons_conf_idx, euribor3m, nr_employed):
    # Create a DataFrame with the provided inputs
    prediction_data = pd.DataFrame({
        'age': [age],
        'job': [job],
        'marital': [marital],
        'education': [education],
        'default': [default],
        'housing': [housing],
        'loan': [loan],
        'contact': [contact],
        'month': [month],
        'day_of_week': [day_of_week],
        'duration': [duration],
        'campaign': [campaign],
        'pdays': [pdays],
        'previous': [previous],
        'poutcome': [poutcome],
        'emp_var_rate': [emp_var_rate],
        'cons_price_idx': [cons_price_idx],
        'cons_conf_idx': [cons_conf_idx],
        'euribor3m': [euribor3m],
        'nr_employed': [nr_employed]
    })

    # Make predictions using the pipeline
    prediction = model_pipeline.predict(prediction_data)[0]

    # Map the prediction to a label
    prediction_label = 'Subscribed to Deposit' if prediction == 1 else 'Not Subscribed to Deposit'

    return prediction_label

# Define input components for the Gradio interface
input_components = [
    gr.Number(label='Age: Enter the age of the customer.', minimum=17, maximum=98),
    gr.Dropdown(choices=['blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'admin.', 'unknown'], label='Job: Select the job type of the customer.'),
    gr.Dropdown(choices=['single', 'married', 'divorced'], label='Marital: Select the marital status of the customer.'),
    gr.Dropdown(choices=['basic.4y', 'basic.6y', 'basic.9y', 'high.school', 'illiterate', 'professional.course', 'university.degree', 'unknown'], label='Education: Select the education level of the customer.'),
    gr.Dropdown(choices=['no', 'yes'], label='Default: Select if the customer has credit in default.'),
    gr.Dropdown(choices=['no', 'yes'], label='Housing: Select if the customer has a housing loan.'),
    gr.Dropdown(choices=['no', 'yes'], label='Loan: Select if the customer has a personal loan.'),
    gr.Dropdown(choices=['cellular', 'telephone', 'unknown'], label='Contact: Select the communication type used for contact.'),
    gr.Dropdown(choices=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], label='Month: Select the last contact month of the customer.'),
    gr.Dropdown(choices=['mon', 'tue', 'wed', 'thu', 'fri'], label='Day of Week: Select the last contact day of the week.'),
    gr.Number(label='Duration: Enter the duration of the last contact in seconds.', minimum=0, maximum=4918),
    gr.Number(label='Campaign: Enter the number of contacts performed during the campaign.', minimum=1, maximum=56),
    gr.Number(label='Pdays: Enter the number of days since the client was last contacted.', minimum=-1, maximum=999),
    gr.Number(label='Previous: Enter the number of contacts performed before this campaign.', minimum=0, maximum=7),
    gr.Dropdown(choices=['failure', 'nonexistent', 'success', 'unknown'], label='Poutcome: Select the outcome of the previous marketing campaign.'),
    gr.Number(label='Employment Variation Rate: Enter the employment variation rate.', minimum=-3.40, maximum=1.40),
    gr.Number(label='Consumer Price Index: Enter the consumer price index.', minimum=92.0, maximum=95.0),
    gr.Number(label='Consumer Confidence Index: Enter the consumer confidence index.', minimum=-51.0, maximum=-27.0),
    gr.Number(label='Euribor 3 Month Rate: Enter the Euribor 3 month rate.', minimum=0.63, maximum=5.0),
    gr.Number(label='Number of Employees: Enter the number of employees.', minimum=4965, maximum=5228)
]

# Create and launch the Gradio interface
iface = gr.Interface(
    fn=deposit_subscription_prediction,
    inputs=input_components,
    outputs="text",
    title="Deposit Subscription Prediction",
    description="Predict whether a customer will subscribe to a term deposit using machine learning. Enter customer information to get a prediction.",
    live=False
)

iface.launch()



























