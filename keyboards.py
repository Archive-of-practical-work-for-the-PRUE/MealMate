from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для команды /help
def help_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("/taste_settings")],
            [KeyboardButton("/choice")],
            [KeyboardButton("/favorites")]
        ],
        resize_keyboard=True
    )

# Клавиатура для настройки вкусовых предпочтений
def taste_settings_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Вкусовые предпочтения", callback_data="settings_taste")
            ],
            [
                InlineKeyboardButton("Диетические ограничения", callback_data="settings_diet")
            ],
            [
                InlineKeyboardButton("Настроение", callback_data="settings_mood")
            ],
            [
                InlineKeyboardButton("Готово", callback_data="settings_done")
            ]
        ]
    )

# Клавиатура для выбора вкусовых предпочтений
def taste_preferences_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Мясо", callback_data="taste_мясо"),
                InlineKeyboardButton("Рыба", callback_data="taste_рыба")
            ],
            [
                InlineKeyboardButton("Овощи", callback_data="taste_овощи"),
                InlineKeyboardButton("Фрукты", callback_data="taste_фрукты")
            ],
            [
                InlineKeyboardButton("Сладкое", callback_data="taste_сладкое"),
                InlineKeyboardButton("Острое", callback_data="taste_острое")
            ],
            [
                InlineKeyboardButton("Готово", callback_data="taste_done")
            ]
        ]
    )

# Клавиатура для выбора диетических ограничений
def diet_restrictions_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Вегетарианское", callback_data="diet_вегетарианское")
            ],
            [
                InlineKeyboardButton("Веганское", callback_data="diet_веганское")
            ],
            [
                InlineKeyboardButton("Без глютена", callback_data="diet_без глютена")
            ],
            [
                InlineKeyboardButton("Без лактозы", callback_data="diet_без лактозы")
            ],
            [
                InlineKeyboardButton("Без ограничений", callback_data="diet_без ограничений")
            ],
            [
                InlineKeyboardButton("Готово", callback_data="diet_done")
            ]
        ]
    )

# Клавиатура для выбора настроения
def mood_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Уютное", callback_data="mood_уютный")
            ],
            [
                InlineKeyboardButton("Праздничное", callback_data="mood_праздничный")
            ],
            [
                InlineKeyboardButton("Легкое", callback_data="mood_легкий")
            ],
            [
                InlineKeyboardButton("Сытное", callback_data="mood_сытный")
            ],
            [
                InlineKeyboardButton("Готово", callback_data="mood_done")
            ]
        ]
    )

# Клавиатура для действий с рекомендацией
def dish_action_keyboard(dish_id, recipe_url, order_url):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Рецепт", url=recipe_url),
                InlineKeyboardButton("Заказать", url=order_url)
            ],
            [
                InlineKeyboardButton("Запросить новый вариант", callback_data="new_choice")
            ],
            [
                InlineKeyboardButton("Сохранить в избранное", callback_data=f"favorite_{dish_id}")
            ]
        ]
    )