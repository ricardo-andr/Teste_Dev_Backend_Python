import re

class ValidarCpf():
    
    def isValid(cpf):
        
        cpf = re.sub(r'[.-]+', "", cpf)
    
        if len(cpf) != 11:
            return False

        if cpf in (c * 11 for c in "1234567890"):
            return False

        cpf_reverso = cpf[::-1]
        for i in range(2, 0, -1):
            cpf_enumerado = enumerate(cpf_reverso[i:], start=2)
            dv_calculado = sum(map(lambda x: int(x[1]) * x[0], cpf_enumerado)) * 10 % 11
            if cpf_reverso[i - 1:i] != str(dv_calculado % 10):
                return False

        return True