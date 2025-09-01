# -*- coding: utf-8 -*-
"""
Package initializer for modules
هذا الملف يجعل مجلد modules يُعامل كحزمة بايثون.
"""

from .tests_psych import PSYCH_TESTS, score_test as score_psych
from .tests_personality import PERS_TESTS, score_personality
from .recommend import recommend_tests_from_case
