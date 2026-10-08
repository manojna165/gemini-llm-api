"""
Prompt Engineering Examples

This file contains three prompts for the same use case:
1. Basic Zero-Shot
2. Improved Zero-Shot
3. Few-Shot
"""

# ---------------------------------------------------------
# SAMPLE INPUT
# ---------------------------------------------------------

REVIEW = """
I bought these wireless headphones last week. The sound quality is
excellent and the battery lasts a long time. However, the ear cushions
are uncomfortable after wearing them for more than an hour.
Overall, I am happy with the purchase.
"""


# ---------------------------------------------------------
# PROMPT 1 - BASIC ZERO-SHOT
# ---------------------------------------------------------

ZERO_SHOT_PROMPT = """
Analyze the sentiment of the following customer review.

Return the sentiment, confidence, and reason.

Customer Review:
{review}
"""


# ---------------------------------------------------------
# PROMPT 2 - IMPROVED ZERO-SHOT
# ---------------------------------------------------------

IMPROVED_ZERO_SHOT_PROMPT = """
You are a sentiment analysis system.

Analyze the customer review below.

Classify the overall sentiment into exactly one of these categories:
- positive
- negative
- neutral

Consider the overall opinion expressed by the customer rather than
focusing on only one sentence.

Also provide:
- confidence: a number between 0 and 1
- reason: a short explanation for the classification

Customer Review:
{review}
"""


# ---------------------------------------------------------
# PROMPT 3 - FEW-SHOT
# ---------------------------------------------------------

FEW_SHOT_PROMPT = """
You are a professional customer-review sentiment analyzer.

Classify the overall sentiment as:
- positive
- negative
- neutral

Use the following examples as guidance.

Example 1:
Review:
"The product is amazing. The quality is excellent and I absolutely
love using it every day."

Expected sentiment:
positive

Example 2:
Review:
"This product stopped working after two days. The quality is terrible
and I regret buying it."

Expected sentiment:
negative

Example 3:
Review:
"The product arrived on time. It works as expected, but there is
nothing particularly impressive about it."

Expected sentiment:
neutral

Now analyze the following customer review.

Customer Review:
{review}

Return:
- sentiment
- confidence between 0 and 1
- a short reason explaining your decision
"""