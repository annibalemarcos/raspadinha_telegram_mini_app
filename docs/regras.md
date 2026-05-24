# Regras do MVP

## Fluxo correto

- Não existe saldo interno.
- O usuário escolhe uma raspadinha.
- O sistema cria uma invoice Pix fake.
- O usuário pode simular pagamento ou cancelar.
- Invoice pendente não libera jogo.
- Depois do pagamento simulado, o usuário deve inserir a chave Pix.
- A chave Pix deve ser confirmada digitando exatamente igual uma segunda vez.
- Só depois da chave Pix confirmada a raspadinha é liberada.
- Invoice com Pix confirmado libera exatamente uma jogada.
- Cada jogada gera hash SHA-256.
- Se perder, termina o fluxo.
- Se ganhar, o payout demo é registrado automaticamente para a chave Pix já confirmada.
- Tudo aparece no dashboard admin.

## Status de invoice

```txt
pending       → criada, aguardando ação
paid          → pagamento simulado confirmado, aguardando Pix do jogador
pix_confirmed → chave Pix do jogador confirmada, pode raspar
canceled      → cancelada pelo usuário
played        → usada em uma jogada
```

## Status de payout da jogada

```txt
not_applicable → perdeu, sem prêmio
paid_demo      → ganhou, payout fake registrado automaticamente
```

## Distribuição padrão

- 70%: 0
- 15%: reembolso
- 10%: dobro
- 4%: prêmio intermediário
- 1%: prêmio máximo
