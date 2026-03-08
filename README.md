# Asset Indexer (Work in Progress)

CLI-first tool for indexing, analyzing and searching large file archives.

This project is an experimental backend tool designed to help manage large collections of files.
It can work with media files, documents, PDFs, spreadsheets and other digital assets.

The goal is to create a simple but powerful indexing system that allows fast inspection and search inside large folders and archives.

The project is currently under active development.

---

## Motivation

When working with large archives or production folders, files quickly become difficult to manage:

* hundreds or thousands of files
* duplicated materials
* inconsistent file naming
* forgotten file locations
* large historical archives

Instead of manually browsing folders, this tool builds an index of files and allows fast inspection of the archive.

---

## Current MVP Direction

The current MVP focuses on:

* scanning large folders and archives
* creating an index of files
* storing file metadata in SQLite
* detecting duplicate files using hashes
* searching files by name and path
* filtering by creation or modification date
* tagging files for easier classification
* providing archive statistics

---

## Architecture

The project follows a layered architecture:

Interface (CLI)
↓
Application Layer
↓
Domain
↓
Storage (SQLite)

This architecture allows replacing the CLI interface with GUI or API in the future without changing the core logic.

---

## Project Structure

The repository is organized using a layered architecture separating domain logic, application services and infrastructure.

```
asset-engine/
│
├── application/
│
├── domain/
│   ├── asset.py
│   ├── hash.py
│   ├── tag.py
│   ├── source.py
│   ├── state.py
│   ├── types.py
│   └── exceptions.py
│
├── interface/
│
├── storage/
│
├── tests/
│   ├── test_asset.py
│   ├── test_state.py
│   └── test_type.py
│
├── main.py
└── README.md
```

## Domain Model (current)

Entity:

* Asset

Value Objects:

* AssetType
* AssetSource
* AssetState
* FileHash
* Tag

Asset fields include:

* filename
* full_path
* size
* created_at
* modified_at
* hash (optional)
* tags

---

## Planned CLI Commands

Examples of commands planned for the CLI interface:

scan archive

search keyword

duplicates

stats

tag add

tag search

---
## Example Use Cases

### Media Production Archives

Video production teams often accumulate thousands of media files across many projects.  
This tool can index the archive and help detect duplicate footage, forgotten assets and inconsistent naming.

### Research and Journalism Archives

Investigative journalism projects often collect large volumes of source material: videos, PDFs, documents and datasets.  
The index allows fast search and inspection across the archive.

### Large Document Collections

Organizations sometimes store thousands of PDFs, spreadsheets and reports across shared folders.  
The tool helps locate duplicates, search by name and analyze archive structure.

### Backup Inspection

Large backup folders may contain many redundant or outdated files.  
By indexing the archive and comparing hashes, the tool can detect duplicate files and provide statistics about stored data.

### General File Archive Management

The architecture is not limited to media files and can work with any file types, making it useful for general archive inspection and search.
## Project Status

Work in progress.

The project is being developed incrementally with small commits that reflect the evolution of the design and architecture.
