# Course data

| File | What it is | Used in |
|---|---|---|
| `womens_clothing_ecommerce_reviews.csv` | 23,486 customer reviews of women's clothing from an online retailer: age, title, review text, 1-5 rating, recommended flag, helpful-vote count, division/department/class. | Labs 12-16 |
| `reviews_sample.txt` | 600 reviews sampled from the CSV (`random_state=42`, reviews with text only), one per line as `rating<TAB>text`, internal line breaks replaced by spaces. | Labs 08, 09, 11 |

**Source:** "Women's E-Commerce Clothing Reviews", published on Kaggle by Nick Brooks (nicapotato), https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews. Listed there as CC0: Public Domain. The reviews are real and anonymised; the retailer's name was replaced by "retailer" in the text.

Known quirks the labs rely on (do not "fix" the raw file): an unnamed index column, the `Initmates` typo in `Division Name`, missing titles/texts, 7 duplicated review texts, `\r\n` inside some reviews, and a ~500-character limit on review length.

To regenerate the sample:

```python
import re, pandas as pd
df = pd.read_csv("data/womens_clothing_ecommerce_reviews.csv", index_col=0)
s = df.dropna(subset=["Review Text"]).sample(600, random_state=42)
with open("data/reviews_sample.txt", "w", encoding="utf-8") as f:
    for r, t in zip(s["Rating"], s["Review Text"]):
        f.write(f"{r}\t{re.sub(r'\s*[\r\n]+\s*', ' ', t).strip()}\n")
```
