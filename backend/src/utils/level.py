from schemas.level import UserLevel

LEVELS = {
    "Новичок": 0,
    "Обыватель": 300,
    "Знаток города": 700,
    "Исследователь": 1500,
    "Мастер": 2500,
    "Эксперт": 4000,
    "Ревизор": 7000,
}


def get_user_level(points: int) -> UserLevel:
    current_level = None
    next_level = None
    for level, points_for_level in LEVELS.items():
        if points_for_level <= points:
            current_level = level
        elif points_for_level > points:
            next_level = level
            break
    user_level = UserLevel(
        current_level=current_level,
        min_xp=LEVELS[current_level],
        current_xp=points,
    )

    if next_level:
        user_level.next_level = next_level
        user_level.max_xp = LEVELS[next_level]
    return user_level
