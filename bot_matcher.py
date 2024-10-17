import discord # type: ignore
from discord import app_commands # type: ignore
from discord.ext import commands # type: ignore
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Налаштування інтенцій бота і префікс команд
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Словник для зберігання профілів користувачів
user_profiles = {}

@bot.event
async def on_ready():
    try:
        # Синхронізація команд глобально
        await bot.tree.sync()  # Синхронізувати команди глобально для оновлення
        print(f'Бот готовий. Увійшов як {bot.user}')
        print('Команди успішно синхронізовані!')
    except Exception as e:
        print(f'Не вдалося синхронізувати команди: {e}')

# Допоміжна функція для отримання або створення профілю користувача
def get_or_create_profile(user_id):
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            'personality_type': 'N/A',
            'hobbies': [],
            'communication_styles': []
        }
    return user_profiles[user_id]

# Допоміжна функція для надання опису MBTI
def get_mbti_description(mbti_type):
    descriptions = {
        'ENTJ': 'Командир: Лідери, що бачать загальну картину та ефективно організовують ресурси.',
        'ENTP': 'Дебатер: Інтелектуали, що люблять виклики і шукають нові ідеї.',
        'ENFJ': 'Протагоніст: Харизматичні лідери, що прагнуть надихати інших.',
        'ENFP': 'Кампанейнер: Творчі оптимісти, завжди готові до нових ідей.',
        'ESTJ': 'Виконавчий: Рішучі адміністратори, орієнтовані на ефективність.',
        'ESTP': 'Підприємець: Енергійні люди, завжди готові до дій.',
        'ESFJ': 'Консул: Дружелюбні люди, що створюють гармонійне середовище.',
        'ESFP': 'Артист: Спонтанні оптимісти, що приносять радість.',
        'INFJ': 'Адвокат: Ідеалісти, що розуміють почуття і допомагають іншим.',
        'INFP': 'Медіатор: Альтруїсти, що керуються цінностями та прагнуть гармонії.',
        'INTJ': 'Архітектор: Стратегічні мислителі, зосереджені на планах і інноваціях.',
        'INTP': 'Мислитель: Аналітики, що люблять знання та творчі ідеї.',
        'ISFJ': 'Захисник: Турботливі люди, що прагнуть захистити близьких.',
        'ISFP': 'Авантюрист: Гнучкі митці, що цінують свободу вираження.',
        'ISTJ': 'Логіст: Практичні реалісти, надійні та вірні правилам.',
        'ISTP': 'Віртуоз: Сміливі експериментатори, здатні вирішувати проблеми.'
    }
    return descriptions.get(mbti_type, 'N/A')

# Команда для встановлення типу особистості з описом
@bot.tree.command(name="setpersonality", description="Встановіть свій тип особистості.")
async def setpersonality(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Будь ласка, оберіть свій тип особистості:",
        view=PersonalityTypeView(),
        ephemeral=True
    )

class PersonalityTypeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        options = [
            discord.SelectOption(label=ptype, description=get_mbti_description(ptype)) for ptype in [
                'INTJ', 'INTP', 'ENTJ', 'ENTP',
                'INFJ', 'INFP', 'ENFJ', 'ENFP',
                'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
                'ISTP', 'ISFP', 'ESTP', 'ESFP'
            ]
        ]
        self.add_item(PersonalityTypeSelect(options=options))

class PersonalityTypeSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Оберіть свій MBTI тип особистості", options=options)

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(interaction.user.id)
        profile['personality_type'] = self.values[0]
        description = get_mbti_description(self.values[0])
        await interaction.response.send_message(f"Тип особистості встановлено: {self.values[0]}: {description}.", ephemeral=True)

# Команда для встановлення хобі
@bot.tree.command(name="sethobbies", description="Встановіть свої хобі.")
async def sethobbies(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Будь ласка, оберіть категорію хобі:",
        view=HobbyCategoryView(),
        ephemeral=True
    )

class HobbyCategoryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        categories = [
            "Творчість і медіа",
            "Активний відпочинок і спорт",
            "Технології та ігри",
            "Розвиток і самовдосконалення",
            "Домашнє дозвілля",
            "Подорожі та дослідження"
        ]
        for category in categories:
            self.add_item(HobbyCategoryButton(label=category, category=category))

class HobbyCategoryButton(discord.ui.Button):
    def __init__(self, label, category):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.category = category

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Ви обрали категорію: {self.category}. Виберіть хобі:",
            view=HobbySelectView(self.category),
            ephemeral=True
        )

class HobbySelectView(discord.ui.View):
    def __init__(self, category):
        super().__init__()
        options = self.get_hobby_options(category)
        self.add_item(HobbySelect(options=options))

    @staticmethod
    def get_hobby_options(category):
        hobbies = {
            "Творчість і медіа": [
                discord.SelectOption(label='Малювання'),
                discord.SelectOption(label='Фотографія'),
                discord.SelectOption(label='Музика (гра на інструментах)'),
                discord.SelectOption(label='Танці'),
                discord.SelectOption(label='Писання (блоги, поезія, проза)'),
                discord.SelectOption(label='Відеомонтаж'),
                discord.SelectOption(label='Графічний дизайн')
            ],
            "Активний відпочинок і спорт": [
                discord.SelectOption(label='Біг'),
                discord.SelectOption(label='Йога'),
                discord.SelectOption(label='Фітнес'),
                discord.SelectOption(label='Футбол'),
                discord.SelectOption(label='Кемпінг та походи'),
                discord.SelectOption(label='Екстримальні види спорту (скелелазіння)')
            ],
            "Технології та ігри": [
                discord.SelectOption(label='Ігрові відеоігри'),
                discord.SelectOption(label='Кодинг/програмування'),
                discord.SelectOption(label='Кіберспорт'),
                discord.SelectOption(label='Моделювання ігор')
            ],
            "Розвиток і самовдосконалення": [
                discord.SelectOption(label='Читання книг'),
                discord.SelectOption(label='Медитація'),
                discord.SelectOption(label='Психологія'),
                discord.SelectOption(label='Астрологія')
            ],
            "Домашнє дозвілля": [
                discord.SelectOption(label='Кулінарія'),
                discord.SelectOption(label='Садівництво'),
                discord.SelectOption(label='DIY проекти – створення речей своїми руками (меблі, декор, одяг)'),
                discord.SelectOption(label='Колекціонування (марки, монети)')
            ],
            "Подорожі та дослідження": [
                discord.SelectOption(label='Подорожі'),
                discord.SelectOption(label='Астрономія'),
                discord.SelectOption(label='Історичні реконструкції'),
                discord.SelectOption(label='Робота з тваринами')
            ]
        }
        return hobbies.get(category, [])

class HobbySelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder='Оберіть свої хобі', options=options, min_values=1, max_values=len(options))

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(interaction.user.id)
        profile['hobbies'].extend(self.values)
        await interaction.response.send_message(f"Хобі оновлено: {', '.join(self.values)}", ephemeral=True)

# Команда для встановлення стилів спілкування
@bot.tree.command(name="setcommunicationstyle", description="Встановіть свої стилі спілкування.")
async def setcommunicationstyle(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Будь ласка, оберіть свої стилі спілкування (можна обрати кілька варіантів):",
        view=CommunicationStyleView(),
        ephemeral=True
    )

class CommunicationStyleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CommunicationStyleSelect())

class CommunicationStyleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Розмови один на один"),
            discord.SelectOption(label="Малі групові обговорення"),
            discord.SelectOption(label="Великі групові зустрічі"),
            discord.SelectOption(label="Слухання та спостереження"),
            discord.SelectOption(label="Дебати та дискусії"),
            discord.SelectOption(label="Наставництво / Керівництво"),
            discord.SelectOption(label="Емпатичні розмови"),
            discord.SelectOption(label="Гумор та легкі розмови"),
            discord.SelectOption(label="Розповідання історій"),
            discord.SelectOption(label="Глибокі, роздумисті розмови"),
            discord.SelectOption(label="Вирішення конфліктів")
        ]
        super().__init__(
            placeholder="Оберіть свої стилі спілкування", options=options, min_values=1, max_values=len(options)
        )

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(interaction.user.id)
        profile['communication_styles'] = ', '.join(self.values)
        await interaction.response.send_message(f"Стилі спілкування встановлено: {', '.join(self.values)}", ephemeral=True)

# Команда для перегляду профілю користувача
@bot.tree.command(name="myprofile", description="Переглянути свій профіль.")
async def myprofile(interaction: discord.Interaction):
    try:
        profile = get_or_create_profile(interaction.user.id)
        await interaction.response.send_message(
            f"**Тип особистості**: {profile['personality_type']} ({get_mbti_description(profile['personality_type'])})\n"
            f"**Хобі**: {', '.join(profile['hobbies']) if profile['hobbies'] else 'N/A'}\n"
            f"**Стилі спілкування**: {profile['communication_styles'] if profile['communication_styles'] else 'N/A'}"
        )
    except Exception as e:
        await interaction.response.send_message(f"Сталася помилка: {e}", ephemeral=True)

# Команда для перевірки профілю іншого користувача
@bot.tree.command(name="checkprofile", description="Переглянути профіль іншого користувача.")
@app_commands.describe(user="Користувач, чий профіль ви хочете переглянути")
async def checkprofile(interaction: discord.Interaction, user: discord.Member):
    try:
        profile = get_or_create_profile(user.id)
        await interaction.response.send_message(
            f"**Тип особистості**: {profile['personality_type']} ({get_mbti_description(profile['personality_type'])})\n"
            f"**Хобі**: {', '.join(profile['hobbies']) if profile['hobbies'] else 'N/A'}\n"
            f"**Стилі спілкування**: {profile['communication_styles'] if profile['communication_styles'] else 'N/A'}"
        )
    except Exception as e:
        await interaction.response.send_message(f"Сталася помилка: {e}", ephemeral=True)

bot.run(TOKEN)