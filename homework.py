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

        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
    # "Вместо pass тут отлично подойдет исключение NotImplementedError."
    # Это должно выглядеть так?
        return NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CAL_RATE_1 = 18
    CAL_RATE_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.CAL_RATE_1 * self.get_mean_speed()
                - self.CAL_RATE_2) * self.weight / Training.M_IN_KM
                * self.duration * self.IN_MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP: float = 0.68
    M_IN_KM: int = 1000
    CAL_RATE_3 = 0.035
    CAL_RATE_4 = 0.029
    SPEED_MULTIPLIER = 2

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.CAL_RATE_3 * self.weight
                + (self.get_mean_speed() ** self.SPEED_MULTIPLIER
                 // self.height)
                 * self.CAL_RATE_4) * (self.duration * self.IN_MINUTES))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CAL_RATE_5 = 1.1
    CAL_RATE_6 = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self):
        return (self.action * Swimming.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.CAL_RATE_5)
                * self.CAL_RATE_6 * self.weight)


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""

    dicti: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in dicti:
        # "...лучше вообще развернуть проверку наоборот..."
        # "...аварийный возврат с исключением и текстом ошибки с ключом..."
        raise NotImplementedError("Неожиданный тип тренировки")
        # Так? Или по-другому?
    else:
        return dicti[workout_type](*data)


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
        # "Ловить нужно исключение"
        if read_package(workout_type, data) is None:
            # Имелось ввиду, что нужно местами поменять if и else
            main(read_package(workout_type, data))
            # Или нужно было использовать try/except?
        else:
            print('Неожиданный тип тренировки')
