import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# 🔹 Konfiguracja strony Streamlit
st.set_page_config(page_title="Analiza Recenzji Kawy", layout="wide")

# 🔹 Wczytanie danych
df = pd.read_csv("coffee_reviews_sentiment.csv", encoding="utf-8")
topics_df = pd.read_csv("coffee_topics.txt", delimiter=":", names=["Temat", "Słowa"])

# 🔹 Tytuł dashboardu
st.title("☕ Analiza Recenzji Kawy")

# 🔹 Filtracja recenzji po sentymencie
st.sidebar.header("📌 Filtruj recenzje")
sentyment_filter = st.sidebar.multiselect("Wybierz sentyment:", ["Pozytywny 😊", "Neutralny 😐", "Negatywny 😡"], default=["Pozytywny 😊", "Neutralny 😐", "Negatywny 😡"])

# 🔹 Filtrowanie danych
df_filtered = df[df["sentyment"].isin(sentyment_filter)]

# 🔹 Wykres sentymentu
st.subheader("📊 Rozkład sentymentu opinii")
sentyment_counts = df_filtered["sentyment"].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=sentyment_counts.index, y=sentyment_counts.values, palette="coolwarm", ax=ax)
plt.xlabel("Sentyment")
plt.ylabel("Liczba recenzji")
st.pyplot(fig)

# 🔹 Średnia ocena kawy
st.subheader("⭐ Średnia ocena kawy")
avg_rating = df_filtered["rating"].mean()
st.metric(label="Średnia ocena", value=round(avg_rating, 2))

# 🔹 Wykres zmian ocen w czasie
st.subheader("📈 Zmiany ocen kawy w czasie")
df_filtered["review_date"] = pd.to_datetime(df_filtered["review_date"])  # Konwersja daty
df_time_series = df_filtered.groupby("review_date")["rating"].mean().reset_index()

fig_time, ax_time = plt.subplots(figsize=(10, 5))
sns.lineplot(x="review_date", y="rating", data=df_time_series, marker="o", ax=ax_time)
plt.xlabel("Data recenzji")
plt.ylabel("Średnia ocena")
plt.xticks(rotation=45)
plt.title("📈 Średnia ocena kawy w czasie")

st.pyplot(fig_time)

# 🔹 Analiza długości recenzji
st.subheader("📏 Analiza długości recenzji")
df_filtered["review_length"] = df_filtered["desc_1"].astype(str).apply(lambda x: len(x.split()))

fig_hist, ax_hist = plt.subplots(figsize=(10, 5))
sns.histplot(df_filtered["review_length"], bins=30, kde=True, ax=ax_hist)
plt.xlabel("Liczba słów w recenzji")
plt.ylabel("Liczba recenzji")
plt.title("📏 Rozkład długości recenzji")

st.pyplot(fig_hist)


# 🔹 Chmura słów
st.subheader("🌥️ Chmura słów z recenzji")
all_words = " ".join(df_filtered["desc_1"].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="coolwarm").generate(all_words)

fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
ax_wc.imshow(wordcloud, interpolation="bilinear")
ax_wc.axis("off")
st.pyplot(fig_wc)

# 🔹 Najważniejsze tematy
st.subheader("📌 Najczęściej występujące tematy w recenzjach")
st.dataframe(topics_df)

# 🔹 Pobieranie danych
st.subheader("📥 Pobierz przetworzone dane")
st.download_button(label="📥 Pobierz jako CSV", data=df_filtered.to_csv(index=False), file_name="coffee_reviews_filtered.csv", mime="text/csv")
