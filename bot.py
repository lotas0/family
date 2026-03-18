import telebot
from telebot import types
import json
import os
import random
from datetime import datetime

# ТВОИ ДАННЫЕ:
TOKEN = '8708696890:AAEs1e8ZUjKF18ADUAPvb2QFgRIeUj8EPLI'  # Создай нового через @BotFather
YOUR_ID = 1050084715  # Твой ID
HUSBAND_ID = 974307387  # ID мужа

# Разрешённые пользователи
ALLOWED_USERS = [YOUR_ID, HUSBAND_ID]

bot = telebot.TeleBot(TOKEN)

# Файлы для хранения данных
MENU_FILE = 'family_menu.json'
RECIPES_FILE = 'recipes_base.json'

# ========== БАЗА РЕЦЕПТОВ ==========
# Встроенная база адекватных рецептов (проверено для беременных!)
DEFAULT_RECIPES = {
    "курица": [
        "Куриные котлеты с пюре (нейтрально, вкусно, безопасно)",
        "Куриный суп с лапшой (лёгкий и сытный)",
        "Курица в духовке с картошкой (минимум усилий)",
        "Куриное филе в сметанном соусе (нежно и мягко)",
        "Плов с курицей (без острых специй)"
    ],
    "говядина": [
        "Бефстроганов с гречкой (классика)",
        "Суп с говядиной и овощами (полезно)",
        "Говяжьи тефтели в томатном соусе (с макаронами)",
        "Тушёная говядина с картошкой (в горшочке)",
        "Мясной рулет с яйцом (празднично)"
    ],
    "свинина": [
        "Свинина тушёная с овощами (нежирные куски)",
        "Мясо по-французски (с сыром, без майонеза)",
        "Свиные отбивные в духовке",
        "Жаркое с мясом и картошкой",
        "Ленивые голубцы (вкусно и быстро)"
    ],
    "рыба": [
        "Рыба в фольге с лимоном (минтай/треска)",
        "Рыбные котлеты (можно с картофельным пюре)",
        "Уха из красной рыбы (легко и сытно)",
        "Рыба запечённая с овощами",
        "Рыбный суп с пшеном"
    ],
    "картошка": [
        "Картофельная запеканка с мясом (сытно)",
        "Картошка тушёная с грибами",
        "Драники (оладьи из картофеля)",
        "Картофельное пюре с котлетой",
        "Картофель по-деревенски в духовке"
    ],
    "макароны": [
        "Макароны по-флотски (с фаршем)",
        "Паста с курицей и сливочным соусом",
        "Макаронная запеканка с сыром",
        "Лазанья (можно купить готовые листы)",
        "Спагетти с томатным соусом и фрикадельками"
    ],
    "рис": [
        "Рисовая каша с мясом (как в садике)",
        "Плов с курицей (без острых специй)",
        "Рис с овощами и кусочками курицы",
        "Фаршированные перцы (с рисом и мясом)",
        "Рисовая запеканка с фаршем"
    ],
    "гречка": [
        "Гречка по-купечески (с мясом)",
        "Гречневая каша с подливкой",
        "Гречка с грибами и луком",
        "Гречневые котлеты (с подливкой)",
        "Гречка с тушёнкой (быстрый вариант)"
    ],
    "яйца": [
        "Омлет с овощами (пышный, в духовке)",
        "Яичница с помидорами (глазунья)",
        "Запечённые яйца в авокадо (если есть)",
        "Яйца фаршированные (на ужин легко)",
        "Гренки с яйцом (на завтрак)"
    ],
    "овощи": [
        "Рагу овощное с мясом",
        "Суп-пюре из тыквы/кабачков",
        "Овощи запечённые с курицей",
        "Цветная капуста в кляре",
        "Кабачки, фаршированные мясом"
    ],
    "суп": [
        "Куриный суп с вермишелью",
        "Борщ (без острого, со сметаной)",
        "Щи из свежей капусты",
        "Сырный суп с курицей",
        "Гороховый суп (не слишком острый)",
        "Рассольник (без солёных огурцов в меру)"
    ],
    "быстро": [
        "Макароны с сосисками (если качественные)",
        "Яичница с помидорами и хлебом",
        "Быстрая пицца на готовом тесте",
        "Гренки с яйцом на завтрак",
        "Бутерброды горячие с сыром"
    ]
}

# ========== РАБОТА С ФАЙЛАМИ ==========

def load_menu():
    """Загружает список блюд семьи с твоим личным меню"""
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # ТВОЙ ЛИЧНЫЙ СПИСОК БЛЮД
    return {
        "мясные": [
            "Ленивые голубцы",
            "Котлеты мясные",
            "Голубцы",
            "Тефтели",
            "Гуляш",
            "Тушёная печень",
            "Болоньезе",
            "Беляши",
            "Чебуреки",
            "Мясной пирог",
            "Треугольники с мясом",
            "Крупа с сердечками",
            "Лагман"
        ],
        "супы": [
            "Куринный суп с вермишелью и овощами",
            "Борщ",
            "Рассольник",
            "Рыбный суп с рисом",
            "Куринный суп с пшеном",
            "Харчо",
            "Суп с фрикадельками",
            "Суп с клёцками",
            "Гречневый суп"
        ],
        "рыбные": [
            "Рыбка в духовке под шубой",
            "Котлеты рыбные с пюре",
            "Пирог с рыбой",
            "Макароны с морепродуктами",
            "Рыбный с рисом"
        ],
        "салаты": [
            "Салат Оливье",
            "Салат Крабовый",
            "Салат Свекла с чесноком"
        ],
        "выпечка/завтраки": [
            "Блины",
            "Панкейки",
            "Лепёшки с картошкой",
            "Творожная запеканка",
            "Ленивые вареники",
            "Сырники",
            "Пирог с капустой"
        ],
        "гарниры/основное": [
            "Картошка по-деревенски",
            "Картошка тушёная с овощами и тушёнкой",
            "Пюре с мясными котлетами",
            "Пюре с рыбными котлетами"
        ]
    }

def save_menu(menu_data):
    """Сохраняет список блюд"""
    with open(MENU_FILE, 'w', encoding='utf-8') as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=2)

def get_user_name(user_id):
    """Возвращает имя пользователя"""
    if user_id == YOUR_ID:
        return "хозяйка"
    elif user_id == HUSBAND_ID:
        return "муж"
    return "гость"

def is_allowed(user_id):
    """Проверка доступа"""
    return user_id in ALLOWED_USERS

# ========== КЛАВИАТУРЫ ==========

def get_main_keyboard():
    """Главное меню"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("🍽 Выбрать блюдо", callback_data="choose_dish")
    btn2 = types.InlineKeyboardButton("🤔 Что приготовить?", callback_data="generate")
    btn3 = types.InlineKeyboardButton("📋 Добавить блюдо", callback_data="add_dish")
    btn4 = types.InlineKeyboardButton("❓ Помощь", callback_data="help")
    
    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn4)
    
    return keyboard

def get_categories_keyboard():
    """Клавиатура с категориями блюд"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    categories = [
        ("🥩 Мясные", "cat_meat"),
        ("🥣 Супы", "cat_soup"),
        ("🐟 Рыбные", "cat_fish"),
        ("🥗 Салаты", "cat_salad"),
        ("🥞 Выпечка/Завтраки", "cat_breakfast"),
        ("🍲 Гарниры", "cat_main"),
        ("◀ Назад", "back_to_main")
    ]
    
    for name, callback in categories:
        keyboard.add(types.InlineKeyboardButton(name, callback_data=callback))
    
    return keyboard

def get_dishes_keyboard(category, dishes):
    """Клавиатура с блюдами из категории (по индексам)"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    for index, dish in enumerate(dishes):
        # Используем индекс вместо названия
        keyboard.add(types.InlineKeyboardButton(
            f"🍽 {dish}", 
            callback_data=f"dish_{category}_{index}"
        ))
    
    keyboard.add(types.InlineKeyboardButton("◀ Назад к категориям", callback_data="choose_dish"))
    
    return keyboard

# ========== ОСНОВНЫЕ ФУНКЦИИ ==========

@bot.message_handler(commands=['start'])
def start(message):
    """Обработка команды /start"""
    user_id = message.chat.id
    user_name = get_user_name(user_id)
    
    if not is_allowed(user_id):
        bot.reply_to(message, "😊 Этот бот только для нашей семьи!")
        return
    
    welcome_text = (
        f"👋 Привет, {user_name}!\n\n"
        "🍳 **Семейный Меню-Бот** поможет решить вечный вопрос «Что готовить?»\n\n"
        "**Что умею:**\n"
        "• Муж может выбрать блюдо — тебе придёт уведомление\n"
        "• По продуктам подберу рецепт (только нормальные сочетания)\n"
        "• Можно добавлять свои любимые блюда\n\n"
        "Выбирай в меню 👇"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Обработка нажатий на кнопки"""
    user_id = call.message.chat.id
    user_name = get_user_name(user_id)
    
    if not is_allowed(user_id):
        bot.answer_callback_query(call.id, "Нельзя 😊")
        return
    
    # ===== ГЛАВНОЕ МЕНЮ =====
    
    if call.data == "choose_dish":
        """Выбор блюда"""
        menu = load_menu()
        
        text = (
            "🍽 **Выбери категорию:**\n\n"
            "Потом просто нажми на блюдо, и хозяйке придёт уведомление!"
        )
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_categories_keyboard(),
            parse_mode="Markdown"
        )
    
    elif call.data == "generate":
        """Генерация блюда по продуктам"""
        text = (
            "🤔 **Что приготовить?**\n\n"
            "Напиши мне список продуктов через запятую, например:\n"
            "`курица, картошка, лук`\n\n"
            "Или просто название продукта:\n"
            "`курица`\n\n"
            "Также можно написать тип блюда:\n"
            "`суп`, `быстро`"
        )
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("◀ Назад", callback_data="back_to_main")
            ),
            parse_mode="Markdown"
        )
        
        # Устанавливаем состояние "ожидание продуктов"
        bot.register_next_step_handler(call.message, handle_ingredients)
    
    elif call.data == "add_dish":
        """Добавление нового блюда"""
        if user_id != YOUR_ID:
            bot.answer_callback_query(call.id, "Только хозяйка может добавлять блюда!")
            return
        
        text = (
            "📋 **Добавление нового блюда**\n\n"
            "Напиши блюдо и категорию через запятую, например:\n"
            "`Ленивые голубцы, мясные`\n\n"
            "Доступные категории:\n"
            "• мясные\n"
            "• супы\n"
            "• рыбные\n"
            "• салаты\n"
            "• выпечка/завтраки\n"
            "• гарниры/основное"
        )
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("◀ Назад", callback_data="back_to_main")
            ),
            parse_mode="Markdown"
        )
        
        bot.register_next_step_handler(call.message, handle_add_dish)
    
    elif call.data == "help":
        """Помощь"""
        help_text = (
            "❓ **Помощь**\n\n"
            "**Для хозяйки:**\n"
            "• Добавляй блюда в меню\n"
            "• Получаешь уведомления, когда муж выбрал\n\n"
            "**Для мужа:**\n"
            "• Заходи, выбирай блюдо\n"
            "• Жене приходит сообщение\n\n"
            "**Генератор рецептов:**\n"
            "• Пиши продукты — бот предложит блюда\n"
            "• Только адекватные сочетания (безопасно для беременных)\n\n"
            "**Команды:**\n"
            "/start — главное меню"
        )
        
        bot.edit_message_text(
            help_text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("◀ Назад", callback_data="back_to_main")
            ),
            parse_mode="Markdown"
        )
    
    elif call.data == "back_to_main":
        """Назад в главное меню"""
        bot.edit_message_text(
            "🍳 Главное меню",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_main_keyboard()
        )
    
    # ===== КАТЕГОРИИ =====
    
    elif call.data.startswith("cat_"):
        """Выбрана категория"""
        category_map = {
            "cat_meat": ("мясные", "🥩 Мясные блюда"),
            "cat_soup": ("супы", "🥣 Супы"),
            "cat_fish": ("рыбные", "🐟 Рыбные блюда"),
            "cat_salad": ("салаты", "🥗 Салаты"),
            "cat_breakfast": ("выпечка/завтраки", "🥞 Выпечка и завтраки"),
            "cat_main": ("гарниры/основное", "🍲 Гарниры и основное")
        }
        
        cat_key, cat_title = category_map.get(call.data, (None, None))
        if not cat_key:
            return
        
        menu = load_menu()
        dishes = menu.get(cat_key, [])
        
        if not dishes:
            bot.answer_callback_query(call.id, "В этой категории пока нет блюд")
            return
        
        text = f"{cat_title}\n\nВыбери блюдо:"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_dishes_keyboard(cat_key, dishes),
            parse_mode="Markdown"
        )
    
    # ===== ВЫБРАННОЕ БЛЮДО =====
    
    elif call.data.startswith("dish_"):
        """Выбрано конкретное блюдо (по индексу)"""
        try:
            # Разбираем callback_data: dish_категория_индекс
            parts = call.data.split("_")
            category = parts[1]
            dish_index = int(parts[2])
            
            # Загружаем меню и получаем блюдо по индексу
            menu = load_menu()
            category_dishes = menu.get(category, [])
            
            if 0 <= dish_index < len(category_dishes):
                dish_name = category_dishes[dish_index]
                
                # Уведомление хозяйке
                bot.send_message(
                    YOUR_ID,
                    f"👨 **Муж выбрал на завтра!**\n\n"
                    f"🍽 {dish_name}\n\n"
                    f"Категория: {category}\n"
                    f"Время: {datetime.now().strftime('%d.%m %H:%M')}",
                    parse_mode="Markdown"
                )
                
                # Подтверждение мужу
                bot.answer_callback_query(call.id, "✅ Отправлено! Жена получила уведомление")
                
                bot.edit_message_text(
                    f"✅ Отлично! Жене отправлено уведомление о выборе:\n\n**{dish_name}**",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton("◀ Назад в меню", callback_data="back_to_main")
                    ),
                    parse_mode="Markdown"
                )
            else:
                bot.answer_callback_query(call.id, "Ошибка: блюдо не найдено")
                
        except Exception as e:
            bot.answer_callback_query(call.id, "Ошибка, попробуй ещё раз")
            print(f"Ошибка в dish callback: {e}")
            
            # Подтверждение мужу
            bot.answer_callback_query(call.id, "✅ Отправлено! Жена получила уведомление")
            
            bot.edit_message_text(
                f"✅ Отлично! Жене отправлено уведомление о выборе:\n\n**{dish_name}**",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("◀ Назад в меню", callback_data="back_to_main")
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            bot.answer_callback_query(call.id, "Ошибка, попробуй ещё раз")
            print(f"Ошибка: {e}")
        
        # Подтверждение мужу
        bot.answer_callback_query(call.id, "✅ Отправлено! Жена получила уведомление")
        
        bot.edit_message_text(
            f"✅ Отлично! Жене отправлено уведомление о выборе:\n\n**{dish_name}**",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("◀ Назад в меню", callback_data="back_to_main")
            ),
            parse_mode="Markdown"
        )

# ========== ГЕНЕРАТОР РЕЦЕПТОВ ==========

def handle_ingredients(message):
    """Обработка списка продуктов"""
    user_input = message.text.lower().strip()
    
    # Разбираем продукты
    ingredients = [i.strip() for i in user_input.split(',') if i.strip()]
    
    if not ingredients:
        bot.reply_to(
            message,
            "😕 Напиши хотя бы один продукт!\n\nПопробуй ещё раз:",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("◀ Назад", callback_data="back_to_main")
            )
        )
        return
    
    # Ищем подходящие рецепты
    suggestions = []
    
    for ing in ingredients:
        # Проверяем каждый ингредиент
        for key in DEFAULT_RECIPES:
            if key in ing or ing in key:
                suggestions.extend(DEFAULT_RECIPES[key])
    
    # Проверяем, не искали ли суп
    if any("суп" in ing for ing in ingredients) or "суп" in user_input:
        suggestions.extend(DEFAULT_RECIPES.get("суп", []))
    
    # Проверяем, не нужно ли быстрое блюдо
    if any("быстро" in ing for ing in ingredients) or "быстро" in user_input:
        suggestions.extend(DEFAULT_RECIPES.get("быстро", []))
    
    # Убираем дубликаты
    suggestions = list(set(suggestions))
    
    if not suggestions:
        # Если ничего не нашли, даём универсальные советы
        suggestions = [
            "Мясо с картошкой в духовке (всё вместе — и готово!)",
            "Макароны с котлетой (купить готовые котлеты)",
            "Яичница с овощами (быстро и безопасно)",
            "Куриный суп с вермишелью (курица есть?)"
        ]
    
    # Берём 3 случайных рецепта
    selected = random.sample(suggestions, min(3, len(suggestions)))
    
    result = "🍳 **Что можно приготовить:**\n\n"
    for i, recipe in enumerate(selected, 1):
        result += f"{i}. {recipe}\n"
    
    result += f"\n(поиск по: {', '.join(ingredients)})"
    
    bot.send_message(
        message.chat.id,
        result,
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔄 Ещё варианты", callback_data="generate"),
            types.InlineKeyboardButton("◀ В меню", callback_data="back_to_main")
        ),
        parse_mode="Markdown"
    )

# ========== ДОБАВЛЕНИЕ БЛЮД ==========

def handle_add_dish(message):
    """Добавление нового блюда"""
    user_id = message.chat.id
    if user_id != YOUR_ID:
        return
    
    text = message.text.strip()
    
    try:
        if ',' not in text:
            raise ValueError("Нет запятой")
        
        dish_name, category = [x.strip() for x in text.split(',', 1)]
        category = category.lower()
        
        # Проверяем категорию
        category_map = {
            "мясные": "мясные",
            "мясо": "мясные",
            "супы": "супы",
            "суп": "супы",
            "рыбные": "рыбные",
            "рыба": "рыбные",
            "салаты": "салаты",
            "салат": "салаты",
            "выпечка/завтраки": "выпечка/завтраки",
            "выпечка": "выпечка/завтраки",
            "завтраки": "выпечка/завтраки",
            "гарниры/основное": "гарниры/основное",
            "гарниры": "гарниры/основное",
            "основное": "гарниры/основное"
        }
        
        cat_key = category_map.get(category)
        if not cat_key:
            bot.reply_to(
                message,
                f"❌ Неправильная категория. Доступны: мясные, супы, рыбные, салаты, выпечка/завтраки, гарниры/основное",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("◀ В меню", callback_data="back_to_main")
                )
            )
            return
        
        # Добавляем блюдо
        menu = load_menu()
        if dish_name not in menu[cat_key]:
            menu[cat_key].append(dish_name)
            save_menu(menu)
            bot.reply_to(
                message,
                f"✅ Блюдо **{dish_name}** добавлено в категорию {cat_key}!",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("◀ В меню", callback_data="back_to_main")
                ),
                parse_mode="Markdown"
            )
        else:
            bot.reply_to(
                message,
                f"⚠️ Блюдо **{dish_name}** уже есть в списке!",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("◀ В меню", callback_data="back_to_main")
                ),
                parse_mode="Markdown"
            )
            
    except Exception as e:
        bot.reply_to(
            message,
            "❌ Ошибка! Напиши в формате: `Название блюда, категория`\n"
            "Например: `Лазанья, мясные`",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("◀ Назад", callback_data="back_to_main")
            ),
            parse_mode="Markdown"
        )

# ========== ЗАПУСК ==========

if __name__ == "__main__":
    print("🍳 Семейный Меню-Бот запущен!")
    print(f"Хозяйка ID: {YOUR_ID}")
    print(f"Муж ID: {HUSBAND_ID}")
    print("\n📋 Твоё меню загружено:")
    menu = load_menu()
    for category, dishes in menu.items():
        print(f"  {category}: {len(dishes)} блюд")
    bot.infinity_polling()