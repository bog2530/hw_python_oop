from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEXT: str = ('Тип тренировки: {training_type}; '
                 'Длительность: {duration:.3f} ч.; '
                 'Дистанция: {distance:.3f} км; '
                 'Ср. скорость: {speed:.3f} км/ч; '
                 'Потрачено ккал: {calories:.3f}.'
                 )

    def get_message(self) -> str:
        """Возвращает строку с результатами тренировки."""

        return self.TEXT.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_qty: int = action
        self.duration_hour: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action_qty * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__, self.duration_hour,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_SPEED_1: float = 18
    COEFF_SPEED_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_SPEED_1 * self.get_mean_speed()
                - self.COEFF_SPEED_2) * self.weight_kg
                / self.M_IN_KM * self.duration_hour * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WEIGHT_1: float = 0.035
    COEFF_WEIGHT_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_WEIGHT_1 * self.weight_kg + (self.get_mean_speed()
                ** 2 // self.height_cm) * self.COEFF_WEIGHT_2 * self.weight_kg)
                * self.duration_hour * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_SPEED_1: float = 1.1
    COEFF_WEIGHT_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool
        self.count_pool_qty: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool_m * self.count_pool_qty / self.M_IN_KM
                / self.duration_hour)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.COEFF_SPEED_1)
                * self.COEFF_WEIGHT_2 * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    code: dict[str, type[Training]] = {'RUN': Running,
                                       'SWM': Swimming,
                                       'WLK': SportsWalking,
                                       }
    return code.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""

    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
