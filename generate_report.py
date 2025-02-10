import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# 🔹 Rejestracja czcionki obsługującej polskie znaki
pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

# 🔹 Wczytanie danych
df = pd.read_csv("coffee_reviews_sentiment.csv", encoding="utf-8")

# 🔹 Statystyki ogólne
total_reviews = len(df)
avg_rating = round(df["rating"].mean(), 2)
sentyment_counts = df["sentyment"].value_counts()

# 🔹 Tworzenie pliku PDF
pdf_filename = "coffee_reviews_report.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)
c.setFont("DejaVu", 16)  # Użycie czcionki z polskimi znakami
c.drawString(100, 770, "📄 Raport końcowy: Analiza Recenzji Kawy")

# 🔹 Podstawowe statystyki
c.setFont("DejaVu", 12)
c.drawString(100, 750, f"📌 Liczba recenzji: {total_reviews}")
c.drawString(100, 730, f"⭐ Średnia ocena: {avg_rating}")

# 🔹 Wykres sentymentu
fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(x=sentyment_counts.index, y=sentyment_counts.values, palette="coolwarm", ax=ax)
plt.xlabel("Sentyment")
plt.ylabel("Liczba recenzji")
plt.title("📊 Rozkład sentymentu")
fig.savefig("sentyment_chart.png")
c.drawImage("sentyment_chart.png", 100, 500, width=400, height=200)

# 🔹 Wykres zmian ocen w czasie
df["review_date"] = pd.to_datetime(df["review_date"])
df_time_series = df.groupby("review_date")["rating"].mean().reset_index()
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(x="review_date", y="rating", data=df_time_series, marker="o", ax=ax)
plt.xlabel("Data recenzji")
plt.ylabel("Średnia ocena")
plt.title("📈 Zmiany ocen kawy w czasie")
fig.savefig("rating_over_time.png")
c.drawImage("rating_over_time.png", 100, 250, width=400, height=200)

# 🔹 Chmura słów
all_words = " ".join(df["desc_1"].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="coolwarm").generate(all_words)
fig, ax = plt.subplots(figsize=(5, 3))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
plt.title("🌥️ Chmura słów z recenzji")
fig.savefig("wordcloud.png")
c.drawImage("wordcloud.png", 100, 20, width=400, height=200)

# 🔹 Zamknięcie PDF
c.showPage()
c.save()

print(f"✅ Raport został zapisany jako {pdf_filename}")

