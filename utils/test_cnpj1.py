from cnpj_validator_util import CnpjValidator

def test_cnpj_validation(cnpj):
    try:
        CnpjValidator.validate(cnpj)
        print(f"{cnpj}: válido")
    except ValueError as e:
        print(f"{cnpj}: inválido - {e}")
    except Exception as e:
        print(f"{cnpj}: erro inesperado - {e}")

def run_tests():
    test_cases = [
        '58577114000189',   # válido
        'A5857711400018',   # inválido (caractere não numérico)
        '585771140001899',  # inválido (comprimento incorreto)
        '58577114000159',   # inválido (dígitos verificadores inválidos)
        '58577114000183'    # válido
    ]

    for cnpj in test_cases:
        test_cnpj_validation(cnpj)

if __name__ == "__main__":
    run_tests()
