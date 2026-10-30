from flask import Flask, render_template, request

app = Flask(__name__)

ITEMS = [{'name': 'Laptop', 'category': 'Electronics', 'price': 55000, 'score': 96, 'emoji': '💻'}, {'name': 'Wireless Mouse', 'category': 'Electronics', 'price': 899, 'score': 88, 'emoji': '🖱️'}, {'name': 'Smartphone', 'category': 'Electronics', 'price': 22000, 'score': 93, 'emoji': '📱'}, {'name': 'Running Shoes', 'category': 'Fashion', 'price': 2499, 'score': 91, 'emoji': '👟'}, {'name': 'Backpack', 'category': 'Fashion', 'price': 1299, 'score': 84, 'emoji': '🎒'}, {'name': 'Coffee Maker', 'category': 'Home', 'price': 3499, 'score': 86, 'emoji': '☕'}, {'name': 'Desk Lamp', 'category': 'Home', 'price': 799, 'score': 80, 'emoji': '💡'}]

@app.route("/")
def home():
    results = ITEMS.copy()
    selected = ""
    feature = "filter"

    if feature == "filter":
        categories = ["All", "Electronics", "Fashion", "Home"]
        selected = request.args.get("category", "All")
        if selected not in categories:
            selected = "All"
        if selected != "All":
            results = [item for item in results if item["category"] == selected]
    elif feature == "sort":
        selected = request.args.get("sort", "score")
        if selected == "name":
            results.sort(key=lambda item: item["name"].lower())
        elif selected == "price_low":
            results.sort(key=lambda item: item["price"])
        elif selected == "price_high":
            results.sort(key=lambda item: item["price"], reverse=True)
        else:
            selected = "score"
            results.sort(key=lambda item: item["score"], reverse=True)

    return render_template("index.html", title="Recommendation System V2",
        subtitle="Filter – Apply Condition", version="V2", feature=feature,
        items=results, categories=["All", "Electronics", "Fashion", "Home"], selected=selected)

@app.get("/health")
def health():
    return {"status": "ok", "version": "v2"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
