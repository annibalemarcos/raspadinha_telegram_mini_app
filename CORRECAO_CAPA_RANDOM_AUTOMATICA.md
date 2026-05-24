# Correção: capa opcional com tema automático

Agora o campo:

```txt
Capa / tema da raspadinha
```

é opcional.

## Como funciona

Se o admin enviar uma imagem:

```txt
usa a capa enviada
```

Se o admin não enviar nada:

```txt
o Mini App usa uma capa automática/randomizada
```

A escolha é baseada no ID da raspadinha para manter consistência visual.

## Temas automáticos

- 💎 diamante
- 🔥 fogo
- 🍀 sorte
- 👑 rei
- 🪙 moeda
- ⭐ estrela
- 🎰 cassino
- 🌈 arco-íris

## Arquivos alterados

- `backend/app/templates/admin/scratch_cards.html`
- `backend/app/static/miniapp/app.js`
- `backend/app/static/miniapp/app.css`
- `README.md`
