from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    REPORT = ("Тип тренировки: {training_type}; "
              "Длительность: {duration:.3f} ч.; "
              "Дистанция: {distance:.3f} км; "
              "Ср. скорость: {speed:.3f} км/ч; "
              "Потрачено ккал: {calories:.3f}.")

    def get_message(self) -> str:
        return self.REPORT.format(**asdict(self))


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    IN_MINUTES = 60
    """Базовый класс тренировки."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод не должен вызываться '
                                  'в классе Training')
    # Я так понял, что можно что угодно тут писать,
    # лишь бы коллеги поняли, верно?

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    AVG_SPEED_COEFF_1 = 18
    AVG_SPEED_COEFF_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.AVG_SPEED_COEFF_1 * self.get_mean_speed()
                - self.AVG_SPEED_COEFF_2) * self.weight / Training.M_IN_KM
                * self.duration * self.IN_MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_COEFF_1 = 0.035  # weight_coeff тк. влияет на вес
    AVG_SPEED_COEFF_3 = 0.029  # avg_speed_coeff тк. влияет на среднюю скорость
    SPEED_MULTIPLIER = 2

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return (self.WEIGHT_COEFF_1 * self.weight
                + (self.get_mean_speed() ** self.SPEED_MULTIPLIER
                   // self.height)
                * self.AVG_SPEED_COEFF_3) * (self.duration * self.IN_MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    WEIGHT_COEFF_2 = 2
    AVG_SPEED_COEFF_4 = 1.1

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    # Тут был переопределяемый get_distance
    # долго не получалось заставить всё работать без переопределения
    # в итоге додумался изменить метод в родительском классе:
    # Training.LEN_STEP ---> self.LEN_STEP

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.AVG_SPEED_COEFF_4)
                * self.WEIGHT_COEFF_2 * self.weight)


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""

    workout_types: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in workout_types:
        raise ValueError("Неожиданный тип тренировки: workout_type")
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            main(read_package(workout_type, data))
        except KeyError as key_e:
            print(f'Ошибка. Отсуствует ключ {key_e} '
                  'в словаре workout_types')
