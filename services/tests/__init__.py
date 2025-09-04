# يعرّف مجلد tests كموديول
from .tests_psych import score_test, psych_info
from .tests_personality import personality_test
from .recommend import recommend_based_on_psych, recommend_based_on_personality

__all__ = [
    "score_test",
    "psych_info",
    "personality_test",
    "recommend_based_on_psych",
    "recommend_based_on_personality",
]
