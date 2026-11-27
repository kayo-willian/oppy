# PSG portal reconnaissance

[Português (Brasil)](../pt-BR/docs/psg-recon.md) · [Home](../README.md)

On 19 November 2026 we sampled the public Senac Pará PSG listing and two Santarém details. Scope includes every course area. Senac is the information source. The fixtures are reduced excerpts, with candidate forms, scripts, contact information and unrelated content excluded. PDF links are metadata only.

## Access

GET /robots.txt returned 404. The listing returned 200 twice. The first response could not be inspected because a local HTML library was unavailable. Both detail GETs returned 200. Requests identified the project and linked to its repository, with a four-second connection timeout, ten-second total timeout, zero automatic retries and no redirects. No assets, forms, PDFs or policy pages were requested.

A local search of listing links and sampled page text found no identifiable terms of use, access policy or polling interval. No explicit conflict with a 30-minute interval was observed. Whether recurring automated access at that interval is permitted remains unresolved. The 404 and successful page loads do not establish permission. Confirm applicable conditions and whether the interval covers detail requests before enabling polling.

## Listing boundaries and identity

Each municipality has its own div.panel.panel-default. Match exactly one direct .panel-heading > h2.panel-title with the normalized text “Santarém”. Read only its panel's direct ul.list-group > li.list-group-item children. Validate each selection anchor against the HTTPS source host and observed Santarém detail path. Deduplicate repeated hrefs inside a row. The fixture retains Ananindeua as a control. Municipal order has no role in this lookup.

The two detail paths end in /santarem/5/948 and /santarem/5/377342740. The listing also exposes the edital labels 152/2026 and 126/2026. Use the source, municipality and opaque selection identifier from the linked path as a provisional key. On active online course actions, data-cidade and data-selecao corroborate the path. Identifier stability over time is unverified.

## Detail fields

| Field | Observed representation and limits |
|---|---|
| Course and status | Each ul.lista-psg-cursos > li contains a .media-body and h3.media-heading. Read the title separately from its small child. Selection 126 was labelled “Inscrições Abertas” yet individual controls said “Inscrever neste curso”, “Inscrições encerradas” or “Vagas preenchidas”. On 152 the disabled control said “Inscrição Presencial”, which by itself gives no closure signal. |
| Modality | The small child says “inscrição online” or “inscrição presencial”. This describes registration. No explicit teaching modality was identified in the sampled course rows. |
| Registration dates | Inline text “Inscrições de … às … até … às …” surrounds separate strong elements with DD/MM/YYYY dates and HH:MM times. No timezone was attached to these values. |
| Course period and venue | “Período do curso: de … até …” gives two dates. “Local do curso:” introduces free text. |
| Requirements | Free text after “Pré-requisito:” varies by course and can combine schooling, age and prior knowledge. The Defesa de Redes text ends mid-word (“lógi”). Preserve uncertainty. |
| Documents | Selection-level list items pair a PDF anchor labelled “Download” with adjacent edital or retificativo text. Record the label and official URL. Document contents and effects on registration were not examined. |

Selection 126 had ten course rows. Three active actions exposed data-curso (3587, 437, 450), data-selecao, data-cidade, data-nome-curso and data-nome-url. Closed or full rows and the in-person row in 152 lacked that course identifier. No stable class identifier was established. Prefer a selection-scoped course ID when present and unique, allowing title edits. Keep the last known ID. For rows without IDs, use venue, course period and title as matching evidence only. Require an unambiguous one-to-one match. A rename with insufficient evidence, reused IDs or indistinguishable same-name classes must remain unresolved. Neither row position nor a title-derived slug resolves identity.

## Failure boundary

Require a successful HTML response, exactly one target panel, a recognizable list and consistent municipality links. Validate the course list and identities per detail. Keep missing optional fields unknown. Treat conflicting links, missing structures, ambiguous matches and empty results without an explicit source indication as failed or partial observations. Preserve the affected last valid state and suppress removal and cancellation events. Absence alone cannot establish removal even after a valid listing. A genuine empty-state marker, class identity across snapshots and changes to the same document URL remain unverified.
