import streamlit as st
import json
import datetime
import random
import openai  # For AI-powered travel tips

# Mock Data
DESTINATIONS = ["International Space Station", "Lunar Hotel Orion", "Mars Habitat Alpha", "Titan Explorer Base"]
SEAT_CLASSES = {"Economy": 5000, "Business": 15000, "VIP Zero-Gravity": 50000}
MOCK_PACKAGES = [
    {"name": "Explorer Package", "price": 8000, "discount": "10% off for first-time travelers"},
    {"name": "Luxury Package", "price": 20000, "discount": "Includes VIP Lounge Access"},
]
ACCOMMODATIONS = {
    "International Space Station": "ISS Capsule Suites",
    "Lunar Hotel Orion": "Lunar Resort & Spa",
    "Mars Habitat Alpha": "Red Rock Domes",
    "Titan Explorer Base": "Subsurface Ice Vaults",
}

# Persistent storage for user bookings
if "user_bookings" not in st.session_state:
    st.session_state.user_bookings = []


# Function to get AI-powered travel tips
def get_travel_tips():
    general_tips = "1. Stay hydrated in microgravity. 2. Secure loose items. 3. Follow space station protocols."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "system", "content": "Provide travel tips for space tourists."}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return general_tips


# Home Page
def home():
    st.title("🚀 Welcome to Space Travel Booking!")
    st.image("https://source.unsplash.com/800x400/?space,stars", use_column_width=True)
    st.markdown("Book your dream space journey today!")

    if st.session_state.user_bookings:
        st.subheader("Your Upcoming Trips")
        for booking in st.session_state.user_bookings:
            st.write(f"🌍 Destination: {booking['destination']}")
            st.write(f"🛫 Departure Date: {booking['date']}")
            st.write(f"💺 Seat Class: {booking['seat_class']}")
            st.write(f"💵 Price: ${booking['price']}")
            st.divider()


# Booking Page
def booking():
    st.title("🛰️ Book Your Space Adventure")
    destination = st.selectbox("Choose Your Destination", DESTINATIONS)
    departure_date = st.date_input("Select Departure Date", datetime.date.today())
    seat_class = st.radio("Choose Seat Class", list(SEAT_CLASSES.keys()))
    price = SEAT_CLASSES[seat_class]

    if st.button("Book Now"):
        booking_data = {
            "destination": destination,
            "date": departure_date.strftime("%Y-%m-%d"),
            "seat_class": seat_class,
            "price": price,
        }
        st.session_state.user_bookings.append(booking_data)
        st.success(f"Trip to {destination} on {departure_date} confirmed! Your {seat_class} ticket costs ${price}.")


# Pricing Page
def pricing():
    st.title("💰 Pricing & Packages")
    for package in MOCK_PACKAGES:
        st.subheader(package["name"])
        st.write(f"**Price:** ${package['price']}")
        st.write(f"**Special Offer:** {package['discount']}")


# Dashboard Page
def dashboard():
    st.title("👤 Your Dashboard")
    if st.session_state.user_bookings:
        st.subheader("Upcoming Trips")
        for booking in st.session_state.user_bookings:
            trip_date = datetime.datetime.strptime(booking["date"], "%Y-%m-%d").date()
            countdown = (trip_date - datetime.date.today()).days
            st.write(f"🚀 {booking['destination']} - {booking['seat_class']} class, ${booking['price']}")
            st.write(f"Countdown: {countdown} days left! 🕒")
            st.divider()
    else:
        st.write("No upcoming trips. Book your adventure now!")

    st.subheader("✨ AI-Powered Travel Tips")
    st.write(get_travel_tips())


# Sidebar Navigation
st.sidebar.title("🌌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Booking", "Pricing", "Dashboard"])

if page == "Home":
    home()
elif page == "Booking":
    booking()
elif page == "Pricing":
    pricing()
elif page == "Dashboard":
    dashboard()
