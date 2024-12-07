import gradio as gr
from gradio.components import Number, Dropdown
import numpy as np
import pandas as pd
import pickle

# Load exported data
exported_data_path = 'src\Components\ML\my_exported_data.pkl'
with open(exported_data_path, 'rb') as file:
    exported_data = pickle.load(file)

# Load the exported components
categorical_imputer = exported_data['categorical_imputer']
numerical_imputer = exported_data['numerical_imputer']
encoder = exported_data['encoder']
scaler = exported_data['scaler']
best_model = exported_data['best_model']

# Define your prediction function for the new app
def deposit_subscription_prediction(age, job, marital, education, default, housing, loan, contact, month, 
                                    day_of_week, campaign, pdays, previous, poutcome, emp_var_rate, cons_price_idx,
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
        'campaign': [campaign],
        'pdays': [pdays],
        'previous': [previous],
        'poutcome': [poutcome],
        'emp.var.rate': [emp_var_rate],
        'cons.price.idx': [cons_price_idx],
        'cons.conf.idx': [cons_conf_idx],
        'euribor3m': [euribor3m],
        'nr.employed': [nr_employed]
    })

    # Preprocessing for categorical data
    prediction_data_categorical = prediction_data.select_dtypes(include='object')
    prediction_data_encoded = encoder.transform(categorical_imputer.transform(prediction_data_categorical))

    # Convert the encoded sparse matrix to a DataFrame
    prediction_data_encoded_df = pd.DataFrame.sparse.from_spmatrix(prediction_data_encoded,
                                                                  columns=encoder.get_feature_names_out(prediction_data_categorical.columns),
                                                                  index=prediction_data_categorical.index)

    # Preprocessing for numerical data
    prediction_data_numerical = prediction_data.select_dtypes(include=['int', 'float'])
    prediction_data_scaled = scaler.transform(numerical_imputer.transform(prediction_data_numerical))

    # Convert the scaled numerical data to a DataFrame
    prediction_data_scaled_df = pd.DataFrame(prediction_data_scaled,
                                             columns=prediction_data_numerical.columns,
                                             index=prediction_data_numerical.index)

    # Concatenate the encoded categorical data and scaled numerical data
    prediction_data_preprocessed = pd.concat([prediction_data_encoded_df, prediction_data_scaled_df], axis=1)

    # Make predictions using the loaded model
    predictions = best_model.predict(prediction_data_preprocessed)

    # Map the predictions to 'Yes' or 'No'
    prediction_label = 'Subscribed to Deposit' if predictions[0] == 1 else 'Not Subscribed to Deposit'

    return prediction_label


# Define input components for the Gradio interface
input_components = [
    gr.Number(label='age: Enter the age of the customer.', minimum=18, maximum=100),
    gr.Dropdown(choices=['blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'admin.', 'unknown'], label='job: Select the job type of the customer.'),
    gr.Dropdown(choices=['single', 'married', 'divorced'], label='marital: Select the marital status of the customer.'),
    gr.Dropdown(choices=['basic.4y', 'basic.6y', 'basic.9y', 'high.school', 'illiterate', 'professional.course', 'university.degree', 'unknown'], label='education: Select the education level of the customer.'),
    gr.Dropdown(choices=['no', 'yes'], label='default: Select if the customer has credit in default.'),
    gr.Dropdown(choices=['no', 'yes'], label='housing: Select if the customer has housing loan.'),
    gr.Dropdown(choices=['no', 'yes'], label='loan: Select if the customer has personal loan.'),
    gr.Dropdown(choices=['cellular', 'telephone', 'unknown'], label='contact: Select the communication type used for contact.'),
    gr.Dropdown(choices=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], label='month: Select the last contact month of the customer.'),
    gr.Dropdown(choices=['mon', 'tue', 'wed', 'thu', 'fri'], label='day_of_week: Select the last contact day of the week.'),
    gr.Number(label='campaign: Enter the number of contacts performed during the campaign.', minimum=0, maximum=100),
    gr.Number(label='pdays: Enter the number of days since the client was last contacted.', minimum=-1, maximum=1000),
    gr.Number(label='previous: Enter the number of contacts performed before this campaign.', minimum=0, maximum=100),
    gr.Dropdown(choices=['failure', 'nonexistent', 'success', 'unknown'], label='poutcome: Select the outcome of the previous marketing campaign.'),
    gr.Number(label='emp.var.rate: Enter the employment variation rate.', minimum=-3.0, maximum=3.0),
    gr.Number(label='cons.price.idx: Enter the consumer price index.', minimum=92.0, maximum=95.0),
    gr.Number(label='cons.conf.idx: Enter the consumer confidence index.', minimum=-50.0, maximum=50.0),
    gr.Number(label='euribor3m: Enter the Euribor 3 month rate.', minimum=0.0, maximum=6.0),
    gr.Number(label='nr.employed: Enter the number of employees.', minimum=1000.0, maximum=6000.0)
]

# Create Gradio interface
gr.Interface(fn=deposit_subscription_prediction, inputs=input_components, outputs="text").launch()

# Create and launch the Gradio interface
iface = gr.Interface(
    fn=deposit_subscription_prediction,
    inputs=input_components,
    outputs="text",
    title="Customer Churn Prediction", 
    description="This app Predict customer churn using machine learning. It Provides stakeholders & Customers information to predict whether they are likely to leave(Churn) a telecommunications company or stay.",
    live=False,  
    # share=True
)

iface.launch()