from tariffs.models import Distributor
from universities.models import University


class CreateDistributorTestUtil:
    distributors_dict = [
        {
            'name': 'Neoenergia',
            'cnpj': '01083200000118'
        },
        {
            'name': 'CEB',
            'cnpj': '07522669000192'
        }
    ]

    @classmethod
    def create_distributor(cls, index: int, university: University):
        dist_dict = cls.distributors_dict[index]
        distributor = Distributor.objects.create(
            name=dist_dict['name'],
            cnpj=dist_dict['cnpj'],
            university=university
        )

        return dist_dict, distributor
