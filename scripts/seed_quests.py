import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


os.environ["DATABASE_URL"] = "sqlite:///./vim_master.db"

from app.db.base import SessionLocal, create_tables
from app.db.models import Chapter, DifficultyLevel, Quest, QuestType


def create_mvp_quests():
    create_tables()
    db = SessionLocal()

    try:
        chapter = Chapter(
            title="Vim Basics",
            description="Learn the fundamental Vim commands",
            difficulty=DifficultyLevel.BEGINNER,
            order_index=1,
            unlock_score=0,
        )
        db.add(chapter)
        db.commit()
        db.refresh(chapter)

        quests_data = [
            {
                "title": "The Dot Command",
                "description": "Learn to use the powerful dot (.) command to repeat your last action. You have the text 'hello' and need to add '!' after each character.",
                "quest_type": QuestType.COMMAND,
                "difficulty": DifficultyLevel.BEGINNER,
                "order_index": 1,
                "initial_text": "hello",
                "expected_result": "h!e!l!l!o!",
                "vim_command": "A!<Esc>",
                "hints": [
                    "Use A to append at the end of the line",
                    "Press Escape to return to normal mode",
                    "Use . (dot) to repeat the last action",
                ],
                "max_score": 10,
                "time_limit": 60,
            },
            {
                "title": "Basic Motions",
                "description": "Master word movements with w, b, and e. Navigate through the text using these motion commands.",
                "quest_type": QuestType.MOTION,
                "difficulty": DifficultyLevel.BEGINNER,
                "order_index": 2,
                "initial_text": "vim is a powerful text editor",
                "expected_result": "VIM IS A POWERFUL TEXT EDITOR",
                "vim_command": "gUU",
                "hints": [
                    "w moves forward by word",
                    "b moves backward by word",
                    "e moves to end of word",
                    "gU converts to uppercase",
                ],
                "max_score": 15,
                "time_limit": 90,
            },
            {
                "title": "Insert Mode Mastery",
                "description": "Practice different ways to enter insert mode: A (append at end), I (insert at beginning), o (new line below).",
                "quest_type": QuestType.EDITING,
                "difficulty": DifficultyLevel.BEGINNER,
                "order_index": 3,
                "initial_text": "line one\nline three",
                "expected_result": "line one\nline two\nline three",
                "vim_command": "o",
                "hints": [
                    "A appends at the end of the line",
                    "I inserts at the beginning of the line",
                    "o creates a new line below and enters insert mode",
                ],
                "max_score": 12,
                "time_limit": 60,
            },
            {
                "title": "Visual Selection",
                "description": "Use visual mode to select text and perform operations. Select a word and make it uppercase.",
                "quest_type": QuestType.VISUAL,
                "difficulty": DifficultyLevel.BEGINNER,
                "order_index": 4,
                "initial_text": "make this WORD uppercase",
                "expected_result": "make this WORD UPPERCASE",
                "vim_command": "viwgU",
                "hints": [
                    "v enters visual mode",
                    "iw selects inner word",
                    "gU converts selection to uppercase",
                ],
                "max_score": 18,
                "time_limit": 90,
            },
            {
                "title": "Search and Replace",
                "description": "Use the substitute command to replace all occurrences of 'old' with 'new' in the text.",
                "quest_type": QuestType.SEARCH,
                "difficulty": DifficultyLevel.BEGINNER,
                "order_index": 5,
                "initial_text": "old text with old words and old patterns",
                "expected_result": "new text with new words and new patterns",
                "vim_command": ":%s/old/new/g",
                "hints": [
                    ":s is the substitute command",
                    "% means apply to all lines",
                    "g means global (all occurrences on each line)",
                ],
                "max_score": 20,
                "time_limit": 120,
            },
        ]

        for quest_data in quests_data:
            quest = Quest(chapter_id=chapter.id, **quest_data)
            db.add(quest)

        db.commit()
        print("✅ Successfully created MVP quests!")

        created_quests = db.query(Quest).filter(Quest.chapter_id == chapter.id).all()
        print(f"Created {len(created_quests)} quests in chapter '{chapter.title}':")
        for quest in created_quests:
            print(f"  - {quest.order_index}. {quest.title}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating quests: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_mvp_quests()
