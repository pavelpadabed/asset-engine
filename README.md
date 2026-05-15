# Asset Engine

Backend-oriented asset indexing and occurrence tracking engine for large filesystem archives.

Asset Engine is an experimental Python backend project focused on filesystem scanning, indexing pipelines, occurrence-aware storage modeling and archive analysis.

The system is designed to inspect large file collections, detect duplicates, build searchable indexes and model physical file occurrences independently from logical asset identity.

The project focuses on backend architecture, repository abstractions, indexing pipelines and scalable filesystem modeling rather than simple file utility scripting.

---

# Motivation

Large archives quickly become difficult to manage:

- duplicated files
- inconsistent folder structures
- forgotten file locations
- historical archives accumulated over years
- repeated scans of the same folders
- lack of searchable indexing

Instead of manually browsing directories, Asset Engine builds an indexed representation of the filesystem and provides analysis and search capabilities over the archive.

---

# Current MVP Direction

The current MVP focuses on:

- scanning large filesystem archives
- building occurrence-aware indexes
- storing normalized metadata in SQLite
- duplicate detection using file hashes
- occurrence-based search pipelines
- scan session tracking
- archive statistics and inspection
- modular CLI orchestration
- repository-driven storage architecture

---

# Core Architectural Idea

The project separates:

- logical asset identity
- physical filesystem occurrence

This allows the system to model:

- multiple copies of the same asset
- repeated scan sessions
- historical archive evolution
- occurrence-aware duplicate analysis

---

# Domain Model

## Asset

Represents the logical identity of a file.

Asset identity is hash-based.

The Asset entity does not store physical filesystem location.

---

## Occurrence

Represents a physical file instance inside the filesystem.

Occurrence stores:

- path
- file_size
- modified_time
- scan_id

Multiple occurrences may reference the same logical asset.

---

## Scan Session

Each scan execution generates a single `scan_id`.

All occurrences created during the same scan share this identifier.

This allows future implementation of:

- historical scan comparison
- archive evolution analysis
- incremental indexing
- scan reporting

---

# Architecture

The project follows a layered backend architecture:


CLI / Interface
        ↓
Application Layer
        ↓
Domain
        ↓
Storage Layer (SQLite)

## Current Architecture Components

Composition Root

CLI Orchestrators

Application Services

Repository Design

Search Pipeline

Duplicate Detection

## Project Structure

```text
asset-engine/
│
├── application/
│   ├── components/
│   ├── criteria/
│   ├── dto/
│   ├── services/
│   └── __init__.py
│
├── docs/
│   └── architecture.md
│
├── domain/
│   ├── factories/
│   ├── asset.py
│   ├── occurrence.py
│   ├── metadata.py
│   ├── hash.py
│   ├── source.py
│   ├── state.py
│   ├── tag.py
│   ├── types.py
│   ├── exceptions.py
│   └── __init__.py
│
├── interface/
│   └── cli/
│       └── __init__.py
│
├── storage/
│   ├── mappers/
│   ├── repositories/
│   ├── sqlite/
│   ├── types/
│   └── __init__.py
│
├── tests/
│
├── utils/
│
├── main.py
├── README.md
├── .gitignore
└── assets.db
```

### Composition Root

`main.py`

Responsible only for system wiring:

- repositories
- services
- CLI commands

No business logic is placed inside the composition root.

---

### CLI Orchestrators

CLI commands act as use-case orchestrators.

Examples:

- scan
- search
- duplicates

Orchestrators coordinate services and user interaction flow.

---

### Application Services

Examples:

- `ScanService`
- `IndexService`
- `SearchService`
- `DuplicateService`
- `DeleteService`

Services remain isolated and responsibility-focused.

---

## Repository Design

The project uses repository abstractions to isolate storage implementation details.

Current implementation:

- SQLite repository

The repository layer currently supports:

- asset persistence
- occurrence persistence
- occurrence iteration
- occurrence-aware searching
- duplicate analysis flows

---

## Search Pipeline

The search system operates on filesystem occurrences rather than logical assets.

Current search capabilities include:

- filename search
- path search
- extension filtering
- modification date filtering

The architecture is designed for future extensibility.

---

## Duplicate Detection

Duplicate detection is hash-based.

The system separates:

- duplicate analysis
- deletion operations

Duplicate discovery is handled by `DuplicateService`.

Deletion operations are delegated to `DeleteService`.

This separation keeps analysis and filesystem mutation independent.

## Engineering Concepts Demonstrated

The project currently demonstrates:

- layered backend architecture
- repository pattern
- DTO pipelines
- orchestration layer design
- occurrence modeling
- normalized storage architecture
- scan session semantics
- contract-driven development
- test-driven refactoring
- filesystem indexing pipelines

---

## Example Use Cases

### Media Production Archives

Indexing large collections of footage, project exports and production assets.

Possible workflows:

- duplicate detection
- archive inspection
- forgotten footage discovery
- production archive indexing

---

### Research / Journalism Archives

Investigative projects often accumulate:

- videos
- PDFs
- screenshots
- datasets
- exported documents

Asset Engine can provide searchable archive indexing and duplicate inspection.

---

### Large Historical Archives

Long-term storage folders often contain repeated or outdated copies of files accumulated over years.

Occurrence-aware indexing enables deeper archive analysis.

---

## Future Directions

Planned future exploration areas:

- processor-based pipeline architecture
- advanced presenter / CLI UX
- scan reporting
- tag normalization
- occurrence history analysis
- AI-assisted metadata processors
- semantic indexing pipelines

---

## Project Status

Work in progress.

The project evolves incrementally through architecture-focused refactoring and small isolated commits.

Current focus:

- CLI orchestration
- presenter UX
- duplicate cleanup flow
- occurrence-aware workflows