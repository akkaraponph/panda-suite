# Substantial engineering documents

Use the project's template first. This section menu is for describing a current
system; designing proposed contracts belongs with a specification workflow.
Keep numbering, revision history, and a table of contents when useful or required
by the established format. Record only known metadata and actual revisions;
an absent owner or version is not an invitation to invent one.

## Select sections by the reader's task

| Section | Questions to answer from evidence |
| --- | --- |
| Purpose and scope | Who uses this document, for what task, within which system boundary? |
| System overview | What are the components, responsibilities, technologies, and external dependencies? |
| Architecture and processing | How does an entry point invoke components, transform data, and reach an outcome? |
| Features | What conditions, validation, permissions, state transitions, and failure paths apply to each feature? |
| Integrations | Which side owns each contract, field transformation, authentication, error, retry, and recovery behavior? |
| Data | Which schemas, migrations, constraints, ownership, lifecycles, and transaction boundaries are implemented? |
| Background work | What registers or schedules jobs, and what establishes retries, idempotency, and failure handling? |
| Configuration and operations | Which keys control behavior, what runtime prerequisites exist, and which deployment procedures are verified? |
| Handover | How can a maintainer run, diagnose, and change this system using verified commands and source anchors? |

Open major sections with their role, then explain processing paths and boundaries.
Use consistent implementation names and inline code for identifiers. Tables suit
comparable facts such as Feature / Code Path and Configuration / Purpose; prose
explains conditions and consequences. Omit irrelevant chapters rather than filling
them with generic statements.

## Evidence and presentation checks

- Trace each integration independently. One client's retries or authentication
  do not establish another client's behavior or a remote service's guarantees.
- Keep code-defined data models separate from observed stored data. A field name
  alone establishes neither a foreign key nor a retention policy.
- Give diagrams a title, purpose, flow direction, components, and relevant
  boundaries. Explain material limits; logical relationships do not establish
  servers, replicas, networks, or deployment topology.
- Preserve supported portions of existing documents. For conflicting claims,
  explain the discrepancy with a source anchor; distinguish a stale description
  from an unresolved requirement or environment question.
- Collect exact unknowns as `Pending Confirmation`, with the needed evidence or
  decision. Keep verified sections useful without guessed facts or invented owners.
- Check paths, symbols, payloads, examples, terminology, headings, and links.
  Separate executed examples from static checks and unavailable runtime evidence.
- Deliver the artifact or review findings plus a brief verification account and
  remaining gaps. Keep investigation narration out of the finished document.
