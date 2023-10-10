import string
import threading
from threading import Thread
from queue import Queue
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
from collections import Counter
import vk_api
from telethon.sync import TelegramClient
import asyncio
import tkinter as tk

# Ваши API ключи и данные пользователя ВКонтакте
VK_API_KEY = '8cfd674f8cfd674f8cfd674f2f8fe8a1c188cfd8cfd674fe9e9c46c6ee3e864a6bd414b'
# Ваши API ID и API хэш для Telegram, полученные при регистрации приложения на https://my.telegram.org
TG_API_ID = '27071189'
TG_API_HASH = 'f7b40d943c57dfae1a4ae9f0b8781703'

# Авторизация в VK API
vk_session = vk_api.VkApi(token=VK_API_KEY)
vk = vk_session.get_api()

nlp = spacy.load("ru_core_news_sm")

# Метод для получения идентификатора пользователя по имени
def get_user_id_by_name(username):
    try:
        response = vk.users.get(user_ids=username)
        user_id = response[0]['id']
        return user_id
    except Exception as e:
        print(f"Ошибка при получении идентификатора пользователя: {e}")
        return None

# Метод для получения записей со стены пользователя или группы
def get_wall_posts(owner_id, count=30):
    try:
        response = vk.wall.get(owner_id=owner_id, count=count)
        return response['items']
    except Exception as e:
        print(f"Ошибка при получении записей со стены: {e}")
        return []

# Загрузка данных из VK
def scrape_vk_data(usernames, group_ids, data_queue):
    for username in usernames:
        user_id = get_user_id_by_name(username)
        if user_id is not None:
            user_posts = get_wall_posts(user_id, count=30)
            for post in user_posts:
                data_queue.put(post['text'])

    for group_id in group_ids:
        group_posts = get_wall_posts(group_id, count=30)
        for post in group_posts:
            data_queue.put(post['text'])

# Загрузка данных из Telegram
async def scrape_telegram_data(group_names, data_queue, num_messages):
    api_id = TG_API_ID
    api_hash = TG_API_HASH

    # Создаем клиент и авторизуемся
    client = TelegramClient('session_name', api_id, api_hash,
                            system_version='4.16.30-vxCUSTOM')
    await client.start()

    for group_name in group_names:
        # Получаем информацию о группе по ее имени
        group_entity = await client.get_input_entity(group_name)

        # Читаем последние сообщения из группы
        async for message in client.iter_messages(group_entity, limit=num_messages):
            data_queue.put(message.text)

    # Завершаем работу Telegram клиента
    await client.disconnect()
    client.disconnect()

# Создание блокировки для синхронизации доступа к общему списку
preprocessed_data_lock = threading.Lock()

# Предварительная обработка данных
def preprocess_data(data_queue, preprocessed_data, stop_words):
    while True:
        data = data_queue.get()
        if data is None:
            break

        data = data.lower()
        tokens = word_tokenize(data, language='russian')
        # Исключаем слова, состоящие только из тире и слова, содержащие тире
        tokens = [word for word in tokens if word not in stop_words and not all(c in string.punctuation + '–«»—“”''' for c in word)]

        with preprocessed_data_lock:
            preprocessed_data.extend(tokens)

# Анализ данных на предмет ключевых слов и фраз
def analyze_keywords(data, keyword_counts):
    doc = nlp(data)
    target_keywords = ["митинг"]
    for token in doc:
        if token.text in target_keywords:
            keyword_counts[token.text] += 1

# Выполнить анализ данных
def perform_analysis():
    # Количество потоков
    num_threads = 3

    # Список пользователей VK, чьи записи вы хотите получить
    vk_users_to_fetch = ['durov']

    # Список групп VK, чьи записи вы хотите получить
    vk_groups_to_fetch = [-194944166, -29725717]  # Замените на ID групп, которые вы хотите анализировать

    # Имя Telegram группы, из которой вы хотите получить сообщения
    telegram_group_name = ['murza4ch', 'readovkanews', 'bazabazon']

    data_queue_vk = Queue()
    data_queue_telegram = Queue()
    preprocessed_data_vk = []
    preprocessed_data_telegram = []
    keyword_counts_vk = Counter()
    keyword_counts_telegram = Counter()
    stop_words = set(stopwords.words('russian'))

    # Создание потоков для сбора данных из VK
    vk_scraping_threads = [Thread(target=scrape_vk_data, args=(vk_users_to_fetch, vk_groups_to_fetch, data_queue_vk)) for _ in range(num_threads)]

    # Количество сообщений, которые нужно получить из Telegram
    num_telegram_messages = 30
    # Создание потока для сбора данных из Telegram
    telegram_scraping_thread = Thread(target=lambda: asyncio.run(scrape_telegram_data(telegram_group_name, data_queue_telegram, num_telegram_messages)))

    # Создание потоков для предварительной обработки данных
    preprocessing_threads = [Thread(target=preprocess_data, args=(data_queue_vk, preprocessed_data_vk, stop_words)), Thread(target=preprocess_data, args=(data_queue_telegram, preprocessed_data_telegram, stop_words))]

    for thread in vk_scraping_threads:
        thread.start()

    telegram_scraping_thread.start()

    for thread in preprocessing_threads:
        thread.start()

    for thread in vk_scraping_threads:
        thread.join()

    telegram_scraping_thread.join()

    # Добавление сигналов о завершении обработки в очередь данных
    for _ in range(num_threads):
        data_queue_vk.put(None)
        data_queue_telegram.put(None)

    for thread in preprocessing_threads:
        thread.join()

    # Анализ данных на предмет ключевых слов и фраз
    for data_item in preprocessed_data_vk:
        analyze_keywords(data_item, keyword_counts_vk)

    for data_item in preprocessed_data_telegram:
        analyze_keywords(data_item, keyword_counts_telegram)

    for keyword, count in keyword_counts_vk.items():
        keyword_counts_vk[keyword] = count // (num_threads + 1)

    for keyword, count in keyword_counts_telegram.items():
        keyword_counts_telegram[keyword] = count // (num_threads)

    result_text_vk.delete(1.0, tk.END)
    result_text_telegram.delete(1.0, tk.END)

    # Выведите результаты по VK в соответствующее текстовое поле
    result_text_vk.insert(tk.END, "Количество найденных ключевых слов и фраз в VK:\n")
    result_text_vk.insert(tk.END, str(keyword_counts_vk) + "\n")

    result_text_vk.insert(tk.END, "\n10 самых употребляемых слов и их количество в VK:\n")
    word_counts_vk = Counter(preprocessed_data_vk)
    top_words_vk = word_counts_vk.most_common(10)
    for word, count in top_words_vk:
        result_text_vk.insert(tk.END, f'{word}: {count // (num_threads + 1)}\n')

    # Выведите результаты по Telegram в соответствующее текстовое поле
    result_text_telegram.insert(tk.END, "Количество найденных ключевых слов и фраз в Telegram:\n")
    result_text_telegram.insert(tk.END, str(keyword_counts_telegram) + "\n")

    result_text_telegram.insert(tk.END, "\n10 самых употребляемых слов и их количество в Telegram:\n")
    word_counts_telegram = Counter(preprocessed_data_telegram)
    top_words_telegram = word_counts_telegram.most_common(10)
    for word, count in top_words_telegram:
        result_text_telegram.insert(tk.END, f'{word}: {count // (num_threads)}\n')


root = tk.Tk()
root.title("Анализ данных")

# Создаем метку с инструкциями
instructions_label = tk.Label(root, text="Нажмите кнопку, чтобы проанализировать данные.")
instructions_label.pack(pady=10)
result_text_vk = tk.Text(root)
result_text_vk.pack()
result_text_telegram = tk.Text(root)
result_text_telegram.pack()
# Создаем кнопку для выполнения анализа
analyze_button = tk.Button(root, text="Провести анализ", command=perform_analysis)
analyze_button.pack(pady=10)

# Запускаем главный цикл GUI
root.mainloop()






















