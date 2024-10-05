import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Keeping your existing CSS but adding styles for the sidebar calendar and menu
st.markdown("""
<style>
    /* Your existing styles here */
    
    /* New styles for sidebar */
    .sidebar-menu {
        padding: 20px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .menu-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .menu-item:hover {
        background-color: rgba(76, 175, 80, 0.2);
    }
    
    .calendar-widget {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Style for date input */
    .stDateInput>div>div {
        background-color: #1e2130;
        border: 1px solid #4CAF50;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("../dashboard/data_sewa_sepeda_clean.csv")
    return df

day_df = load_data()

# Calculate rental frequencies (move this outside of any specific analysis section)
rental_frequencies = day_df.groupby(['year', 'month']).agg({
    'total_rentals': 'sum',
}).reset_index()

rental_frequencies['month_year'] = rental_frequencies['month'].astype(str) + '-' + rental_frequencies['year'].astype(str)
rental_frequencies['date'] = pd.to_datetime(rental_frequencies[['year', 'month']].assign(day=1))
rental_frequencies = rental_frequencies.sort_values('date')

# Sidebar with Calendar and Menu
with st.sidebar:
    st.image("image/logo1.png")
    st.markdown("<h1 style='text-align: center;'> Bike Sharing</h1>", unsafe_allow_html=True)
    
    # Add calendar widget
    st.markdown("<div class='calendar-widget'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4CAF50;'>📅 Select Date Range</h3>", unsafe_allow_html=True)
    start_date = st.date_input("Start Date", datetime(2011, 1, 1))
    end_date = st.date_input("End Date", datetime(2012, 12, 31))
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add menu items
    st.markdown("<div class='sidebar-menu'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4CAF50;'>📊 Dashboard Menu</h3>", unsafe_allow_html=True)
    
    selected_menu = st.radio(
        "",
        ["Overview", "Weather Analysis", "Monthly Analysis", "Trend Analysis"],
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add filters
    st.markdown("<div class='sidebar-menu'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4CAF50;'>🔍 Filters</h3>", unsafe_allow_html=True)
    
    weather_filter = st.multiselect(
        "Weather Condition",
        options=[1, 2, 3, 4],
        default=[1, 2, 3, 4]
    )
    
    season_filter = st.multiselect(
        "Season",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Main content based on selected menu
if selected_menu == "Overview":
    st.markdown("<h2 style='color: #4CAF50;'>📈 Dashboard Overview</h2>", unsafe_allow_html=True)
    
    # Calculate key metrics
    total_rentals = day_df['total_rentals'].sum()
    avg_daily_rentals = day_df['total_rentals'].mean()
    max_rentals_day = day_df['total_rentals'].max()
    total_days = len(day_df)

    # Create metrics layout with 4 columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Style for metrics
    metric_style = """
    <div style="
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4CAF50;
        text-align: center;
    ">
        <h3 style="color: #4CAF50; font-size: 24px;">{value}</h3>
        <p style="color: #ffffff; font-size: 16px;">{label}</p>
    </div>
    """

    with col1:
        st.markdown(metric_style.format(
            value=f"{total_rentals:,.0f}",
            label="Total Rentals"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_style.format(
            value=f"{avg_daily_rentals:,.0f}",
            label="Average Daily Rentals"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_style.format(
            value=f"{max_rentals_day:,.0f}",
            label="Max Daily Rentals"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_style.format(
            value=f"{total_days:,.0f}",
            label="Total Days Analyzed"
        ), unsafe_allow_html=True)

    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Create two columns for charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<h3 style='color: #33fff0;'>🌡️ Rental Distribution by Temperature</h3>", unsafe_allow_html=True)
    
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        
        # Check the actual column name for temperature in your dataframe
        # It might be 'temp' instead of 'temperature'
        temp_column = 'temp' if 'temp' in day_df.columns else 'temperature'
        
        sns.scatterplot(data=day_df, x=temp_column, y='total_rentals', 
                    alpha=0.5, color='#01fae3')
        
        plt.title('Rental Distribution by Temperature', color='white')
        plt.xlabel('Temperature (°C)', color='white')
        plt.ylabel('Total Rentals', color='white')
        plt.tick_params(colors='white')
        plt.grid(True, alpha=0.2)
        st.pyplot(fig)

    with col_right:
        st.markdown("<h3 style='color: #33fff0;'>🗓️ Average Rentals by Day of Week</h3>", unsafe_allow_html=True)
        
        # Calculate average rentals by day of week
        weekday_avg = day_df.groupby('weekday')['total_rentals'].mean().reset_index()
        weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        weekday_avg['weekday_name'] = weekday_avg['weekday'].map(dict(enumerate(weekday_names)))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        
        sns.barplot(data=weekday_avg, x='weekday_name', y='total_rentals', 
                   color='#01fae3', ax=ax)
        
        plt.title('Average Rentals by Day of Week', color='white')
        plt.xlabel('Day of Week', color='white')
        plt.ylabel('Average Rentals', color='white')
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        st.pyplot(fig)

    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Add seasonal analysis
    st.markdown("<h3 style='color: #33fff0;'>🌺 Seasonal Rental Patterns</h3>", unsafe_allow_html=True)

    # Calculate seasonal metrics
    seasonal_avg = day_df.groupby('season')['total_rentals'].agg(['mean', 'max', 'min']).reset_index()
    season_names = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    seasonal_avg['season_name'] = seasonal_avg['season'].map(season_names)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    x = np.arange(len(seasonal_avg))
    width = 0.25

    ax.bar(x - width, seasonal_avg['mean'], width, label='Average', color='#01fae3')
    ax.bar(x, seasonal_avg['max'], width, label='Maximum', color='#ff6b6b')
    ax.bar(x + width, seasonal_avg['min'], width, label='Minimum', color='#4ecdc4')

    ax.set_xticks(x)
    ax.set_xticklabels(seasonal_avg['season_name'], color='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.title('Seasonal Rental Patterns', color='white')
    plt.xlabel('Season', color='white')
    plt.ylabel('Number of Rentals', color='white')
    plt.legend(facecolor='black', labelcolor='white')
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig)

    # Add explanation box
    st.markdown("""
    <div style='background-color: #1e2130; padding: 20px; border-radius: 10px; margin-top: 20px;'>
        <h4 style='color: #4CAF50;'>📊 Wawasan utama:</h4>
        <ul style='color: white;'>
            <li>Aktivitas penyewaan tertinggi terjadi selama bulan-bulan musim panas</li>
            <li>Pola akhir pekan menunjukkan penggunaan yang berbeda dibandingkan dengan hari kerja</li>
            <li>Suhu memiliki dampak yang signifikan terhadap jumlah penyewaan</li>
            <li>Waktu puncak penggunaan menunjukkan periode penyewaan yang populer</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif selected_menu == "Weather Analysis":
    st.markdown("<h2 style='color: #4CAF50;'>🌤️ Weather Analysis</h2>", unsafe_allow_html=True)
    df_weather_effect = day_df.groupby('weather_condition')['total_rentals'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.set_facecolor('gray')
    fig.patch.set_facecolor('gray')

    sns.barplot(data=df_weather_effect, x='weather_condition', y='total_rentals', color="#01fae3", ax=ax)
    plt.title('Rata-rata Jumlah Penyewaan Sepeda Berdasarkan Situasi Cuaca', color='white')
    plt.xlabel('Situasi Cuaca', color='white')
    plt.ylabel('Rata-rata Jumlah Penyewaan', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.tight_layout()
    st.pyplot(fig)

    with st.expander("Keterangan data"):
        st.markdown("""
        <div style='background-color: #1e2130; padding: 15px; border-radius: 5px;'>
        <p><strong style='color: #FF9800;'></strong>1: Cerah, Sedikit awan, Sebagian berawan, Sebagian berawan.</p>
        <p><strong style='color: #2196F3;'></strong> 2: Kabut + Mendung, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut.</p>
        <p><strong style='color: #4CAF50;'></strong> 3: Salju Ringan, Hujan Ringan + Badai Petir + Awan berserakan, Hujan Ringan + Awan berserakan.</p>
        <p><strong style='color: #4CAF50;'></strong> 4: Hujan Lebat + Rintik Es + Badai Petir + Kabut, Salju + Kabut.</p>
        </div>
        """, unsafe_allow_html=True)


elif selected_menu == "Monthly Analysis":
    st.markdown("<h2 style='color: #4CAF50;'>📅 Monthly Analysis</h2>", unsafe_allow_html=True)
    df_working_days = day_df.pivot_table(
    index=['year', 'month'],
    columns='workingday',
    values='instant',  # 'instant' adalah indeks unik untuk menghitung jumlah baris
    aggfunc='count'
    ).reset_index()

    # Mengganti nama kolom untuk lebih mudah dipahami
    df_working_days.columns = ['year', 'month', 'non_working_days', 'working_days']
    df_working_days['date'] = pd.to_datetime(df_working_days.apply(lambda x: f"{x['year']}-{x['month']}-01", axis=1))
    df_working_days = df_working_days.sort_values('date')  # Mengurutkan berdasarkan tanggal

    # Membuat format label bulan-tahun
    month_year_labels = df_working_days['date'].dt.strftime('%b-%Y')

    # Membuat plot
    fig, ax = plt.subplots(figsize=(18, 8))

    # Posisi x untuk batang
    x = np.arange(len(df_working_days))
    width = 0.35

    # Membuat batang
    rects1 = ax.bar(x - width/2, df_working_days['non_working_days'], width, 
                    label='Non Working Days', color='skyblue')
    rects2 = ax.bar(x + width/2, df_working_days['working_days'], width,
                    label='Working Days', color='lightgreen')

    # Kustomisasi grafik
    ax.set_ylabel('Total Rentals')
    ax.set_title('Working vs Non-Working Days by Month')
    ax.set_xticks(x)
    ax.set_xticklabels(month_year_labels, rotation=45)
    ax.legend()

    # Menambahkan grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Menambahkan nilai di atas batang
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    # Mengatur margin dan menampilkan plot
    plt.tight_layout()
    st.pyplot(fig)

elif selected_menu == "Trend Analysis":
    st.markdown("<h2 style='color: #4CAF50;'>📊 Trend Analysis</h2>", unsafe_allow_html=True)
    rental_frequencies = day_df.groupby(['year', 'month']).agg({
    'total_rentals': 'sum',
}).reset_index()

rental_frequencies['month_year'] = rental_frequencies['month'].astype(str) + '-' + rental_frequencies['year'].astype(str)
rental_frequencies['date'] = pd.to_datetime(rental_frequencies[['year', 'month']].assign(day=1))
rental_frequencies = rental_frequencies.sort_values('date')

fig, ax = plt.subplots(figsize=(12, 6))

# Set the plot background color to black
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Line plot with green color
sns.lineplot(x='month_year', y='total_rentals', data=rental_frequencies, marker='o', color='limegreen', linewidth=2.5, ax=ax)  # Green line


plt.title('Frekuensi Jumlah Total Rental Selama 2 Tahun Terakhir', color='white')
plt.xlabel('Bulan-Tahun', color='white')
plt.ylabel('Total Penyewaan', color='white')
plt.xticks(rotation=45, color='white')  # Rotated x-axis labels, white color
plt.yticks(color='white') # y-axis labels, white color
plt.grid(axis='y', color='gray', linestyle='--', alpha=0.7) # Improved grid
plt.tight_layout()
st.pyplot(fig)


# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Created by M.Arif Rahman Hakim | Bangkit 2024</p>", unsafe_allow_html=True)