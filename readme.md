# 📊 PayGaze: UPI Transactions Analytics Dashboard

**PayGaze** is a powerful, interactive dashboard built using [PhonePe Pulse data](https://github.com/PhonePe/pulse) to visualize and analyze India's UPI transaction trends.

Explore UPI transactions across Indian states and quarters through choropleth maps, comparison graphs, downloadable charts, and more — all in one place.


---

## 🚀 Live Demo

🔗 [https://paygaze-io.streamlit.app](https://paygaze-io.streamlit.app)  
_Deployed on Streamlit Cloud_

---

## ✨ Features

- 📍 **State-wise Choropleth Maps** for UPI Amount and Count  
- 📈 **Time Series Analysis** across quarters and years  
- 🔁 **Multi-State Comparison** on Amount & Count  
- 🧭 **Dynamic Filtering** (Year, Quarter, Type)   
- 💡 **Built with Streamlit + Plotly** for full interactivity

---

## 🛠 Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io)
- **Charts**: [Plotly Express](https://plotly.com/python/plotly-express/)
- **Data Processing**: `pandas`
- **Deployment**: Streamlit Cloud
- **Data Source**: PhonePe Pulse GitHub [Repo](https://github.com/PhonePe/pulse)

---

## 🧑‍💻 How to Run Locally

### 🔧 Prerequisites

- Python 3.8+
- pip

### 📦 Install Dependencies

```bash
git clone https://github.com/imankurbhowmik/payGaze.git
cd payGaze
pip install -r requirements.txt
