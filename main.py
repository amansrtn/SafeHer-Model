from fastapi import FastAPI, Request
import logging
import pickle
import string
from textblob import TextBlob
from nltk.corpus import stopwords
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/analyze")
async def generate_quiz(request: Request):
    try:
        text = await request.json()
        result_text = text["text"]
        c = Predict_Dark_Pattern_Type(result_text)
        return str(c)
    except Exception as e:
        logging.info(e)


@app.get("/")
async def api_info():
    return "CodeSage"


def Predict_Dark_Pattern_Type(new_text):
    model = pickle.load(open(Path(__file__).parent.joinpath("model.pkl"), "rb"))

    tfidf_vectorizer = pickle.load(
        open(Path(__file__).parent.joinpath("tfidf_vectorizer.pkl"), "rb")
    )

    DarkPatternType = ["safe", "unsafe"]
    exclude = string.punctuation

    def rempun(text):
        return text.translate(str.maketrans("", "", exclude))

    def spellcorr(text):
        return TextBlob(text).correct().string

    def remstop(text):
        newtext = []
        for w in text.split():
            if w in stopwords.words("english"):
                newtext.append("")
            else:
                newtext.append(w)
        x = newtext[:]
        newtext.clear()
        return " ".join(x)

    new_text = new_text.lower()
    new_text = rempun(new_text)
    new_text = spellcorr(new_text)
    new_text = remstop(new_text)

    X_new_text_tfidf = tfidf_vectorizer.transform([new_text]).toarray()

    predicted_value = model.predict(X_new_text_tfidf)
    predicted_val = model.predict_proba(X_new_text_tfidf)
    return predicted_value[0]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=80)
