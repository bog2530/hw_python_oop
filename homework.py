class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_1: float = 18
    COEFF_2: float = 20
    MINUT: float = 60

    def get_spent_calories(self) -> float:
        calories_form_1 = (self.COEFF_1 * self.get_mean_speed() - self.COEFF_2)
        hour = self.duration * self.MINUT
        return calories_form_1 * self.weight / self.M_IN_KM * hour


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_1: float = 0.035
    COEFF_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coef_1_weight = self.COEFF_1 * self.weight
        coef_2_weight = self.COEFF_2 * self.weight
        form_1 = self.get_mean_speed() ** 2 // self.weight
        calories = (coef_1_weight + form_1 * coef_2_weight) * self.duration
        return calories * Running.MINUT


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_1: float = 1.1
    COEFF_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_form_1 = self.length_pool * self.count_pool / self.M_IN_KM
        return mean_speed_form_1 / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_form_1 = self.get_mean_speed() + self.COEFF_1
        calories_form_2 = self.COEFF_2 * self.weight
        return calories_form_1 * calories_form_2


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code = {'RUN': Running, 'SWM': Swimming, 'WLK': SportsWalking}
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
