from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.MESSAGE.format(**asdict(self))


class Training():
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Нужно переопределить метод')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        duration_in_m: float = self.duration * self.HOUR_IN_MIN
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                            * self.get_mean_speed()
                            + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM
                           * duration_in_m)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KM_PER_H_IN_M_PER_S: float = 0.278
    FIRST_COEFFICIENT: float = 0.035
    SECOND_COEFFICIENT: float = 0.029
    SM_IN_M: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        mean_speed_in_mPs: float = (self.get_mean_speed()  # m/s
                                    * self.KM_PER_H_IN_M_PER_S)
        height_in_m: float = self.height / self.SM_IN_M
        duration_in_m: float = self.duration * self.HOUR_IN_MIN

        calories: float = ((self.FIRST_COEFFICIENT * self.weight
                            + (mean_speed_in_mPs**2 / height_in_m)
                            * self.SECOND_COEFFICIENT * self.weight)
                           * duration_in_m)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    FIRST_COEFFICIENT: float = 1.1
    SECOND_COEFFICIENT: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        calories: float = ((self.get_mean_speed() + self.FIRST_COEFFICIENT)
                           * self.SECOND_COEFFICIENT
                           * self.weight * self.duration)
        return calories


WORKOUT_NAMES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return WORKOUT_NAMES[workout_type](*data)
    except KeyError:
        raise KeyError('Такой тренеровки нет')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
