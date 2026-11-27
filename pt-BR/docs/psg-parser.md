# Interpretação offline das páginas do PSG

[English](../../docs/psg-parser.md) · [Início](../README.md)

Passe o HTML decodificado da listagem a `parse_listing`. Em seguida, forneça a `parse_detail(markup, selection)` uma seleção devolvida pela primeira função e o HTML dos seus detalhes. Ambas devolvem um estado e um motivo. Apenas OK contém registros. A ausência do painel de Santarém em uma listagem reconhecível ou uma lista vazia sem confirmação gera INCONCLUSIVE. Estrutura malformada, links conflitantes e metadados contraditórios da seleção geram FAILED. Em ambos os casos, preserve a última captura válida.

Assume-se America/Santarem para horários de inscrição sem deslocamento de fuso. O período do curso usa datas do calendário local. O canal de inscrição descreve como se inscrever. Um controle de inscrição presencial deixa o estado desconhecido. Nas amostras de teste, o marcador de local omitido representa um local desconhecido. Os documentos da seleção são registrados uma vez por página de detalhes.

Para associar cursos entre duas capturas, siga esta ordem. Cada associação reserva as duas observações envolvidas. Verifique a unicidade nas capturas completas para que uma associação anterior não faça uma duplicata parecer única.

1. Associe o identificador alternativo do curso (`data-curso`) dentro da seleção quando ele ocorrer exatamente uma vez de cada lado. Isso permite identificar um curso cujo título ou local mudou.
2. Associe a combinação de seleção, título normalizado sem distinção entre maiúsculas e minúsculas e local conhecido quando ela for única em cada lado. Datas de curso ausentes ou corrigidas não afetam essa associação.
3. Se a combinação se repetir em algum dos lados, use o período completo do curso (datas de início e término) para distinguir as turmas. O mesmo período deve identificar exatamente uma turma do grupo em cada lado.

Identificadores alternativos conhecidos e conflitantes impedem uma associação pelos demais critérios. Falta de evidência ou ambiguidade restante gera `unresolved`. Cada associação referencia a observação anterior por índice. A posição da linha não serve como evidência. Nenhum resultado gera remoção ou cancelamento.

Os hashes e as comparações de campos usam a mesma captura canônica, com Unicode NFC, espaços em branco consecutivos reduzidos, datas e horários ISO e ordem determinística das coleções. A comparação devolve os valores canônicos anterior e atual para cada campo de primeiro nível que mudou. Compare individualmente os cursos associados para identificar mudanças no curso.
