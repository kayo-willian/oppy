# Como contribuir com o Oppy

[English](../CONTRIBUTING.md) · [Documentação em português](README.md)

> Tradução para português brasileiro. Em caso de divergência, consulte a versão original em inglês.

Contribuições são bem-vindas, tanto de quem está aprendendo Python, Linux ou Docker quanto de quem já mantém software de monitoramento. Oppy é um pequeno projeto independente e auto-hospedado. Você pode fazer um fork, relatar problemas, melhorar a documentação ou enviar um pull request específico. Estas diretrizes se aplicam às contribuições ao projeto original, não aos forks independentes sob a [licença MIT](../LICENSE).

## Escopo

Oppy monitora listas públicas de oportunidades e envia notificações. Sua única fonte implementada é o PSG do Senac Pará para cursos gratuitos em Santarém. Telegram é o único provedor externo de notificações implementado. Mantenha o núcleo de monitoramento simples, preserve o comportamento existente e discuta novas fontes, dependências ou mudanças arquiteturais significativas em uma issue antes de implementá-las.

Contribuições úteis incluem relatos de bugs reproduzíveis, testes de regressão com fixtures, acessibilidade e formatação de notificações, documentação de instalação, exportações somente para leitura e propostas de fontes com escopo definido.

Consulte a [lista de colaboradores do GitHub](https://github.com/kayo-willian/oppy/graphs/contributors) para os créditos dos commits.

## Primeiros passos

Use um ambiente de desenvolvimento Linux com Git e Python 3.11 ou superior. O runtime utiliza a biblioteca padrão. Os testes offline precisam de pytest, mas não exigem Docker, conta do Telegram, credenciais ou acesso real ao portal.

1. Faça um fork do repositório no GitHub e clone seu fork.
2. Adicione o remoto upstream e crie uma branch específica.

   ```sh
   git clone https://github.com/YOUR-USERNAME/oppy.git
   cd oppy
   git remote add upstream https://github.com/kayo-willian/oppy.git
   git fetch upstream
   git switch -c fix/descriptive-name upstream/main
   ```

3. Prepare o ambiente de desenvolvimento e execute a suíte existente.

   ```sh
   python3 -m venv .venv
   . .venv/bin/activate
   python -m pip install "pip>=25.1"
   python -m pip install --group dev
   python -m pytest -q
   ```

4. Faça a menor alteração coerente. Adicione testes de regressão quando apropriado. Execute novamente a suíte e confira o diff.
5. Faça commit, envie para seu fork e abra um pull request para a branch `main` do projeto original.

   ```sh
   git diff --check
   git status --short
   git add -- path/to/changed-file
   git commit -m "fix: describe the change"
   git push -u origin fix/descriptive-name
   ```

Substitua o nome de usuário, a branch e o caminho de arquivo dos exemplos. Use nomes descritivos para branches e separe alterações não relacionadas.

## Requisitos técnicos e de segurança

- Mantenha os testes automatizados offline. Utilize fixtures HTML reduzidas e sanitizadas, bancos SQLite temporários, provedores simulados e simulações em loopback. Não acesse o portal PSG real nem envie mensagens pelo Telegram no pytest ou na CI.
- Confirme as condições de acesso aplicáveis antes de propor ou testar manualmente uma fonte real. Use um User-Agent identificável, requisições limitadas, intervalos conservadores e tratamento de Retry-After. Nunca contorne controles de acesso, CAPTCHA ou limites de requisição, adivinhe identificadores ou colete dados de candidatos.
- Separe o parser específico da fonte dos registros normalizados e da detecção de mudanças. Preserve identidades estáveis dos cursos, estados desconhecidos e a última coleta válida. Uma resposta vazia ou malformada não deve apagar dados válidos.
- Preserve gravações atômicas de estado, eventos e outbox, a deduplicação de eventos e a entrega pelo menos uma vez. Não afirme que o Telegram entrega exatamente uma vez.
- Preserve as configurações existentes `BEACON_`, as migrações do banco e o nome legado do volume Compose, salvo se houver um plano de compatibilidade revisado explicitamente.
- Mantenha credenciais, arquivos reais de ambiente, bancos SQLite, logs privados e capturas HTML brutas de falhas fora do Git e de relatos públicos. Sanitize fixtures antes de adicioná-las.
- Prefira a arquitetura existente baseada na biblioteca padrão. Não adicione serviços, bancos ou dependências sem necessidade clara.

Leia as [notas do parser](docs/psg-parser.md), o [reconhecimento da fonte](docs/psg-recon.md) e a [documentação do núcleo](docs/offline-core.md) para entender a implementação.

## Issues e propostas

Pesquise issues e PRs existentes antes de abrir outro. Utilize o modelo de relato de bug ou proposta de funcionalidade. Inclua o commit, ambiente, passos de reprodução, comportamento esperado e observado e evidências sanitizadas. Uma proposta de fonte deve identificar a listagem pública, condições de acesso, campos de identidade, mudanças esperadas e um plano seguro de testes offline; não implemente nem execute coletas recorrentes antes da revisão.

Issues públicas e seus modelos são bilíngues (inglês e português brasileiro). Você pode escrever ou responder em qualquer idioma sem precisar traduzir por conta própria. Código, commits e pull requests usam inglês. As traduções dos documentos técnicos e comunitários ficam em `pt-BR/` e devem acompanhar os originais. Para suspeitas de vulnerabilidades, siga [SEGURANCA.md](SEGURANCA.md) em vez de publicar detalhes sensíveis.

## Checklist de revisão

Explique o problema, o escopo, o impacto na compatibilidade e as concessões envolvidas. Relate os testes efetivamente realizados, inclusive falhas e verificações não executadas. Atualize a documentação e a seção Unreleased do [CHANGELOG.md](CHANGELOG.md) para mudanças significativas visíveis ao usuário. Para alterações exclusivamente documentais, confira links, comandos, precisão técnica e o diff.

Declare assistência relevante de IA no PR, verifique as alterações e credite trabalhos externos e suas licenças. Envie apenas material que tenha direito de contribuir sob MIT. Não invente autoria, resultados de validação ou permissões de acesso a fontes.

Pull requests são revisados antes do merge. Propostas podem ser recusadas ou adiadas; não há prazo prometido de resposta ou lançamento. Siga o [código de conduta](CODIGO_DE_CONDUTA.md).
