import pytest

from delivery_cost_function import delivery_cost_calculation, DeliveryServiceLoad, \
    FragileObjectDistanceException


class TestDeliveryCost:
    @pytest.mark.parametrize(
        ['is_big_volume', 'total'],
        [
            [True, 560.0],
            [False, 420.0]
        ]
    )
    def test_cargo_volume(self, is_big_volume, total):
        """Проверка с учетом объема груза."""
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
    def test_distance(self, distance, total):
        """Проверка с учетом расстояния до пункта назначения."""
        assert delivery_cost_calculation(
            distance=distance,
            is_big_volume=True,
            delivery_service_load=DeliveryServiceLoad.HIGH.value,
            is_fragile=False
        ) == total

    @pytest.mark.parametrize(
        ['service_load', 'total'],
        [
            [DeliveryServiceLoad.STANDARD.value, 500],
            [DeliveryServiceLoad.MAJOR.value, 600],
            [DeliveryServiceLoad.HIGH.value, 700],
            [DeliveryServiceLoad.VERY_HIGH.value, 800],
        ]
    )
    def test_service_load(self, service_load, total):
        """Проверка с учетом загруженности службы доставки."""
        assert delivery_cost_calculation(
            distance=50,
            is_big_volume=True,
            delivery_service_load=service_load,
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
    def test_is_fragile(self, is_fragile, distance, total, raises_error):
        """Проверка с учетом хрупкого груза."""
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
