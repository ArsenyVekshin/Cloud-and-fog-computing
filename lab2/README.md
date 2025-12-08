# Лабораторная работа №2: Миграция в Kubernetes (Переход к Cloud-Native)

## Цель 
Перенести нагрузку из Лабораторной №1 в Kubernetes. Так как мы избегаем OpenShift, используйте Minikube или Kind (Kubernetes in Docker). Это научит работать с примитивами (Pods, Deployments, Services), которые OpenShift обычно скрывает за абстракциями.

## Инструменты 
Minikube (или Kind), kubectl.

## Ход работы:
1. Трансляция (Translation): Вы должны вручную "перевести" логику Docker
Compose в манифесты K8s:
 - deployment.yaml для приложения Python (определение образа и реплик).
 - deployment.yaml для Redis.
 - service.yaml (тип ClusterIP) для внутреннего доступа к Redis.
 - service.yaml (тип NodePort или LoadBalancer) для внешнего доступа к приложению.
2. Развертывание: Применить манифесты к локальному кластеру (kubectl apply).
3. Rolling Update (Обновление без простоя): Вы меняете код Python (например, цвет фона), собирают образ версии v2, обновляют YAML-файл и наблюдают, как Kubernetes выполняет постепенное обновление подов без остановки сервиса.

---


## Выполнение работы

### Шаг 1: Запуск Minikube

```bash
minikube start
minikube docker-env --shell powershell | Invoke-Expression
```

### Шаг 2: Сборка Docker-образа v1

```bash
docker build -t visit-counter:v1 .
```

### Шаг 3: Развертывание в Kubernetes

```bash
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml

kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
```

### Шаг 4: Проверка развертывания

```bash
# Проверить статус подов
kubectl get pods

# Проверить статус deployments
kubectl get deployments

# Проверить статус сервисов
kubectl get services

# Детальная информация о поде
kubectl describe pod <pod-name>

# Просмотр логов
kubectl logs <pod-name>
```

### Шаг 5: Доступ к приложению

```bash
minikube service visit-counter
```
---

## Rolling Update (Обновление без простоя)
### Шаг 1: Сборка образа v2

```bash
copy app-v2.py app.py
docker build -t visit-counter:v2 .
```

### Шаг 2: Применение Rolling Update
```bash
# Применить обновленный deployment с версией v2
kubectl apply -f k8s/app-deployment-v2.yaml

# Наблюдать за процессом обновления в реальном времени
kubectl rollout status deployment/visit-counter

# Следить за подами во время обновления
kubectl get pods -w
```

### Шаг 3: Проверка обновления

```bash
# Проверить текущую версию образа в deployment
kubectl describe deployment visit-counter | grep Image

# Посмотреть историю развертываний
kubectl rollout history deployment/visit-counter
```

### Шаг 4: Откат (если необходимо)

```bash
# Откат к предыдущей версии
kubectl rollout undo deployment/visit-counter

# Откат к конкретной ревизии
kubectl rollout undo deployment/visit-counter --to-revision=1
```

---

## Полезные команды

```bash
# Масштабирование deployment
kubectl scale deployment visit-counter --replicas=3

# Просмотр событий
kubectl get events --sort-by=.metadata.creationTimestamp

# Выполнение команды в поде
kubectl exec -it <pod-name> -- /bin/sh

# Проброс порта напрямую к поду
kubectl port-forward <pod-name> 5000:5000

# Удаление всех ресурсов
kubectl delete -f k8s/

# Остановка Minikube
minikube stop

# Удаление кластера
minikube delete
```