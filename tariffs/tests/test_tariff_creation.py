import pytest

from universities.models import University
from tariffs.models import Distributor

from tariffs.tests.utils import create_blue_tariff, create_green_tariff

@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        university_dict = {
            'name': 'Universidade de São Paulo',
            'cnpj': '63025530000104'
        }

        self.university = University.objects.create(**university_dict)

        self.distributor = Distributor.objects.create(
            name='Distribuidora de Energia',
            cnpj='63025530000104',
            university=self.university
        )

    def test_creates_blue_tariff(self):
        tariff = create_blue_tariff(self.distributor.id)

        assert tariff.is_blue()

        blue_tariff = tariff.as_blue_tariff()

        assert 1 == blue_tariff.peak_tusd_in_reais_per_kw
        assert 4 == blue_tariff.off_peak_tusd_in_reais_per_kw

    def test_creates_green_tariff(self):
        tariff = create_green_tariff(self.distributor.id)

        assert not tariff.is_blue()

        green_tariff = tariff.as_green_tariff()

        assert 1 == green_tariff.peak_tusd_in_reais_per_mwh
        assert 5 == green_tariff.na_tusd_in_reais_per_kw

    def test_mishandles_green_tariff_as_blue_tariff(self):
        tariff = create_green_tariff(self.distributor.id)

        with pytest.raises(Exception) as e:
            tariff.as_blue_tariff()
        assert 'Cannot convert' in str(e.value)

    def test_mishandles_blue_tariff_as_green_tariff(self):
        tariff = create_blue_tariff(self.distributor.id)

        with pytest.raises(Exception) as e:
            tariff.as_green_tariff()
        assert 'Cannot convert' in str(e.value)
