# Reconhecimento do portal PSG

[English](../../docs/psg-recon.md) · [Início](../README.md)

Em 19 de novembro de 2026, foram examinadas a listagem pública do PSG do Senac Pará e duas páginas de detalhes de Santarém. O escopo abrange cursos de todas as áreas. O Senac é a fonte das informações. As amostras usadas nos testes contêm trechos reduzidos, sem formulários de candidatos, scripts, informações de contato ou conteúdo alheio à coleta. Dos PDFs, foram registrados apenas os metadados dos links.

## Acesso

GET /robots.txt retornou 404. A listagem retornou 200 duas vezes. Não foi possível inspecionar a primeira resposta porque uma biblioteca local de HTML estava indisponível. As duas requisições GET aos detalhes retornaram 200. As requisições identificaram o projeto e incluíram o link do repositório. O limite de conexão foi de quatro segundos e o limite total, dez segundos, sem novas tentativas automáticas ou redirecionamentos. Não houve requisições a recursos da página, formulários, PDFs ou páginas de políticas.

Uma busca local nos links da listagem e no texto das páginas amostradas não identificou termos de uso, política de acesso ou intervalo de consulta. Não foi observado conflito explícito com o intervalo de 30 minutos. A permissão para consultas automatizadas recorrentes nesse intervalo permaneceu em aberto. O 404 e o carregamento bem-sucedido das páginas não estabelecem permissão. Antes de habilitar consultas, confirme as condições aplicáveis e se o intervalo também abrange as requisições aos detalhes.

## Limites da listagem e identificação

Cada município tem um `div.panel.panel-default`. Encontre exatamente um `.panel-heading > h2.panel-title` direto cujo texto normalizado seja “Santarém”. Leia apenas os filhos diretos `ul.list-group > li.list-group-item` dentro desse painel. Valide cada link de seleção em relação ao host HTTPS da fonte e ao caminho observado dos detalhes de Santarém. Elimine hrefs repetidos dentro da mesma linha. A amostra conserva Ananindeua como controle. A ordem dos municípios não interfere na busca.

Os dois caminhos de detalhes terminam em `/santarem/5/948` e `/santarem/5/377342740`. A listagem também mostra os editais 152/2026 e 126/2026. A chave provisória combina fonte, município e identificador opaco da seleção extraído do caminho do link. Nos controles ativos de inscrição online, `data-cidade` e `data-selecao` corroboram o caminho. A estabilidade desses identificadores ao longo do tempo não foi verificada.

## Campos dos detalhes

| Campo | Representação observada e limites |
|---|---|
| Curso e estado | Cada `ul.lista-psg-cursos > li` contém `.media-body` e `h3.media-heading`. Leia o título separadamente do elemento filho `small`. A seleção 126 trazia “Inscrições Abertas”, enquanto os controles dos cursos diziam “Inscrever neste curso”, “Inscrições encerradas” ou “Vagas preenchidas”. Na 152, o controle desabilitado dizia “Inscrição Presencial”, o que por si só não indica encerramento. |
| Modalidade | O elemento `small` diz “inscrição online” ou “inscrição presencial”. Isso descreve a inscrição. Não foi identificada modalidade de ensino explícita nas linhas amostradas. |
| Datas de inscrição | O texto “Inscrições de … às … até … às …” envolve elementos `strong` distintos com datas DD/MM/YYYY e horários HH:MM. Os valores não informavam fuso horário. |
| Período e local do curso | “Período do curso: de … até …” contém duas datas. “Local do curso:” introduz texto livre. |
| Requisitos | O texto após “Pré-requisito:” varia por curso e pode combinar escolaridade, idade e conhecimentos prévios. O texto de Defesa de Redes termina no meio de uma palavra (“lógi”). Preserve a incerteza. |
| Documentos | Itens de lista da seleção associam um link de PDF com rótulo “Download” ao texto adjacente sobre edital ou retificativo. Registre o rótulo e a URL oficial. Não foram examinados o conteúdo dos documentos nem seus efeitos na inscrição. |

A seleção 126 tinha dez linhas de cursos. Três controles ativos expunham `data-curso` (3587, 437, 450), `data-selecao`, `data-cidade`, `data-nome-curso` e `data-nome-url`. As linhas encerradas ou lotadas e a linha presencial da 152 não traziam esse identificador de curso. Não foi estabelecido um identificador estável de turma. Prefira o ID do curso dentro da seleção quando presente e único, admitindo mudanças no título. Guarde o último ID conhecido. Para linhas sem ID, use local, período e título apenas como evidências, exigindo uma correspondência inequívoca de um para um. Renomeações com evidência insuficiente, IDs reutilizados ou turmas homônimas indistinguíveis devem ficar sem resolução. Nem a posição da linha nem um identificador derivado do título resolvem a identidade.

## Condições de falha

Exija uma resposta HTML bem-sucedida, exatamente um painel de destino, uma lista reconhecível e links consistentes com o município. Valide a lista de cursos e as identidades em cada página de detalhes. Mantenha como desconhecidos os campos opcionais ausentes. Links conflitantes, estruturas ausentes, associações ambíguas e resultados vazios sem indicação explícita da fonte representam observações com falha ou parciais. Preserve o último estado válido afetado e suprima eventos de remoção ou cancelamento. A ausência, mesmo após uma listagem válida, não comprova remoção. Permaneceram sem verificação um marcador genuíno de lista vazia, a identidade de turmas entre capturas e alterações em documentos que mantêm a URL.
