import streamlit as st
from forex_python.converter import CurrencyRates

# Set page configuration
st.set_page_config(
    page_title="CloudExpense Wizard",
    page_icon="🌌",
    layout="wide"
)

# Define background images for each cloud provider
background_images = {
    "AWS": "https://d1.awsstatic.com/logos/aws_logo_smile_1200x630.7907552b6930f0f7d824b17f2f4a1b8f.751c4c7601c6b7c1a32b.png",
    "Azure": "https://azurecomcdn.azureedge.net/mediahandler/acomblog/media/Default/blog/13469/azure_hero.png",
    "Google Cloud": "https://storage.googleapis.com/gweb-cloudblog-publish/original_images/GCP.jpg"
}

def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize currency converter
currency_rates = CurrencyRates()

def convert_currency(amount, to_currency):
    try:
        rate = currency_rates.get_rate('USD', to_currency)
        converted_amount = amount * rate
        return converted_amount, rate
    except Exception as e:
        st.error(f"Error converting currency: {e}")
        return None, None

# Main UI
st.title("✨ CloudExpense Wizard ✨")
provider = st.selectbox("Select your Cloud Provider", ["AWS", "Azure", "Google Cloud"])

# Set background based on selected provider
set_background(background_images[provider])

st.markdown(
    f"""<div style="font-size: 24px; text-align: center; font-weight: bold;">
        Welcome to the <span style="color: #ff5722;">{provider}</span> cost analysis dashboard!
    </div>""",
    unsafe_allow_html=True
)

# Inputs for cost estimation
st.header("Analyze your Cloud Costs")
instances = st.number_input("Enter the number of instances:", min_value=1, value=1)
hours = st.number_input("Enter the usage hours per month:", min_value=1, value=720)
storage = st.number_input("Enter storage size (in GB):", min_value=1, value=50)

# Cost estimation logic
cost_per_instance = {
    "AWS": 0.05,
    "Azure": 0.045,
    "Google Cloud": 0.04
}
storage_cost = {
    "AWS": 0.023,
    "Azure": 0.02,
    "Google Cloud": 0.018
}

instance_cost = instances * hours * cost_per_instance[provider]
storage_cost_total = storage * storage_cost[provider]
total_cost_usd = instance_cost + storage_cost_total

# Currency conversion
st.subheader("Currency Conversion")
currency = st.selectbox("Choose your currency:", ["USD", "INR", "GBP", "EUR"])
if currency == "USD":
    converted_cost = total_cost_usd
    conversion_rate = 1.0
else:
    converted_cost, conversion_rate = convert_currency(total_cost_usd, currency)

if converted_cost is not None:
    st.metric(label=f"Your Estimated Cost ({currency})", value=f"{converted_cost:.2f}")
    st.caption(f"Conversion rate: 1 USD = {conversion_rate:.4f} {currency}")

# Cost breakdown
st.subheader("Cost Breakdown")
st.write(f"Cost for Instances: {instance_cost:.2f} USD")
st.write(f"Cost for Storage: {storage_cost_total:.2f} USD")

# Optimization suggestions
st.header("Optimization Suggestions")
if provider == "AWS":
    st.write("- Use Reserved Instances for long-term savings.")
    st.write("- Utilize Spot Instances for non-critical workloads.")
elif provider == "Azure":
    st.write("- Optimize with Azure Advisor recommendations.")
    st.write("- Use Azure Hybrid Benefit for Windows Server and SQL Server.")
elif provider == "Google Cloud":
    st.write("- Commit to Sustained Use Discounts.")
    st.write("- Use Preemptible VMs for short-term tasks.")
