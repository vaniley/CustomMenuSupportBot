# CustomMenuSupportBot

![example image](.github/image.png)

CustomMenuSupportBot - это гибкий и настраиваемый Telegram-бот, разработанный для предоставления поддержки и информации через иерархическую систему меню. Созданный на Python с использованием фреймворка Aiogram, этот бот позволяет легко настраивать многоуровневые меню для различных задач поддержки.

## Особенности

- Настраиваемая многоуровневая система меню
- Легко редактируемый файл конфигурации JSON
- Функция кнопки "Назад" для удобной навигации
- Поддержка неограниченной глубины меню
- Использование Aiogram для эффективных асинхронных операций

## Конфигурация

Файл `config.json` управляет структурой и содержимым меню бота. Отредактируйте этот файл, чтобы настроить бота под ваши конкретные нужды. Структура файла выглядит следующим образом:

```json
{
    "welcome_message": "Приветственное сообщение",
    "menu": {
        "Раздел 1": {
            "description": "Описание",
            "menu": {
                "Подраздел 1.1": {
                    "description": "Описание"
                },
                ...
            }
        },
        ...
    }
}
```

## Функциональность бота

Бот предоставляет следующие основные функции:

1. Отображение приветственного сообщения при запуске.
2. Генерация клавиатуры на основе структуры меню из config.json.
3. Навигация по меню с помощью встроенных кнопок.
4. Возможность возврата на предыдущий уровень меню.
5. Отображение описания для каждого раздела и подраздела.
6. Динамическое обновление сообщений при навигации по меню.

Бот легко адаптируется под различные сценарии использования, такие как техническая поддержка, FAQ, обучающие материалы и многое другое, просто путем изменения содержимого файла конфигурации.