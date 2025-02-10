import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import seaborn as sns
from wordcloud import WordCloud

# 🔹 Wczytanie przetworzonych danych
df = pd.read_csv("coffee_reviews_sentiment.csv", encoding="utf-8")

# 🔹 Model TF-IDF (przetwarzanie tekstu)
vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)  # Maksymalnie 1000 słów kluczowych
tfidf_matrix = vectorizer.fit_transform(df["desc_1"].astype(str))

# 🔹 Model LDA (wykrywanie tematów)
lda = LatentDirichletAllocation(n_components=5, random_state=42)  # 5 tematów
lda.fit(tfidf_matrix)

# 🔹 Pobranie słów kluczowych dla każdego tematu
terms = vectorizer.get_feature_names_out()
topics = {}

for topic_idx, topic in enumerate(lda.components_):
    top_words = [terms[i] for i in topic.argsort()[:-11:-1]]  # TOP 10 słów dla każdego tematu
    topics[f"Temat {topic_idx+1}"] = top_words

# 🔹 Wyświetlenie tematów
print("\n📌 Kluczowe tematy w recenzjach:")
for temat, slowa in topics.items():
    print(f"{temat}: {', '.join(slowa)}")

# 🔹 Zapisanie tematów do pliku
with open("coffee_topics.txt", "w", encoding="utf-8") as f:
    for temat, slowa in topics.items():
        f.write(f"{temat}: {', '.join(slowa)}\n")

print("\n✅ Analiza tematów zakończona! Wyniki zapisane w coffee_topics.txt.")



# 🔹 Połączenie wszystkich słów kluczowych w jeden tekst
all_words = " ".join(sum(topics.values(), []))

# 🔹 Tworzenie chmury słów
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="coolwarm").generate(all_words)

# 🔹 Rysowanie chmury słów
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")  # Usunięcie osi dla lepszej czytelności
plt.title("☕ Chmura słów z recenzji kawy", fontsize=16)

plt.show()
