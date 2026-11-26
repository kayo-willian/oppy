![Placa OPPY em pixel art](../assets/oppy-cover.svg)

# Oppy

Oppy é um monitor auto-hospedado que consulta listas públicas de oportunidades em intervalos regulares e envia alertas pelo Telegram quando aparecem novas oportunidades ou mudanças. Atualmente, oferece suporte a uma fonte: o Programa Senac de Gratuidade (PSG) do Senac Pará em Santarém.

[![MIT license](https://img.shields.io/badge/license-MIT-blue?style=flat)](../LICENSE)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2468a2?style=flat)
![SQLite](https://img.shields.io/badge/storage-SQLite-486477?style=flat)
[![Telegram bot](https://img.shields.io/badge/Telegram-bot-2987ac?style=flat)](https://core.telegram.org/bots)
[![Tests](https://img.shields.io/github/actions/workflow/status/kayo-willian/oppy/tests.yml?branch=main&label=tests&style=flat)](https://github.com/kayo-willian/oppy/actions/workflows/tests.yml)
![Built with vibe coding](https://img.shields.io/badge/built%20with-vibe%20coding-c87824?style=flat)

[English](../README.md) · [Início rápido](#início-rápido) · [Configuração](#configuração) · [Contribuição](#contribuição) · [Histórico](../CHANGELOG.md)

Oppy é um projeto pessoal independente, distribuído sob a licença MIT. O Senac Pará é uma fonte de informações, não um parceiro nem mantenedor. Contribuições são bem-vindas; não há garantia de prazos de desenvolvimento ou revisão.

## Fontes suportadas

| Fonte | Escopo | Status |
|---|---|---|
| Senac Pará PSG | Cursos gratuitos em Santarém, de todas as áreas | Implementado |

[Portal da fonte](https://www.pa.senac.br/psg/selecao). Antes de executar consultas reais, confirme se o acesso pretendido é permitido, incluindo consultas recorrentes e requisições às páginas de detalhes vinculadas. Consulte as [notas de reconhecimento da fonte](../docs/psg-recon.md). Nenhuma outra fonte está implementada atualmente.

## O que faz

Oppy compara cada coleta com a última coleta válida e registra cada nova oportunidade ou alteração uma única vez, evitando enfileirar alertas duplicados em consultas repetidas. Uma coleta malsucedida é registrada como falha e nunca interpretada como uma lista vazia. Oppy envia um alerta após falhas consecutivas e outro quando a coleta se recupera. Apenas observa as oportunidades e envia notificações. Nunca realiza inscrições nem coleta informações pessoais de candidatos.

O conector PSG detecta novos processos seletivos e cursos, períodos de inscrição futuros, aberturas, encerramentos, vagas preenchidas e reaberturas. Também acompanha alterações de datas, novos documentos e retificações.

## Como funciona

```text
source connector → parser → SQLite → outbox → Telegram
```

O conector atual é [oppy/psg.py](../oppy/psg.py).

- A primeira coleta válida enfileira um resumo. Resumos longos são enviados em partes numeradas, sem dividir os blocos de cada curso.
- Dentro de uma seleção, Oppy associa cursos primeiro pelo identificador único da fonte e, depois, pelo título e local normalizados. O período do curso desempata turmas que, de outra forma, seriam idênticas.
- Uma coleta malsucedida ou inconclusiva preserva o último estado válido. A ausência do painel do município não pode apagar a lista de cursos.
- Cada alteração e sua notificação pendente são gravadas na mesma transação. A fila de saída (outbox) utiliza entrega pelo menos uma vez e registra o sucesso após a confirmação do Telegram.
- HTTP 403, 429 ou 503 encerra o ciclo atual. Os ciclos posteriores aumentam o intervalo de espera e respeitam um Retry-After mais longo. Uma coleta bem-sucedida restaura o intervalo configurado.

Consulte as [regras do parser](../docs/psg-parser.md) e as [notas sobre SQLite e entrega](../docs/offline-core.md).

## Início rápido

### Requisitos e instalação

Utilize um host Linux com Git, Docker e o plugin Docker Compose. Para desenvolvimento nativo, são necessários Python 3.11 ou superior e dados de fuso horário do sistema. A aplicação utiliza apenas a biblioteca padrão do Python; pytest é uma dependência de desenvolvimento.

```sh
git clone https://github.com/kayo-willian/oppy.git
cd oppy
cp -n .env.example .env
```

Mantenha o arquivo `.env` privado. Configure as credenciais do Telegram conforme as instruções abaixo. Se permanecerem vazias, o monitoramento pode funcionar e as notificações pendentes ficam no SQLite.

### Criar o bot do Telegram

1. Abra uma conversa com `@BotFather` no Telegram. Envie `/newbot`, siga as instruções e guarde o token.
2. Abra uma conversa privada com o novo bot e envie uma mensagem.
3. No navegador, acesse `https://api.telegram.org/bot<TOKEN>/getUpdates`, substituindo `<TOKEN>` pelo seu token. Encontre a mensagem que acabou de enviar e copie o `id` numérico dentro do objeto `chat`.
4. Edite o arquivo `.env` local. Defina `BEACON_TELEGRAM_TOKEN` com o token e `BEACON_TELEGRAM_CHAT_ID` com o ID da conversa.

Trate o token como uma senha. Nunca faça commit nem compartilhe esse valor. A URL de `getUpdates` contém o token e é salva no histórico do navegador. Se o token for exposto, revogue-o com `/revoke` no BotFather.

### Executar com Docker Compose

Execute os comandos na raiz do repositório em Linux. As duas verificações rápidas (smoke tests) são operações manuais opcionais: a consulta ao portal realiza requisições HTTP reais e pode salvar capturas de diagnóstico se o parser falhar; a verificação do Telegram envia uma mensagem real. Confirme a permissão antes de acessar o portal. Os testes automatizados não realizam nenhuma dessas operações.

| Tarefa | Comando |
|---|---|
| Construir a imagem | `docker compose build` |
| Consultar o portal uma vez | `docker compose run --rm oppy python -m oppy smoke` |
| Enviar uma mensagem de teste | `docker compose run --rm oppy python -m oppy smoke-telegram` |
| Iniciar o agendador | `docker compose up -d` |
| Consultar as últimas verificações e mensagens pendentes | `docker compose exec oppy python -m oppy status` |
| Consultar o estado em JSON | `docker compose exec oppy python -m oppy status --json` |
| Exibir o resumo salvo | `docker compose exec oppy python -m oppy summary` |
| Enviar diretamente o resumo salvo | `docker compose exec oppy python -m oppy summary --send` |
| Criar um backup consistente do SQLite | `docker compose exec oppy python -m oppy backup` |
| Ler os logs recentes do serviço | `docker compose logs --tail=50 oppy` |
| Parar o serviço sem remover o volume | `docker compose down` |

O estado JSON é somente leitura. last_success_utc e last_failure_utc são datas em UTC (null até a primeira ocorrência), pending_notifications é a contagem pendente e telegram_configured indica se o Telegram está configurado. Um banco ausente ou ilegível gera erro em stderr e código de saída diferente de zero.

Em uma instalação existente, pare o serviço Compose anterior antes de iniciar o Oppy. Preserve o volume ao desligar. O Compose reutiliza explicitamente `opportunity-beacon_beacon-data` mesmo após renomear diretórios ou o projeto. O banco de dados e seus arquivos WAL permanecem em `/app/data`. Evite `docker compose down -v`, que remove volumes. Pare qualquer instância antiga antes de iniciar outra: o agendador foi projetado para um único worker por banco de dados local.

### Atualizações e backups

Antes de atualizar uma instalação existente, crie um backup com o serviço em execução e copie o arquivo concluído para fora do contêiner, mantendo uma cópia independente. O comando de backup exibe sua localização. Mantenha os backups privados.

```sh
docker compose exec oppy python -m oppy backup
docker compose down
git pull --ff-only origin main
docker compose up -d --build
```

Consulte [CHANGELOG.md](../CHANGELOG.md) antes de atualizar. Para restaurar um backup, pare o agendador, coloque uma cópia do arquivo SQLite salvo em um novo caminho dentro do volume de dados montado, configure `BEACON_DB_PATH` com esse caminho e reinicie. Um banco restaurado pode conter notificações pendentes que serão entregues novamente. Nunca sobrescreva um banco em uso.

### Diagnosticar alterações em uma página

Quando o parser rejeita uma página de listagem ou detalhes, Oppy guarda os bytes da resposta e um arquivo JSON com a URL da requisição, data e hora UTC, status HTTP, resultado do parser e motivo. Os dez pares mais recentes ficam em diretórios acessíveis apenas ao proprietário, em `failed-snapshots/`, ao lado do banco. Falhas de transporte e respostas grandes demais não geram capturas.

Execute `docker compose exec oppy python -m oppy status` para localizar o HTML mais recente. Copie seu **diretório pai** para obter os dois arquivos (substitua `<snapshot-id>` pelo nome do diretório informado no caminho):

```sh
docker compose cp 'oppy:/app/data/failed-snapshots/<snapshot-id>' ./snapshot
```

Revise o HTML bruto e os metadados em busca de informações pessoais ou sensíveis antes de compartilhá-los publicamente.

## Configuração

Mantive o prefixo `BEACON_` para preservar a compatibilidade com arquivos `.env` existentes.

| Variável | Significado e valor padrão |
|---|---|
| `BEACON_DB_PATH` | Caminho do SQLite. Padrão: `data/beacon.sqlite3`. Mantenha-o dentro do diretório de dados montado no Compose. |
| `BEACON_INTERVAL_MINUTES` | Minutos de espera após um ciclo concluído. Padrão 30, mínimo 10; utilize apenas uma frequência permitida pela fonte. |
| `BEACON_FAILURE_ALERT_AFTER` | Número de verificações consecutivas malsucedidas ou inconclusivas antes de um alerta de incidente. Padrão 3. |
| `BEACON_NOTIFICATION_LANGUAGE` | `pt-BR` (padrão) ou `en` (inglês). Aplica-se ao Telegram e à prévia local de `summary`. Valores não reconhecidos usam português. Títulos dos cursos, locais e nomes dos documentos preservam a redação da fonte. |
| `BEACON_TELEGRAM_TOKEN` | Token do bot fornecido pelo BotFather. Vazio por padrão. |
| `BEACON_TELEGRAM_CHAT_ID` | Conversa de destino. Se qualquer uma das duas configurações do Telegram estiver vazia, as notificações permanecem pendentes. |
| `BEACON_BACKUP_PATH` | Novo arquivo de destino. Por padrão, um arquivo com data e hora no nome, ao lado do banco. |

## Limitações

Oppy consulta oportunidades apenas enquanto a máquina e o serviço estão em execução. Um período curto de inscrição pode passar entre consultas. A entrega pelo menos uma vez pode gerar uma duplicata se o processo parar depois de o Telegram aceitar a mensagem, mas antes de o SQLite registrar o sucesso.

Oppy não é uma ferramenta de inscrição. Não inspeciona o conteúdo de PDFs; acompanha os links e nomes dos documentos, portanto substituições com URL e nome inalterados podem não ser detectadas.

Inscrições presenciais podem ter status desconhecido. A extração depende do HTML do portal. Um ciclo completo consulta a listagem uma vez e segue um link de detalhes por seleção de Santarém, com no máximo uma nova tentativa para erros transitórios elegíveis.

## Testes

Os testes utilizam HTML salvo, bancos SQLite temporários e simulações HTTP locais. A CI executa a suíte offline. As verificações no portal real são manuais.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install "pip>=25.1"
python -m pip install --group dev
python -m pytest -q
```

## Roadmap

Possíveis melhorias futuras, ainda não implementadas nem agendadas:

- Suportar outras fontes públicas de oportunidades em que o acesso automatizado seja permitido.
- Adicionar canais de notificação além do Telegram.
- Explorar exportações somente para leitura.

Consulte as [issues abertas](https://github.com/kayo-willian/oppy/issues) para propostas específicas. Sugestões e pull requests são bem-vindos, mas uma proposta não implica compromisso de implementação.

## Contribuição

Você pode ajudar com documentação, testes de regressão offline, feedback sobre implantação, exportação de dados, formatação de notificações ou propostas de novas fontes. Não é necessário ter um token do Telegram, um bot em execução ou acesso ao portal PSG para contribuir.

1. [Faça um fork do repositório](https://github.com/kayo-willian/oppy/fork) e crie uma branch específica a partir da `main` do projeto original.
2. Leia [CONTRIBUICAO.md](CONTRIBUICAO.md) e [AGENTS.md](../AGENTS.md).
3. Execute os testes offline, faça a alteração e adicione testes de regressão relevantes.
4. Abra um pull request para `main` e descreva a validação efetivamente realizada e suas limitações.

| Recurso | Finalidade |
|---|---|
| [Guia de contribuição](CONTRIBUICAO.md) | Desenvolvimento, revisão e testes seguros |
| [Código de conduta](CODIGO_DE_CONDUTA.md) | Participação respeitosa |
| [Política de segurança](SEGURANCA.md) | Opções de comunicação privada de vulnerabilidades |
| [Issues](https://github.com/kayo-willian/oppy/issues) | Relatos de bugs e propostas de funcionalidades; inglês e português brasileiro são bem-vindos |
| [Pull requests](https://github.com/kayo-willian/oppy/pulls) | Alterações propostas e revisões |
| [Histórico](../CHANGELOG.md) | Alterações significativas integradas |

O README possui versões em inglês e português brasileiro. Os guias de contribuição, conduta e segurança também estão disponíveis em português. A documentação técnica interna, o código, os commits e os pull requests permanecem em inglês. Issues públicas criadas pelo projeto e modelos de issues usam inglês e português brasileiro; colaboradores podem responder ou reportar problemas em qualquer um dos dois idiomas. Forks independentes permanecem livres para evoluir sob a licença MIT.

## Como este projeto foi construído

Idealizei o Oppy e defini seus objetivos, requisitos, prioridades e limites. Não escrevi o código manualmente: a implementação foi realizada por meio de vibe coding, com ferramentas de IA desempenhando papéis distintos.

| Papel | Responsável |
|---|---|
| Ideia, requisitos, decisões, testes na minha própria máquina, revisão e merge de cada pull request | Eu |
| Briefing inicial do projeto | ChatGPT 6 (esforço alto) |
| Escrita dos prompts de cada fase, revisão dos relatórios do Codex, revisão técnica do plano | Claude Sonnet 5.5 (esforço médio) |
| Código, testes e configuração do Docker | OpenAI Codex, GPT-6.2 Model Astra (esforço médio) |

O ChatGPT elaborou o primeiro briefing, o Claude o revisou e sugeriu melhorias (uma outbox para notificações, hashes dos campos normalizados, testes offline com HTML salvo e uma distinção clara entre coleta malsucedida e coleta vazia), e enviei cada fase ao Codex como um prompt. O Codex abriu um pull request por fase. Revisei cada um, executei pessoalmente os testes com Docker e os smoke tests, e só fiz o merge quando fiquei satisfeito. O Claude não teve acesso ao repositório e não executou o código; trabalhou a partir dos relatórios e resultados que compartilhei.

## Licença

[MIT](../LICENSE).
