
import streamlit as st
import json
import os
from datetime import datetime
---------------- Page Configuration ----------------
st.set_page_config(
page_title="Smart Home Device Manager",
page_icon="🏠",
layout="wide",
initial_sidebar_state="expanded"
)
---------------- Data File ----------------
DATA_FILE = "devices.json"
def load_devices():
"""Load devices from JSON file."""
if os.path.exists(DATA_FILE):
try:
with open(DATA_FILE, "r", encoding="utf-8") as f:
return json.load(f)
except Exception:
return []
return []
def save_devices(devices):
"""Save devices to JSON file."""
with open(DATA_FILE, "w", encoding="utf-8") as f:
json.dump(devices, f, indent=2)
---------------- Session State ----------------
if "devices" not in st.session_state:
st.session_state.devices = load_devices()
devices = st.session_state.devices
---------------- Sidebar ----------------
st.sidebar.title("🏠 Smart Device Manager")
st.sidebar.markdown("Bright Minds Academy")
menu = st.sidebar.radio(
"Menu",
[
"📋 Dashboard",
"➕ Add Device",
"🔄 Update Status",
"🔍 Search Device",
"📊 All Devices",
],
)
st.sidebar.markdown("---")
st.sidebar.info("Python + Streamlit | ACCA5036 Coursework")
---------------- Main Title ----------------
st.title("Smart Home Device Manager")
st.markdown(
"Centralized Management System for Bright Minds Academy Smart Classroom"
)
==================================================
Dashboard
==================================================
if menu == "📋 Dashboard":
st.header("📊 Overview")
col1, col2, col3, col4 = st.columns(4)
total = len(devices)
online = len([d for d in devices if d.get("status") == "online"])
offline = len([d for d in devices if d.get("status") == "offline"])
maintenance = len(
[d for d in devices if d.get("status") == "maintenance"]
)
col1.metric("Total Devices", total)
col2.metric("Online", online)
col3.metric("Offline", offline)
col4.metric("Maintenance", maintenance)
if devices:
st.subheader("Recent Devices")
st.dataframe(devices[-5:], use_container_width=True)
==================================================
Add Device
==================================================
elif menu == "➕ Add Device":
st.header("➕ Add New Device")
with st.form("add_form"):
name = st.text_input(
"Device Name",
placeholder="Smart Light A1",
)
room = st.text_input(
"Room / Location",
placeholder="Classroom B2",
)
status = st.selectbox(
"Initial Status",
["online", "offline", "maintenance"],
)
submitted = st.form_submit_button("Add Device")
if submitted:
if not name or not room:
st.error("Device name and room are required!")
elif any(
d["name"].lower() == name.lower()
for d in devices
):
st.error("Device with this name already exists!")
else:
new_device = {
"name": name.strip(),
"room": room.strip(),
"status": status,
"added_date": datetime.now().strftime(
"%Y-%m-%d %H:%M"
),
}
devices.append(new_device)
save_devices(devices)
st.success(
f"✅ Device '{name}' added successfully!"
)
st.balloons()
==================================================
Update Status
==================================================
elif menu == "🔄 Update Status":
st.header("🔄 Update Device Status")
if not devices:
st.warning("No devices found. Add some first!")
else:
device_names = [d["name"] for d in devices]
selected_name = st.selectbox(
"Select Device",
device_names,
)
device = next(
(
d
for d in devices
if d["name"] == selected_name
),
None,
)
if device:
st.info(
f"Current Status: {device['status'].upper()} | Room: {device['room']}"
)
statuses = [
"online",
"offline",
"maintenance",
]
new_status = st.radio(
"New Status",
statuses,
index=statuses.index(device["status"]),
)
if st.button(
"Update Status",
type="primary",
):
device["status"] = new_status
save_devices(devices)
st.success(
f"Status updated to {new_status} for {selected_name}"
)
==================================================
Search Device
==================================================
elif menu == "🔍 Search Device":
st.header("🔍 Search Device")
search_term = st.text_input(
"Enter Device Name"
)
if search_term:
results = [
d
for d in devices
if search_term.lower()
in d["name"].lower()
]
if results:
for dev in results:
st.success(
f"{dev['name']} | Room: {dev['room']} | Status: {dev['status'].upper()}"
)
else:
st.error(
"No matching device found."
)
==================================================
All Devices
==================================================
elif menu == "📊 All Devices":
st.header("📋 All Devices")
if not devices:
st.info(
"No devices yet. Add some from the sidebar."
)
else:
filter_term = st.text_input(
"Filter by name or room",
"",
)
filtered = devices
if filter_term:
filtered = [
d
for d in devices
if filter_term.lower()
in d["name"].lower()
or filter_term.lower()
in d["room"].lower()
]
st.dataframe(
filtered,
use_container_width=True,
column_config={
"name": "Device Name",
"room": "Location",
"status": st.column_config.TextColumn(
"Status"
),
"added_date": "Added On",
},
)
if st.button("Download as JSON"):
st.download_button(
label="📥 Download devices.json",
data=json.dumps(
devices,
indent=2,
),
file_name="devices_backup.json",
mime="application/json",
)
---------------- Footer ----------------
st.sidebar.markdown("---")
st.caption(
"© Bright Minds Academy | Built with Streamlit for ACCA5036"
)
