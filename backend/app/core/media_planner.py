import datetime

def create_media_plan(toned_posts: dict):
    plan = []
    now = datetime.datetime.now()
    timings = {
        0: "now",
        1: now + datetime.timedelta(hours=3),
        2: now + datetime.timedelta(days=1)
    }
    for i, (platform, content) in enumerate(toned_posts.items()):
        plan.append({
            "platform": platform,
            "content": content + " Source: [original link]",
            "time": timings.get(i % len(timings), "now")
        })
    return plan