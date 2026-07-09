# Registro de Decisões de Design

Este arquivo centraliza decisões arquiteturais e motivos por trás delas. Cada entrada deve seguir o template abaixo para permitir rastreabilidade.

## Template de Decisão

- ID: DD-YYYY-NNN
- Título: Curto e descritivo
- Data: YYYY-MM-DD
- Autores: Nomes/handles
- Contexto: Situação que exigiu a decisão
- Decisão: O que foi decidido
- Alternativas consideradas: Lista curta
- Impacto: Componentes afetados e migração necessária
- Status: Proposto / Aceito / Rejeitado / Depreciado

## Exemplo

- ID: DD-2026-001
- Título: Persistência de Memória em SQLite
- Data: 2026-07-09
- Autores: Equipe Sentinel
- Contexto: Necessidade de armazenamento simples, local e indexável
- Decisão: Usar SQLite com esquema versionado e interface de abstração
- Alternativas consideradas: Elasticsearch, Faiss
- Impacto: `sentinel.memory`, scripts de migração
- Status: Aceito

---

Registre cada decisão aqui e referencie-a nas PRs e no SDD relevante.
