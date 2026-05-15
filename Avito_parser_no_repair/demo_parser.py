import pandas as pd
import datetime

# Ключевые слова из вашего ТЗ
INCLUDE_KEYWORDS = [
    "без ремонта", "требуется ремонт", "черновая отделка",
    "под отделку", "коробка дома", "без внутренней отделки"
]

EXCLUDE_KEYWORDS = [
    "евроремонт", "дизайнерский ремонт", "с ремонтом",
    "готов к проживанию", "заезжай и живи"
]


def is_no_repair(text):
    if not text:
        return False
    text_lower = text.lower()
    for exc in EXCLUDE_KEYWORDS:
        if exc in text_lower:
            return False
    for inc in INCLUDE_KEYWORDS:
        if inc in text_lower:
            return True
    return False


# Демо-объявления (имитация данных с Avito)
demo_data = [
    {
        "title": "Продается дом в Подмосковье",
        "price": "4 500 000 ₽",
        "url": "https://www.avito.ru/moskva/dom_bez_remonta_123",
        "description": "Дом 100 кв.м. Требуется ремонт. Хороший участок, коммуникации подведены.",
        "address": "Московская область, Чеховский район",
        "date": "сегодня"
    },
    {
        "title": "Коттедж с евроремонтом",
        "price": "15 000 000 ₽",
        "url": "https://www.avito.ru/moskva/kottedzh_s_remontom_456",
        "description": "Дизайнерский ремонт, готова к проживанию. Заезжай и живи!",
        "address": "МО, Красногорск",
        "date": "вчера"
    },
    {
        "title": "Дача под отделку",
        "price": "2 800 000 ₽",
        "url": "https://www.avito.ru/moskva/dacha_pod_otdelku_789",
        "description": "Дачный домик, черновая отделка. Можно делать любой ремонт.",
        "address": "Дмитровский район",
        "date": "2 дня назад"
    },
    {
        "title": "Таунхаус без внутренней отделки",
        "price": "7 200 000 ₽",
        "url": "https://www.avito.ru/moskva/taunhaus_bez_remonta_101",
        "description": "Коробка дома, без внутренней отделки. Подведены коммуникации.",
        "address": "МО, Мытищи",
        "date": "сегодня"
    },
    {
        "title": "Дом с ремонтом",
        "price": "9 500 000 ₽",
        "url": "https://www.avito.ru/moskva/dom_s_remontom_202",
        "description": "Косметический ремонт, можно жить сразу.",
        "address": "Истринский район",
        "date": "5 дней назад"
    }
]

print("🔍 Начинаем фильтрацию объявлений...")
print("=" * 60)

results = []
for item in demo_data:
    full_text = f"{item['title']} {item['description']}"
    is_good = is_no_repair(full_text)

    if is_good:
        results.append(item)
        print(f"✅ ПОДХОДИТ: {item['title']}")
        print(f"   Причина: нет ремонта\n")
    else:
        print(f"❌ ИСКЛЮЧЕН: {item['title']}")
        print(f"   Причина: объявление с ремонтом\n")

# Сохраняем результаты
df = pd.DataFrame(results)
filename_xlsx = "avito_no_repair_demo.xlsx"
filename_csv = "avito_no_repair_demo.csv"

df.to_excel(filename_xlsx, index=False)
df.to_csv(filename_csv, index=False, encoding="utf-8-sig")

print("=" * 60)
print(f"📊 РЕЗУЛЬТАТ:")
print(f"   Всего объявлений: {len(demo_data)}")
print(f"   Подходит: {len(results)}")
print(f"   Исключено: {len(demo_data) - len(results)}")
print(f"\n📁 Файлы сохранены:")
print(f"   - {filename_xlsx}")
print(f"   - {filename_csv}")
print("=" * 60)

# Выводим первые 5 подходящих
if results:
    print("\n📋 СПИСОК ПОДХОДЯЩИХ ОБЪЯВЛЕНИЙ:")
    for i, ad in enumerate(results[:5], 1):
        print(f"{i}. {ad['title']}")
        print(f"   Цена: {ad['price']}")
        print(f"   Адрес: {ad['address']}")
        print(f"   Ссылка: {ad['url']}\n")