import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================

def test_bug1_subtotal_considera_quantidade(pedido_pequeno):
    # 1 x 6,00 + 2 x 4,50 = 15,00
    assert pedido_pequeno.subtotal() == 15.0


def test_bug2_frete_gratis_com_exatamente_50():
    pedido = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert pedido.tem_frete_gratis() is True


def test_bug3_item_mais_barato(pedido_pequeno):
    # Café 6,00 x Pão de queijo 4,50
    assert pedido_pequeno.item_mais_barato().nome == "Pão de queijo"


def test_bug4_desconto_subtrai_do_subtotal():
    pedido = Pedido("Carla", [Item("Marmita", 100.0, 1)])
    assert pedido.total_com_desconto(10) == 90.0



# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função

def test_contar_frete_gratis_todos_com_frete(pedido_grande):
    pedido_50 = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert contar_frete_gratis([pedido_grande, pedido_50]) == 2


def test_contar_frete_gratis_nenhum_com_frete(pedido_pequeno):
    pedido_49 = Pedido("Carla", [Item("Combo", 49.99, 1)])
    assert contar_frete_gratis([pedido_pequeno, pedido_49]) == 0


def test_contar_frete_gratis_lista_mista(pedido_pequeno, pedido_grande):
    assert contar_frete_gratis([pedido_pequeno, pedido_grande]) == 1


def test_contar_frete_gratis_lista_vazia():
    assert contar_frete_gratis([]) == 0



# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método

def test_situacao_tudo_disponivel_abaixo_de_50(pedido_pequeno):
    assert pedido_pequeno.situacao(0) == "Confirmado"


def test_situacao_tudo_disponivel_a_partir_de_50(pedido_grande):
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"


def test_situacao_mais_de_25_porcento_cancela_mesmo_com_frete(pedido_grande):
    # 5 unidades, 2 indisponíveis = 40%
    assert pedido_grande.situacao(2) == "Cancelado por falta de estoque"


def test_situacao_exatamente_25_porcento_segue_para_frete():
    # 4 unidades, 1 indisponível = 25%; subtotal 4 x 12,50 = 50,00
    pedido = Pedido("Carla", [Item("Lanche", 12.5, 4)])
    assert pedido.situacao(1) == "Confirmado com frete grátis"


def test_situacao_pouco_acima_de_25_porcento_cancela():
    # 7 unidades, 2 indisponíveis = 28,6%
    pedido = Pedido("Carla", [Item("Pastel", 5.0, 7)])
    assert pedido.situacao(2) == "Cancelado por falta de estoque"



# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método

def test_sugerir_frete_gratis_abaixo_de_50_envia_sms(pedido_pequeno):
    sms_service = MagicMock()

    pedido_pequeno.sugerir_frete_gratis(sms_service)

    # subtotal 15,00 -> faltam 35,00
    sms_service.enviar.assert_called_once_with("Bruno", 35.0)


def test_sugerir_frete_gratis_acima_de_50_nao_envia_sms(pedido_grande):
    sms_service = MagicMock()

    pedido_grande.sugerir_frete_gratis(sms_service)

    sms_service.enviar.assert_not_called()
