class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration:
                 float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")
    pass


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    """Базовый класс тренировки."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
    pass


class Running(Training):
    """Тренировка: бег."""
    cal_rate_1 = 18
    cal_rate_2 = 20
    in_minutes = 60

    def get_spent_calories(self) -> float:
        return ((self.cal_rate_1 * self.get_mean_speed() 
                - self.cal_rate_2) * self.weight / Training.M_IN_KM *
                (self.duration * self.in_minutes))
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.68
    M_IN_KM: int = 1000
    in_minutes = 60

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.cal_rate_3 = 0.035
        self.cal_rate_4 = 0.029
        self.height = height

    def get_spent_calories(self):
        return ((self.cal_rate_3 * self.weight 
                + (self.get_mean_speed() ** 2 // self.height) 
                * self.cal_rate_4) * (self.duration * self.in_minutes))
    pass


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.cal_rate_5 = 1.1
        self.cal_rate_6 = 2

    def get_distance(self) -> float:
        return (self.action * Swimming.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool 
               / Training.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.cal_rate_5)
                * self.cal_rate_6 * self.weight)
    pass


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""
    read: dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if read.get(workout_type) is None:
        return None
    return read.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print((info.get_message()))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training is None:
            print('Неожиданный тип тренировки')
        else:
            main(training)
