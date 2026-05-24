# Regras configuráveis de raspadinha

Agora cada raspadinha tem `match_count`.

## Exemplos

```txt
match_count = 1 → 1 símbolo ganha
match_count = 3 → 3 iguais ganha
match_count = 4 → 4 iguais ganha
```

## Onde configurar

No admin:

```txt
/admin/scratch-cards
```

Campo:

```txt
Regra de vitória
```

## Importante

A regra visual controla o que aparece na grade.

A chance real de ganhar continua vindo da tabela `scratch_prizes`, ou seja, das probabilidades de prêmio.

Na prática:

```txt
Prêmio sorteado > 0 → gera símbolos vencedores conforme match_count
Prêmio sorteado = 0 → gera símbolos perdedores conforme match_count
```

Isso impede o visual de mentir para o resultado.
