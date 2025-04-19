import re
from datetime import datetime, timedelta

def validar_linha_digitavel(linha: str) -> dict:
    linha = re.sub(r'\D', '', linha)

    if len(linha) not in (47, 48):
        return {'valido': False}

    # Identificando tipo de boleto (bancário ou convênio)
    tipo = 'convênio' if linha[0] in '89' else 'bancário'

    # Banco (só para boletos bancários)
    banco = linha[:3] if tipo == 'bancário' else None

    # Fator de vencimento (boletos bancários)
    fator = int(linha[33:37]) if tipo == 'bancário' else None
    base_date = datetime(1997, 10, 7)
    vencimento = (base_date + timedelta(days=fator)).strftime('%Y-%m-%d') if fator else None

    # Valor (últimos 10 dígitos nos boletos bancários)
    valor_str = linha[37:47] if tipo == 'bancário' else linha[4:15]
    valor = f"{int(valor_str) / 100:.2f}"

    return {
        'valido': True,
        'tipo': tipo,
        'banco': banco,
        'vencimento': vencimento,
        'valor': valor
    }

