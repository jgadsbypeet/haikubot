import os
import time
import openai
import praw

client = openai.OpenAI(api_key="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")

reddit = praw.Reddit(
    client_id="wxz9EZjLHG2Lyd22ptO_GA",
    client_secret="Ob60ECuVvndAt8uPNqKQrQfzUL3pWA",
    username="Suitable-Towel-8421",
    password="FHZ9xzb!tpu4yxr7fjd",
    user_agent="haiku bot by u/Suitable-Towel-8421"
)

def generate_haiku(text):
    prompt = (
        "Write a haiku (5-7-5) in response to this Reddit post. "
        "Reflect progressive values like empathy, equality, inclusion, social justice, or environmental care—whichever fits best. "
        "Be poetic, not preachy:\n\n"
        f"{text}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
subreddit = reddit.subreddit("test")          # change later

for submission in subreddit.stream.submissions():
    try:
        if submission.saved:
            continue                           # already handled

        text  = f"{submission.title}\n\n{submission.selftext}"
        haiku = generate_haiku(text)

        # 1⃣  show it in your terminal
        print("\n----------")
        print(f"POST: {submission.title}")
        print("HAIKU:\n" + haiku)
        print("----------")

        # 2⃣  publish to Reddit
        reply = submission.reply(haiku)

        # 3⃣  confirm the URL in terminal
        print("Posted →", reply.permalink)

        submission.save()                      # mark as done
        time.sleep(10)                         # be polite to Reddit
    except Exception as e:
        print("❌", e)
        time.sleep(30)