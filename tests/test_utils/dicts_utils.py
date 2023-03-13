from datetime import date

# ---------------------------------------
# Universidades

university_dict_1 = {
    'name': 'Universidade de São Paulo',
    'cnpj': '63025530000104'
}

# ---------------------------------------
# Unidades Consumidoras

consumer_unit_dict_1 = {
    'name': 'Darcy Ribeiro',
    'code': '000000000',
    'is_active': True,
},

consumer_unit_dict_2 = {
    'name': 'Faculdade do Gama',
    'code': '111111111',
    'is_active': True,
},

consumer_unit_dict_3 = {
    'name': 'Faculdade de Planaltina',
    'code': '222222222',
    'is_active': True,
}

# ---------------------------------------
# Contrato

contract_dict_1 = {
    'start_date': date(year = 2022, month = 1, day = 1),
    'tariff_flag': 'V',
    'supply_voltage': 100.00,
    'peak_contracted_demand_in_kw': 100.00,
    'off_peak_contracted_demand_in_kw': 100.00,
},

contract_dict_2 = {
    'start_date': date(year=2023, month = 1, day = 1),
    'tariff_flag': 'A',
    'supply_voltage': 250.00,
    'peak_contracted_demand_in_kw': 250.00,
    'off_peak_contracted_demand_in_kw': 250.00,
},

contract_dict_3 = {
    'start_date': date(year=2024, month = 1, day = 1),
    'tariff_flag': 'A',
    'supply_voltage': 69,
    'peak_contracted_demand_in_kw': 250.00,
    'off_peak_contracted_demand_in_kw': 250.00,
},

contract_dict_4 = {
    'start_date': date(year=2025, month = 1, day = 1),
    'tariff_flag': 'V',
    'supply_voltage': 100.00,
    'peak_contracted_demand_in_kw': 100.00,
    'off_peak_contracted_demand_in_kw': 100.00,
},

contract_dict_5 = {
    'start_date': date(year=2050, month = 1, day = 1),
    'tariff_flag': 'A',
    'supply_voltage': 70,
    'peak_contracted_demand_in_kw': 250.00,
    'off_peak_contracted_demand_in_kw': 250.00,
},

contract_dict_6 = {
    'start_date': date(year=2023, month = 1, day = 1),
    'tariff_flag': 'V',
    'supply_voltage': 100.00,
    'peak_contracted_demand_in_kw': 100.00,
    'off_peak_contracted_demand_in_kw': 100.00,
},

# ---------------------------------------
# Conta de Luz

energy_bill_dict_1 = {
    'date': date.today(),
    'invoice_in_reais': 100.00,
    'is_atypical': False,
    'peak_consumption_in_kwh': 100.00,
    'off_peak_consumption_in_kwh': 100.00,
    'peak_measured_demand_in_kw': 100.00,
    'off_peak_measured_demand_in_kw': 100.00,
}

# ---------------------------------------
# Distribuidoras

distributor_dict_1 = {
    'name': 'Neoenergia',
    'cnpj': '01083200000118'
},

distributor_dict_2 = {
    'name': 'CEB',
    'cnpj': '07522669000192'
}

# ---------------------------------------
# Tarifas

tariff_dict_1 = {
    'start_date': date.today(),
    'end_date': date.today(),
    'subgroup': 'A3',
    'peak_tusd_in_reais_per_kw': 1,
    'peak_tusd_in_reais_per_mwh': 2,
    'peak_te_in_reais_per_mwh': 3,
    'off_peak_tusd_in_reais_per_kw': 4,
    'off_peak_tusd_in_reais_per_mwh': 5,
    'off_peak_te_in_reais_per_mwh': 6
}