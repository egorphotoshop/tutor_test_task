from enum import IntEnum, Enum


class FragileObjectDistanceException(BaseException):
    """Расстояние при перевозке хрупких объектов не должно быть больше 30 км."""


class DeliveryCost(IntEnum):
    MORE_30_KM = 300
    UP_TO_30_KM = 200
    UP_TO_10_KM = 100
    UP_TO_2_KM = 5


class CargoVolume(IntEnum):
    BIG = 200
    SMALL = 100


class IsFragile(IntEnum):
    FRAGILE = 300  # Distance must be less than 30 km


class DeliveryServiceLoad(Enum):
    VERY_HIGH = 1.6
    HIGH = 1.4
    MAJOR = 1.2
    STANDARD = 1


def check_is_fragile(is_fragile: bool, distance: int, total: float):
    if is_fragile:
        if distance < 30:
            total += 300
        else:
            raise FragileObjectDistanceException


def get_distance_k(distance: int | float) -> int | float:
    return (
        DeliveryCost.UP_TO_2_KM if distance < 2
        else DeliveryCost.UP_TO_10_KM if distance < 10
        else DeliveryCost.UP_TO_30_KM if distance < 30
        else DeliveryCost.MORE_30_KM
    )


def get_volume_k(is_big_volume: bool) -> int:
    return CargoVolume.BIG if is_big_volume else CargoVolume.SMALL


def check_if_minimum(total: int | float) -> int | float:
    return max(total, 400)


def delivery_cost_calculation(
        distance: int,
        is_big_volume: bool,
        delivery_service_load: float,
        is_fragile: bool = False,
) -> int | float:
    ans = 0

    check_is_fragile(is_fragile, distance, ans)

    distance_k = get_distance_k(distance)

    volume_k = get_volume_k(is_big_volume)

    ans = (distance_k + volume_k) * delivery_service_load

    ans = check_if_minimum(ans)

    return round(ans, 2)


if __name__ == '__main__':
    ans = delivery_cost_calculation(
        distance=215,
        is_big_volume=True,
        delivery_service_load=DeliveryServiceLoad.VERY_HIGH.value,
        is_fragile=False
    )

    print(ans)
