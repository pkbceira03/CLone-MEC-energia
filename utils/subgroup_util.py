class Subgroup:
    AS = 'AS'
    A4 = 'A4'
    A3A = 'A3a'
    A3 = 'A3'
    A2 = 'A2'
    A1 = 'A1'

    subgroups = [
        {
            "name": AS,
            "min": 0,
            "max": 2.3,
            "equals": None,
        },
        {
            "name": A4,
            "min": 2.3,
            "max": 25,
            "equals": None,
        },
        {
            "name": A3A,
            "min": 30,
            "max": 44,
            "equals": None,
        },
        {
            "name": A3,
            "min": None,
            "max": None,
            "equals": 69,
        },
        {
            "name": A2,
            "min": 88,
            "max": 138,
            "equals": None,
        },
        {
            "name": A1,
            "min": 230,
            "max": 999999,
            "equals": None,
        }
    ]


    def get_subgroup(supply_voltage_in_kv: float):
        for subgroup in Subgroup.subgroups:
            if subgroup['min'] and subgroup['max']:
                if supply_voltage_in_kv >= subgroup['min'] and supply_voltage_in_kv < subgroup['max']:
                    return subgroup['name']
            
            if subgroup['equals']:
                if supply_voltage_in_kv == subgroup['equals']:
                    return subgroup['name']
        
        raise Exception('Subgroup not found for this supply voltage')

    def get_all_subgroups():
        return Subgroup.subgroups