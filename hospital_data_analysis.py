import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Hospital Patient Analysis Dashboard")

st.write("Analyze hospital patients, diseases, departments and revenue.")

df = pd.read_csv("hospital_patient_sample.csv")


df = df.drop_duplicates(subset="Patient_ID")

df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"], errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"], errors="coerce"
)


st.subheader("Hospital Patient Dataset")

st.dataframe(df)


department = st.sidebar.selectbox(
    "Select Department",
    ["All"] + sorted(df["Department"].dropna().unique().tolist())
)

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["Gender"].dropna().unique().tolist())
)

disease = st.sidebar.selectbox(
    "Select Disease",
    ["All"] + sorted(df["Disease"].dropna().unique().tolist())
)

status = st.sidebar.selectbox(
    "Select Patient Status",
    ["All"] + sorted(df["Patient_Status"].dropna().unique().tolist())
)



filtered_data = df.copy()

if department != "All":
    filtered_data = filtered_data[
        filtered_data["Department"] == department
    ]

if gender != "All":
    filtered_data = filtered_data[
        filtered_data["Gender"] == gender
    ]

if disease != "All":
    filtered_data = filtered_data[
        filtered_data["Disease"] == disease
    ]

if status != "All":
    filtered_data = filtered_data[
        filtered_data["Patient_Status"] == status
    ]


total_patients = len(filtered_data)

if total_patients > 0:

    average_age = filtered_data["Age"].mean()

    maximum_age = filtered_data["Age"].max()

    total_revenue = filtered_data["Total_Bill_INR"].sum()

    average_bill = filtered_data["Total_Bill_INR"].mean()

    st.subheader("Hospital Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Patients", total_patients)

    c2.metric(
        "Average Age",
        f"{average_age:.2f} years"
    )

    c3.metric(
        "Maximum Age",
        maximum_age
    )

    c4.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

    st.subheader("Department-wise Patient Analysis")

    department_data = filtered_data[
        "Department"
    ].value_counts()

    st.bar_chart(department_data)

    st.subheader("Disease Analysis")

    disease_data = filtered_data[
        "Disease"
    ].value_counts()

    st.bar_chart(disease_data)

    st.subheader("Gender Analysis")

    gender_data = filtered_data[
        "Gender"
    ].value_counts()

    st.bar_chart(gender_data)


    st.subheader("Patient Status Analysis")

    status_data = filtered_data[
        "Patient_Status"
    ].value_counts()

    st.bar_chart(status_data)

    st.subheader("Department-wise Revenue Analysis")

    revenue_data = filtered_data.groupby(
        "Department"
    )["Total_Bill_INR"].sum()

    st.bar_chart(revenue_data)

    st.subheader("Monthly Admission Analysis")

    monthly_data = filtered_data.dropna(
        subset=["Admission_Date"]
    ).copy()

    monthly_data["Month"] = (
        monthly_data["Admission_Date"].dt.strftime("%Y-%m")
    )

    monthly_admissions = monthly_data.groupby(
        "Month"
    ).size()

    st.line_chart(monthly_admissions)

    st.subheader("Average Treatment Cost")

    average_cost = filtered_data.groupby(
        "Disease"
    )["Total_Bill_INR"].mean()

    st.bar_chart(average_cost)



    st.subheader("Department Summary")

    summary = filtered_data.groupby("Department").agg(
        Total_Patients=("Patient_ID", "count"),
        Average_Age=("Age", "mean"),
        Total_Revenue=("Total_Bill_INR", "sum")
    ).reset_index()

    st.dataframe(summary)

    st.subheader("Average Hospital Bill")

    st.write(
        "Average Bill Amount: ₹",
        round(average_bill, 2)
    )

else:

    st.warning("No patient data found for selected filters.")

st.success("Hospital Patient Analysis Completed!")