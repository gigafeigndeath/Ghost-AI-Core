from app.core.article_reader import read_article
from app.core.fact_extractor import extract_facts
from app.core.tone_engine import apply_tone
from app.core.media_planner import create_media_plan
from app.models.post import Post
from sqlalchemy.orm import Session


class Orchestrator:
    def __init__(self, llm, db: Session):
        self.llm = llm
        self.db = db

    def process_article(self, url: str, platforms: list[str]):
        content = read_article(url)
        facts = extract_facts(content, self.llm)
        toned_posts = {platform: apply_tone(facts, platform, self.llm) for platform in platforms}
        media_plan = create_media_plan(toned_posts)

        # Сохраняем в БД
        for post in media_plan:
            db_post = Post(content=post['content'], platform=post['platform'])
            self.db.add(db_post)
        self.db.commit()

        return media_plan