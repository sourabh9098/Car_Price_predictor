import streamlit as st
import numpy as np
import joblib
import time

# ---------------- LOAD MODEL ----------------
model = joblib.load('ridge_model.pkl')
scaler = joblib.load('scaler.pkl')

st.set_page_config(page_title="Car Price AI", layout="wide")

# ---------------- MODERN UI STYLE ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: white;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 10px;
    font-size: 20px;
}

.slogan {
    text-align: center;
    color: #e2e8f0;
    font-size: 16px;
    margin-top: 10px;
    font-style: italic;
}

.card {
    background: rgba(30, 41, 59, 0.6);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
    backdrop-filter: blur(12px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 12px 40px rgba(0,0,0,0.6);
}

label {
    color: #e2e8f0 !important;
}

.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    color: white;
    border-radius: 12px;
    height: 3.5em;
    font-size: 18px;
    font-weight: 600;
}

.result-box {
    background: #020617;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>🚗 CHECK PRICE OF YOUR DREAM CAR</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>just enter details & get instant AI prediction</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2,1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Car Requirement")

    # SLOGAN INSIDE CARD (NEW POSITION)
    st.markdown("<div class='slogan'>A car is not just a machine; it is an emotion.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        enginesize = st.number_input("Engine Size", min_value=0.0)
        horsepower = st.number_input("Horse Power", min_value=0.0)
        citympg = st.number_input("City MPG", min_value=0.0)

    with col2:
        curbweight = st.number_input("Curb Weight", min_value=0.0)
        carwidth = st.number_input("Car Width", min_value=0.0)

    fueltype = st.selectbox("Fuel Type", ["gas", "diesel"])
    drivewheel = st.selectbox("Drive Wheel", ["fwd", "rwd", "4wd"])

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1555215695-3004980ad54e", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- ENCODING ----------------
fueltype_gas = 1 if fueltype == "gas" else 0

if drivewheel == "fwd":
    drivewheel_fwd = 1
    drivewheel_rwd = 0
elif drivewheel == "rwd":
    drivewheel_fwd = 0
    drivewheel_rwd = 1
else:
    drivewheel_fwd = 0
    drivewheel_rwd = 0

# ---------------- PREDICTION ----------------
if st.button("🚀 Predict Price"):
    try:
        with st.spinner("AI is analyzing..."):
            time.sleep(1)

            input_data = np.array([[enginesize, curbweight, horsepower, carwidth,
                                    citympg, fueltype_gas, drivewheel_fwd, drivewheel_rwd]])

            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)[0]

        # -------- Animated Counter --------
        display = st.empty()
        for i in np.linspace(0, prediction, 30):
            display.markdown(f"<div class='result-box'>💰 ₹ {i:,.0f}</div>", unsafe_allow_html=True)
            time.sleep(0.03)

        # Category
        if prediction < 10000:
            st.success("🚗 Budget Friendly Car")
        elif prediction < 30000:
            st.info("🚘 Mid Range Car")
        else:
            st.warning("🏎️ Premium Car")

        # Car Qualities
        st.markdown("""
        ### 🚘 Car Qualities
        ✔ Powerful Engine Performance  
        ✔ Fuel Efficient  
        ✔ Smooth Driving Experience  
        ✔ Stylish & Modern Design  
        ✔ Reliable & Durable
        """)

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("🚀 Built by Sourabh | AI Powered Car Price Predictor | Deploy Ready")