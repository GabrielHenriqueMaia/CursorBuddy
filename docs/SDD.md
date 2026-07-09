# Software Design Document (SDD) — Project Sentinel

Este documento fornece a visão de alto nível e os detalhes técnicos para a evolução do Project Sentinel. Use este SDD como fonte única de verdade para decisões arquiteturais, diagramas, componentes e requisitos não-funcionais.

## 1. Visão Geral

- Escopo: Descrever componentes principais, integrações e limites do sistema.
- Objetivos: Manter coerência arquitetural, facilitar decisões e onboarding.

## 2. Contexto e Requisitos

- Requisitos Funcionais (RF)
  - RF1: Capturar estado do desktop (screenshots, UI elements, cursor)
  - RF2: Processar contexto com LLMs agnósticos
  - RF3: Gerar e executar planos de ação

- Requisitos Não-Funcionais (RNF)
  - RNF1: Observabilidade (logs estruturados)
  - RNF2: Testabilidade (módulos mockáveis)
  - RNF3: Performance e uso de recursos

## 3. Visão Arquitetural

- Descrição do Loop Agêntico em 6 fases (Percepção → Contexto → Planejamento → Execução → Reflexão → Memória).
- Diagrama de componentes (colocar diagramas mermaid conforme necessário).

## 4. Componentes Principais

- `sentinel.core` — Tipos, abstrações e orquestrador `AgenticLoop`.
- `sentinel.modules` — Implementações por fase (perception, context, planning, execution, reflection, memory).
- `sentinel.llm` — Abstração de providers (OpenAI, Ollama, Claude, Gemini, custom).

## 5. Interfaces e Contratos

- Assinar os tipos de entrada/saída em `sentinel.core.types`.
- Definir contratos async: cada módulo expõe `async def process(self, data) -> ...`.

## 6. Dados e Modelo de Persistência

- Estrutura de `MemoryEntry` armazenada em SQLite (ou outro motor que se desejar trocar).

## 7. Design de Falhas e Resiliência

- Estratégias de retry, circuit-breaker e isolamento de módulos

## 8. Segurança e Privacidade

- Tratar dados sensíveis com cuidado — evitar enviar screenshots a serviços remotos sem consentimento.

## 9. Plano de Migração / Adoção

1. Adotar templates de SDD para novas features.
2. Registrar decisões no `docs/DESIGN_DECISIONS.md`.
3. Revisar SDD em cada grande PR.

## 10. Glossário

- SDD: Software Design Document
- LLM: Large Language Model

---
_Use este arquivo como base; inclua links para designs específicos por feature (ex: `docs/sdd/perception.md`)._
