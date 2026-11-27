# Histórico de alterações

[English](../CHANGELOG.md) · [Início](README.md)

Este arquivo registra as alterações significativas integradas ao Oppy. O código identifica a versão `0.1.0`. As datas descrevem o histórico de desenvolvimento e não correspondem a lançamentos separados com tags. Propostas ficam nas issues.

## [Unreleased]

### Adicionado

- Saída somente leitura de `status --json` para scripts de monitoramento.
- Notificações do Telegram e prévia do resumo opcionais em inglês por meio de `BEACON_NOTIFICATION_LANGUAGE=en`. O português brasileiro continua sendo o padrão.
- Guia de contribuição, código de conduta, política de comunicação de vulnerabilidades, modelos bilíngues de issues e modelo de pull request em inglês.
- Traduções brasileiras das notas sobre o portal PSG, o parser, a persistência e a entrega de notificações, além deste histórico.

### Alterado

- Revisão das instruções do README sobre instalação, configuração, atualizações, backups, limitações da fonte e primeiros passos para colaboradores. O comportamento do programa foi preservado.

## 2026-11-21 — Revisão de confiabilidade

### Corrigido

- Limite de espera ao reiniciar com valores de Retry-After muito longos já armazenados. Preservação apenas dos pares completos de capturas de diagnóstico sem remover arquivos alheios. Esclarecimento dos rótulos de inscrição e da redação das notificações em português ([#13](https://github.com/kayo-willian/oppy/pull/13)). O PR registrou 63 testes offline aprovados.

## 2026-11-20 — Mudança de nome para Oppy e diagnóstico

### Adicionado

- Armazenamento do HTML rejeitado e dos metadados em capturas privadas com retenção limitada, com o caminho disponível no estado do programa ([#12](https://github.com/kayo-willian/oppy/pull/12)).

### Alterado

- Mudança do nome OpportunityBeacon para Oppy e inclusão da capa original, preservando o esquema SQLite, o caminho do banco, as configurações de ambiente e o volume Docker ([#10](https://github.com/kayo-willian/oppy/pull/10)).
- Esclarecimentos sobre a única fonte implementada e a configuração de um bot pessoal do Telegram ([#11](https://github.com/kayo-willian/oppy/pull/11)).

## 2026-11-19 — Primeiro marco funcional

### Adicionado

- Base em Python e SQLite, armazenamento persistente no Compose e CI offline ([#1](https://github.com/kayo-willian/oppy/pull/1), [#3](https://github.com/kayo-willian/oppy/pull/3)).
- Reconhecimento da fonte PSG, amostras sanitizadas, capturas normalizadas e associação de cursos ([#2](https://github.com/kayo-willian/oppy/pull/2), [#4](https://github.com/kayo-willian/oppy/pull/4), [#5](https://github.com/kayo-willian/oppy/pull/5)).
- Alterações de estado atômicas, fila persistente de notificações, agendador, requisições HTTP com limites, entrega no Telegram, diagnóstico local e backup do SQLite ([#6](https://github.com/kayo-willian/oppy/pull/6), [#7](https://github.com/kayo-willian/oppy/pull/7)).
- Parser de HTML tolerante, diagnóstico dos smoke tests por etapa, notificações detalhadas em português e resumos do estado salvo ([#8](https://github.com/kayo-willian/oppy/pull/8), [#9](https://github.com/kayo-willian/oppy/pull/9)).

[Unreleased]: https://github.com/kayo-willian/oppy/commits/main/
