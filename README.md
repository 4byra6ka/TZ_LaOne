Разработать чат-бота для телеграмм.

Задачу, которую должен решать бот:
1. В боте должно быть меню из 3 кнопок: «Получить информацию по товару», «Остановить уведомления», «получить информацию из БД».
2. Нажимая на кнопку «Получить информацию по товару» Пользователь отправляет в бота артикул товара с Wildsberries (например: 211695539).
3. Бот должен выдать информацию о товаре (карточке) - Название, артикул, цена, рейтинг товара, количество товара НА ВСЕХ СКЛАДАХ.
Все эти данные легко получаются по запросу:  https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={артикул товара}
4. Под сообщением, которые присылает бот должна быть inline-кнопка - «подписаться». По нажатию на которую должны приходить уведомления в бот каждые 5 минут с сообщением, что было выше. (Название, артикул, цена, рейтинг товара, количество товара НА ВСЕХ СКЛАДАХ)
5. При нажатии на кнопку «Остановить уведомления» - уведомления останавливаются.
6. При нажатии на кнопку «получить информацию из БД» бот должен прислать сообщение с последними 5 записями из БД.

Бот должен быть написан на Python 3.9+, с использованием библиотек: Aiogram 3. Уведомления должны быть написаны с использованием Celery. Реализуйте взаимодействие с базой данных для сохранения истории запросов (используйте SQLAlchemy и PostgreSQL). Должны сохраняться id пользователя, время запроса, артикул товара. Бота упаковать в docker. Запустить на своем сервере. Прислать ссылку на бота. Прислать ссылку на репозиторий с кодом.

Оформление внутри бота - сообщений и тд на ваше усмотрение, но приветствуется оригинальный подход.

После ознакомления с тестовым заданием НАПИШИТЕ ВАШ DEADLINE ПО ЭТОМУ БОТУ.

### Критика:
***
Логирование ошибок:

Добавьте обработку ошибок и логирование важных событий. Например, если есть проблемы при подключении к базе данных или при запуске бота, логи могут помочь вам быстро выявить и исправить проблемы.
***
Использование контекстного менеджера для сессии:

Вместо того, чтобы вызывать async with engine.begin() as conn, вы можете использовать async_sessionmaker для удобства работы с сессией
***
Использование асинхронного метода create_all:

Вы можете использовать асинхронный метод create_all для создания таблиц базы данных. Это позволяет избежать блокировки цикла событий, которую вызывает синхронный метод create_all.
***
Добавление логики обработки событий и ошибок:

Вы можете добавить обработчики событий, чтобы обрабатывать ситуации, такие как успешный запуск бота, ошибки соединения с базой данных и другие важные моменты.
***
Использование команд для обработки "отмены":

Вы можете использовать фильтр Command("cancel") вместо F.text.casefold() == "cancel" для обработки команды "cancel". Это делает код более ясным и читаемым.
***
Логика обработки выбора меню:

При обработке выбора меню (например, "Получить информацию по товару"), вы можете создать отдельные функции для каждого пункта меню. Это делает код более модульным и легко расширяемым.
***
Использование строкового форматирования:

Вместо использования f"{int(wb_data["salePriceU"])/100}руб", вы можете использовать строковое форматирование, чтобы сделать код более читаемым.
***
Использование InlineKeyboardMarkup для кнопок вместо ReplyKeyboardMarkup:

Если вы хотите использовать inline-кнопки для "Подписаться" и "Отмена", вы можете использовать InlineKeyboardMarkup вместо ReplyKeyboardMarkup.