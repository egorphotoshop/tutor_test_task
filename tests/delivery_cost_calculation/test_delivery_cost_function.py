import pytest

from delivery_cost_function import delivery_cost_calculation, DeliveryServiceLoad, \
    FragileObjectDistanceException


@pytest.mark.parametrize(
    ['is_big_volume', 'total'],
    [
        [True, 560.0],
        [False, 420.0]
    ]
)
def test_cargo_volume(is_big_volume, total):
    assert delivery_cost_calculation(
        distance=10,
        is_big_volume=is_big_volume,
        delivery_service_load=DeliveryServiceLoad.HIGH.value,
        is_fragile=True
    ) == total


@pytest.mark.parametrize(
    ['distance', 'total'],
    [
        [0, 400],
        [2, 420],
        [10, 560],
        [30, 700],
        [400000, 700],
    ]
)
def test_distance(distance, total):
    assert delivery_cost_calculation(
        distance=distance,
        is_big_volume=True,
        delivery_service_load=DeliveryServiceLoad.HIGH.value,
        is_fragile=False
    ) == total


@pytest.mark.parametrize(
    ['is_fragile', 'distance', 'total', 'raises_error'],
    [
        [True, 10, 560.0, False],
        [True, 50, None, True],
        [False, 50, 700, False]
    ]
)
def test_is_fragile(is_fragile, distance, total, raises_error):
    if raises_error:
        with pytest.raises(FragileObjectDistanceException):
            delivery_cost_calculation(
                distance=distance,
                is_big_volume=True,
                delivery_service_load=DeliveryServiceLoad.HIGH.value,
                is_fragile=is_fragile
            )
    else:
        assert delivery_cost_calculation(
            distance=distance,
            is_big_volume=True,
            delivery_service_load=DeliveryServiceLoad.HIGH.value,
            is_fragile=is_fragile
        ) == total
