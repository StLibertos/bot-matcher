import discord  # type: ignore
from discord import app_commands  # type: ignore
from discord.ext import commands  # type: ignore
import os
import asyncio

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

# Команда для перегляду інформації про бота
@bot.tree.command(name="info_personality_bot", description="Переглянути опис можливостей бота.")
async def info_personality_bot(interaction: discord.Interaction):
    info_message = (
        "**🤖 Ось що я вмію:**\n\n"
        "1. **/setpersonality** — Встановити свій тип особистості.\n"
        "   - _Опис_: Ви можете обрати свій MBTI тип особистості. Якщо ви не знаєте свого типу, ви можете пройти [тест на 16 типів особистості](https://www.16personalities.com/uk).\n"
        "   - **Приклад**: `/setpersonality`\n\n"
        "2. **/sethobbies** — Встановити свої хобі.\n"
        "   - _Опис_: Оберіть свої улюблені види дозвілля та захоплення.\n"
        "   - **Приклад**: `/sethobbies`\n\n"
        "3. **/setcommunicationstyle** — Встановити свої стилі спілкування.\n"
        "   - _Опис_: Оберіть свої стилі спілкування.\n"
        "   - **Приклад**: `/setcommunicationstyle`\n\n"
        "4. **/myprofile** — Переглянути свій профіль.\n"
        "   - _Опис_: Показує ваш поточний профіль, включаючи тип особистості, хобі та стилі спілкування.\n"
        "   - **Приклад**: `/myprofile`\n\n"
        "5. **/checkprofile** — Переглянути профіль іншого користувача.\n"
        "   - _Опис_: Можливість перевірити профіль іншого користувача.\n"
        "   - **Приклад**: `/checkprofile @username`\n\n"
        "6. **/deleteprofile** — Видалити свій профіль.\n"
        "   - _Опис_: Видаляє ваш профіль з усіма даними.\n"
        "   - **Приклад**: `/deleteprofile`"
    )

    await interaction.response.send_message(info_message, ephemeral=True)

# Команда для перегляду профілю користувача
@bot.tree.command(name="myprofile", description="Переглянути свій профіль.")
async def myprofile(interaction: discord.Interaction):
    try:
        profile = get_or_create_profile(interaction.user.id)
        await interaction.response.send_message(
            f"🔖 **Тип особистості**: {profile['personality_type']} ({get_mbti_description(profile['personality_type'])})\n\n"
            f"🌱 **Хобі**: {', '.join(profile['hobbies']) if profile['hobbies'] else 'N/A'}\n\n"
            f"💬 **Стилі спілкування**: {', '.join(profile['communication_styles']) if profile['communication_styles'] else 'N/A'}",
            ephemeral=True
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
            f"🔖 **Тип особистості**: {profile['personality_type']} ({get_mbti_description(profile['personality_type'])})\n\n"
            f"🌱 **Хобі**: {', '.join(profile['hobbies']) if profile['hobbies'] else 'N/A'}\n\n"
            f"💬 **Стилі спілкування**: {', '.join(profile['communication_styles']) if profile['communication_styles'] else 'N/A'}",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(f"Сталася помилка: {e}", ephemeral=True)

# Команда для встановлення типу особистості з можливістю видалення
@bot.tree.command(name="setpersonality", description="Встановіть або змініть свій тип особистості.")
async def setpersonality(interaction: discord.Interaction):
    profile = get_or_create_profile(interaction.user.id)
    await interaction.response.send_message(
        f"Ваш поточний тип особистості: {profile['personality_type']}\n\n"
        "Будь ласка, оберіть свій тип особистості або оберіть 'Видалити тип особистості':",
        view=PersonalityTypeView(),
        ephemeral=True
    )
    await interaction.followup.send(
        "Якщо ви не знаєте свого типу особистості, ви можете пройти [тест на 16 типів особистості](https://www.16personalities.com/uk).",
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
        options.append(discord.SelectOption(label='Видалити тип особистості', description='Видалити поточний тип особистості', value='N/A'))
        self.add_item(PersonalityTypeSelect(options=options))

class PersonalityTypeSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Оберіть свій MBTI тип особистості або видаліть поточний", options=options)

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(interaction.user.id)
        selected_type = self.values[0]
        profile['personality_type'] = selected_type
        if selected_type == 'N/A':
            message = "🔖 Ваш тип особистості було видалено."
        else:
            description = get_mbti_description(selected_type)
            message = f"🔖 Тип особистості встановлено: {selected_type}: {description}."
        await interaction.response.send_message(message, ephemeral=True)

# Команда для встановлення хобі з можливістю знімати вибір
@bot.tree.command(name="sethobbies", description="Встановіть або оновіть свої хобі.")
async def sethobbies(interaction: discord.Interaction):
    profile = get_or_create_profile(interaction.user.id)
    await interaction.response.send_message(
        f"Ваші поточні хобі: {', '.join(profile['hobbies']) if profile['hobbies'] else 'немає'}\n\n"
        "Будь ласка, оберіть категорію хобі для додавання або видалення:",
        view=HobbyCategoryView()
        # Removed ephemeral=True to keep the message persistent
    )
    await interaction.followup.send(
        "Натисніть кнопку для додавання власного хобі або видалення існуючих.",
        view=ManageHobbiesView(),
        ephemeral=True
    )

class ManageHobbiesView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(AddCustomHobbyButton())
        self.add_item(RemoveHobbiesButton())

class RemoveHobbiesButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Видалити хобі 🗑️", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(interaction.user.id)
        if not profile['hobbies']:
            await interaction.response.send_message("У вас немає хобі для видалення.", ephemeral=True)
            return
        await interaction.response.send_message(
            "Оберіть хобі для видалення:",
            view=RemoveHobbiesView(profile['hobbies']),
            ephemeral=True
        )

class RemoveHobbiesView(discord.ui.View):
    def __init__(self, hobbies):
        super().__init__()
        options = [discord.SelectOption(label=hobby) for hobby in hobbies]
        self.add_item(RemoveHobbiesSelect(options))

class RemoveHobbiesSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder='Оберіть хобі для видалення', options=options, min_values=1, max_values=len(options))

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(interaction.user.id)
        for hobby in self.values:
            if hobby in profile['hobbies']:
                profile['hobbies'].remove(hobby)
        await interaction.response.send_message(f"🗑️ Видалено хобі: {', '.join(self.values)}", ephemeral=True)

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
            view=HobbySelectView(self.category, interaction.user.id),
            ephemeral=True
        )

class HobbySelectView(discord.ui.View):
    def __init__(self, category, user_id):
        super().__init__()
        options = self.get_hobby_options(category, user_id)
        self.add_item(HobbySelect(options=options, user_id=user_id))

    @staticmethod
    def get_hobby_options(category, user_id):
        hobbies_dict = {
            "Творчість і медіа": [
                'Малювання', 'Фотографія', 'Музика (гра на інструментах)', 'Танці',
                'Писання (блоги, поезія, проза)', 'Відеомонтаж', 'Графічний дизайн'
            ],
            "Активний відпочинок і спорт": [
                'Біг', 'Йога', 'Фітнес', 'Футбол', 'Кемпінг та походи', 'Екстримальні види спорту (скелелазіння)'
            ],
            "Технології та ігри": [
                'Відеоігри', 'Кодинг/програмування', 'Кіберспорт', 'Моделювання ігор'
            ],
            "Розвиток і самовдосконалення": [
                'Читання книг', 'Медитація', 'Психологія', 'Астрологія'
            ],
            "Домашнє дозвілля": [
                'Кулінарія', 'Садівництво', 'DIY проекти – створення речей своїми руками (меблі, декор, одяг)', 'Колекціонування (марки, монети)'
            ],
            "Подорожі та дослідження": [
                'Подорожі', 'Астрономія', 'Історичні реконструкції', 'Робота з тваринами'
            ]
        }
        profile = get_or_create_profile(user_id)
        user_hobbies = profile['hobbies']
        options = []
        for hobby in hobbies_dict.get(category, []):
            options.append(discord.SelectOption(label=hobby, default=hobby in user_hobbies))
        return options

class HobbySelect(discord.ui.Select):
    def __init__(self, options, user_id):
        super().__init__(placeholder='Оберіть свої хобі (обрані будуть додані/зняті)', options=options, min_values=0, max_values=len(options))
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(self.user_id)
        selected_hobbies = set(self.values)

        # Hobbies in the current category
        current_category_hobbies = set(option.label for option in self.options)

        # User's current hobbies
        user_hobbies = set(profile['hobbies'])

        # Hobbies from the current category that the user had previously selected
        previous_selected_in_category = user_hobbies.intersection(current_category_hobbies)

        # Hobbies to add: selected_hobbies - previous_selected_in_category
        new_hobbies = selected_hobbies - previous_selected_in_category

        # Hobbies to remove: previous_selected_in_category - selected_hobbies
        removed_hobbies = previous_selected_in_category - selected_hobbies

        # Update the user's hobbies
        profile['hobbies'] = list((user_hobbies - removed_hobbies).union(new_hobbies))

        message = ""
        if new_hobbies:
            message += f"🌱 Додано хобі: {', '.join(new_hobbies)}\n"
        if removed_hobbies:
            message += f"🗑️ Видалено хобі: {', '.join(removed_hobbies)}\n"
        if not message:
            message = "Ваші хобі залишилися без змін."

        await interaction.response.send_message(message, ephemeral=True)

# Додавання власного хобі
class AddCustomHobbyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(AddCustomHobbyButton())

class AddCustomHobbyButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Додати власне хобі ✏️", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Введіть свої хобі через кому:",
            ephemeral=True
        )

        def check(m):
            return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

        try:
            message = await bot.wait_for('message', check=check, timeout=60.0)
            hobbies = [hobby.strip() for hobby in message.content.split(',')]
            profile = get_or_create_profile(interaction.user.id)
            profile['hobbies'].extend(hobbies)
            await interaction.followup.send(f"🌱 Додано хобі: {', '.join(hobbies)}", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("⏱️ Час на введення хобі вичерпано. Спробуйте знову.", ephemeral=True)

# Команда для встановлення стилів спілкування з можливістю знімати вибір
@bot.tree.command(name="setcommunicationstyle", description="Встановіть або оновіть свої стилі спілкування.")
async def setcommunicationstyle(interaction: discord.Interaction):
    profile = get_or_create_profile(interaction.user.id)
    await interaction.response.send_message(
        f"Ваші поточні стилі спілкування: {', '.join(profile['communication_styles']) if profile['communication_styles'] else 'немає'}\n\n"
        "Будь ласка, оберіть свої стилі спілкування (можна знімати вибір з тих, що вже обрані):",
        view=CommunicationStyleView(interaction.user.id),
        ephemeral=True
    )

class CommunicationStyleView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.add_item(CommunicationStyleSelect(user_id))

class CommunicationStyleSelect(discord.ui.Select):
    def __init__(self, user_id):
        self.user_id = user_id
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
        profile = get_or_create_profile(user_id)
        user_styles = profile['communication_styles']
        for option in options:
            option.default = option.label in user_styles
        super().__init__(
            placeholder="Оберіть свої стилі спілкування",
            options=options,
            min_values=0,
            max_values=len(options)
        )

    async def callback(self, interaction: discord.Interaction):
        profile = get_or_create_profile(self.user_id)
        selected_styles = set(self.values)
        profile['communication_styles'] = list(selected_styles)
        message = f"💬 Стилі спілкування оновлено: {', '.join(selected_styles)}"
        await interaction.response.send_message(message, ephemeral=True)

# Команда для видалення профілю
@bot.tree.command(name="deleteprofile", description="Видалити свій профіль.")
async def deleteprofile(interaction: discord.Interaction):
    # Запит підтвердження від користувача
    await interaction.response.send_message(
        "Ви впевнені, що хочете видалити свій профіль? Цю дію не можна буде скасувати.",
        view=ConfirmDeleteProfileView(),
        ephemeral=True
    )

class ConfirmDeleteProfileView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ConfirmDeleteButton())
        self.add_item(CancelDeleteButton())

class ConfirmDeleteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="✅ Так, видалити профіль", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in user_profiles:
            del user_profiles[user_id]
            await interaction.response.send_message("Ваш профіль було успішно видалено.", ephemeral=True)
        else:
            await interaction.response.send_message("У вас немає профілю для видалення.", ephemeral=True)

class CancelDeleteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="❌ Скасувати", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Видалення профілю скасовано.", ephemeral=True)

bot.run(TOKEN)
