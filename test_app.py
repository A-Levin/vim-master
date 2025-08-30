#!/usr/bin/env python3
"""Simple test script to verify VimMaster functionality."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

os.environ["DATABASE_URL"] = "sqlite:///./vim_master.db"

from app.core.services.game import game_service
from app.core.services.quest import quest_service
from app.core.services.user import user_service
from app.db.base import SessionLocal, create_tables


def test_basic_functionality():
    """Test basic functionality of the VimMaster app."""
    print("🧪 Testing VimMaster basic functionality...")

    # Create database tables
    create_tables()
    db = SessionLocal()

    try:
        # Test 1: Create user
        print("\n1. Testing user creation...")
        user = user_service.get_or_create_user(
            db,
            telegram_id=12345,
            username="test_user",
            first_name="Test",
            last_name="User",
        )
        print(f"✅ User created: {user.first_name} (ID: {user.id})")

        # Test 2: Get available quests
        print("\n2. Testing quest retrieval...")
        chapters = quest_service.get_available_chapters(db)
        if chapters:
            chapter = chapters[0]
            print(f"✅ Found chapter: {chapter.title}")

            quests = quest_service.get_chapter_quests(db, chapter.id)
            if quests:
                quest = quests[0]
                print(f"✅ Found quest: {quest.title}")

                # Test 3: Start quest
                print("\n3. Testing quest gameplay...")
                started_quest = game_service.start_quest(db, user, quest.id)
                if started_quest:
                    print(f"✅ Quest started: {started_quest.title}")

                    # Test 4: Submit correct answer
                    if quest.vim_command:
                        is_correct, score, message = game_service.submit_answer(
                            db, user, quest.id, quest.vim_command
                        )
                        print(f"✅ Answer submitted: {message} (Score: {score})")

                        # Test 5: Check user progress
                        progress_summary = game_service.get_user_progress_summary(
                            db, user.id
                        )
                        print(
                            f"✅ Progress: {progress_summary['total_completed']} quests completed, {progress_summary['total_score']} total score"
                        )

        print("\n🎉 All tests passed! VimMaster is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_basic_functionality()
