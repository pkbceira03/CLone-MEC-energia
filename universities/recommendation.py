from datetime import date

from utils.energy_bill_util import EnergyBillUtils
from contracts.models import EnergyBill

class Recommendation:

    @classmethod
    def get_energy_bills_for_recommendation(cls, consumer_unit_id):
        energy_bills = []

        try:
            energy_bills_dates = EnergyBillUtils.generate_dates_for_recommendation(date.today())

            for energy_bill_object in energy_bills_dates:
                energy_bill = EnergyBill.get_energy_bill(
                    consumer_unit_id,
                    energy_bill_object['month'], 
                    energy_bill_object['year'])

                if energy_bill:
                    energy_bill_object['energy_bill'] = EnergyBillUtils.energy_bill_dictionary(energy_bill)
                
                energy_bills.append(energy_bill_object)

            # A Conta de Luz do mês atual somente é considerada para a recomendação caso seja preechida
            current_energy_bill = EnergyBill.get_energy_bill(
                    consumer_unit_id,
                    date.today().month, 
                    date.today().year)

            if current_energy_bill:
                energy_bill = EnergyBillUtils.create_energy_bill_date(current_energy_bill.date.month, current_energy_bill.date.year)
                energy_bill['energy_bill'] = EnergyBillUtils.energy_bill_dictionary(current_energy_bill)

                energy_bills.insert(0, energy_bill)
                energy_bills.pop()

            return energy_bills
        except Exception as e:
            raise Exception('Error get energy bills for recommendation: ' + str(e))

    @classmethod
    def get_all_energy_bills_by_consumer_unit(cls, consumer_unit_id, start_date):
        try:
            energy_bills_recommendation_dates_list = EnergyBillUtils.generate_dates_for_recommendation(date.today())
            energy_bills_lists = EnergyBillUtils.generate_dates(start_date, date.today())
            
            for years in energy_bills_lists:
                for energy_bill_object in energy_bills_lists[str(years)]:
                    energy_bill = EnergyBill.get_energy_bill(
                        consumer_unit_id,
                        energy_bill_object['month'], 
                        energy_bill_object['year'])

                    is_date_be_on_recommendation_list = EnergyBillUtils.is_date_be_on_recommendation_list(energy_bills_recommendation_dates_list, energy_bill_object)

                    if energy_bill:
                        energy_bill_object['energy_bill'] = EnergyBillUtils.energy_bill_dictionary(energy_bill)
                        energy_bill_object['is_energy_bill_pending'] = False
                    else:
                        energy_bill_object['is_energy_bill_pending'] = is_date_be_on_recommendation_list

                    energy_bill_object['month'] -= 1

            return energy_bills_lists
        except Exception as e:
            raise Exception('Error get all energy bills by consumer unit: ' + str(e))