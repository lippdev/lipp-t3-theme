# Cloud Rain

Um tema para o [T3 Code](https://t3.codes). O fundo é um céu noturno de nuvens em pixel art, coberto por uma trama fraca de dígitos, com gotas de dígitos caindo devagar por cima. Barra lateral, cabeçalho e menus ficam em azul-marinho translúcido para o céu aparecer por trás.

![Fundo do Cloud Rain](previews/background.png)

*A imagem mostra só o fundo, sem a interface do T3.*

## Instalar

```sh
curl -fsSL https://raw.githubusercontent.com/lippdev/lipp-t3-theme/main/cloud-rain.json -o cloud-rain.json
t3 theme set cloud-rain.json
```

O T3 troca para o Cloud Rain na hora, no app desktop e no navegador. Para voltar, escolha outro tema no seletor de temas ou rode `t3 theme set t3-chat`.

### Pedir para o agente instalar

Cole isto numa conversa do T3 Code:

> Instala o tema Cloud Rain de https://github.com/lippdev/lipp-t3-theme. Siga a seção "Instruções para agentes" do README.

### Instruções para agentes

1. Baixe `https://raw.githubusercontent.com/lippdev/lipp-t3-theme/main/cloud-rain.json`.
2. Se o comando `t3` estiver disponível, rode `t3 theme set <caminho do cloud-rain.json>`.
3. Se não estiver, chame a ferramenta `t3_theme_set` com `themeId: "cloud-rain"` e o JSON do arquivo como `theme`.
4. Não edite o arquivo. As imagens do céu e da chuva estão embutidas no CSS, e um caractere errado faz elas sumirem.

## Requisitos

- Um T3 Code Nightly recente (novembro de 2026 ou mais novo).
- Funciona no app desktop e no navegador. O app de celular não usa temas.

## Notas

- O tema é só escuro.
- A chuva anda uma célula de cada vez, com uma animação que roda na placa de vídeo, então pesa pouco. A barra lateral fica sem desfoque de propósito: desfocar por cima da chuva redesenharia tudo a cada passo.
- Com "reduzir movimento" ligado no sistema, a chuva para.
- O padrão da chuva se repete a cada 480 px na horizontal.
- O fundo usa partes internas do layout do T3. Se uma atualização mudar esse layout, o céu pode voltar ao fundo liso do T3. O resto continua funcionando.

## Mudar o tema

| Arquivo | O que controla |
|---|---|
| `src/theme.css` | Os estilos. As imagens entram nos marcadores `__CLOUDS__`, `__RAIN__` e `__TEXTURE__`. |
| `src/rain.py` | A chuva e a trama de dígitos. `DENSITY` define quantas colunas têm gota, `TRAIL` o tamanho das gotas. |
| `src/clouds.py` | Gera `assets/clouds.png` a partir de uma foto de nuvens, com as cores "midnight". |
| `src/build.py` | Junta tudo em `cloud-rain.json` e as cores da interface. Recusa o build se o CSS passar de 20.000 caracteres, o limite do T3. |

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt   # no Windows: .venv\Scripts\pip
.venv/bin/python src/build.py
```

Para trocar o céu, rode `python src/clouds.py caminho/da/foto.jpg` antes do build.
