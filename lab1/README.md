# Лабораторная работа №1: Задача масштабирования (Docker → Swarm)

## Цель
Изучить разницу между простым запуском контейнера и оркестрацией сервиса. Эта работа закрывает пробел между "работает на моем ноутбуке" и "работает в кластере".

## Сценарий
Вы выступаете в роли DevOps-инженеров простого интернет-магазина, которому нужно справиться с наплывом трафика (например, в "Черную пятницу").

## Приложение
Простое двухуровневое приложение:
 - Frontend: Веб-страница на Python/Flask, отображающая счетчик посещений.
 - Backend: База данных Redis для хранения количества хитов.
## Ход работы
1. Контейнеризация: Написать Dockerfile для Python-приложения.
2. Docker Compose: Написать docker-compose.yml для локального запуска связки App + Redis. Убедиться, что они "видят" друг друга.
3. Инициализация Swarm: Перевести Docker в режим Swarm (docker swarm init).
4. Развертывание стека (Deploy Stack): Конвертировать файл compose в деплой стека (Stack Deploy).
5. Тест на отказ (Self-healing): Вы вручную "убиваете" (docker kill) активный контейнер и наблюдают, как Swarm автоматически пересоздает его.
6. Масштабирование: Выполнить команду docker service scale frontend=5.

## Ход работы

### Шаг 1: Контейнеризация
```bash
docker build -t visit-counter:latest .
```

### Шаг 2: Запуск с Docker Compose (локальный режим)
Запустите приложение локально для проверки:

```bash
docker-compose up -d
```
Приложение будет доступно по адресу: http://localhost:5000

```bash
docker-compose down
```

### Шаг 3: Инициализация Docker Swarm

```bash
docker swarm init
```

### Шаг 4: Развертывание стека (Stack Deploy)

```bash
docker stack deploy -c docker-compose.yml shop
docker service ps
```

### Шаг 5: Тест на отказ (Self-healing)
```bash
docker ps
docker kill <CONTAINER_ID>
docker service ps
```

### Шаг 6: Масштабирование
```bash
docker service scale shop_frontend=5
docker ps
```
---

## Полезные команды

```bash
# Посмотреть все сервисы
docker service ls

# Логи сервиса
docker service logs shop_frontend

# Информация о сервисе
docker service inspect shop_frontend

# Удалить стек
docker stack rm shop

# Выйти из режима Swarm
docker swarm leave --force
```

---

## Очистка
```bash
docker stack rm shop
docker swarm leave --force
docker rmi visit-counter:latest
```
