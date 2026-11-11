# 🌌 Wikipedia Galaxy

> **Turn raw Wikipedia dumps into a local, interconnected Obsidian 3D Knowledge Universe.**

![Wikipedia Galaxy Preview](assets/galaxy_preview.jpg)

**Wikipedia Galaxy** is an open-source data pipeline that transforms raw Wikimedia XML dumps (`.xml.bz2`) into a structured, hyperlinked offline Obsidian vault and a graph network ready for 3D exploration.

---

## ⚡ Features

- **🚀 Memory-Flat XML Streaming:** Streams gigabyte-scale `.xml.bz2` Wikipedia dumps using `iterparse` and `bz2file`. Memory stays flat regardless of dump size.
- **🔗 Automatic `[[Wikilinks]]` Extraction:** Parses MediaWiki syntax via `mwparserfromhell`, extracts outgoing links, and linkifies core keyword occurrences into native Obsidian backlink syntax.
- **📂 NTFS-Safe Deep Tree:** Partitions thousands of articles into structured alphabet matrices (`A/B/Article.md`) to prevent Windows NTFS and Linux ext4 from choking on single-directory file limits.
- **🗺️ Gephi & Graph CSV Export:** Generates clean `Source, Target` connection pairs (`wikipedia_galaxy.csv`) ready for Gephi, Cosmograph, or network analysis engines.
- **🎨 Pre-Tuned Nebula Graph Preset:** Bundles a pre-configured `graph.json` with domain color groups (Physics, AI, Military, History, Biology) for Obsidian's Graph View.

---

## 📦 Requirements

```bash
pip install -r requirements.txt
```

- Python 3.9+
- `bz2file`
- `mwparserfromhell`
- [Obsidian](https://obsidian.md/) (for local graph visualization)

---

## 🚀 Quickstart

### 1. Download a Wikipedia Dump Chunk
Download any Wikimedia multistream article chunk (e.g. from [Wikimedia Dumps](https://dumps.wikimedia.org/enwiki/latest/)):

```bash
# Example chunk:
# enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2
```

### 2. Configure Paths
Open `build_galaxy.py` and set your input/output paths:

```python
DUMP_PATH = "path/to/your/enwiki-dump.xml.bz2"
OUTPUT_VAULT = "./vault"
CSV_PATH = "./wikipedia_galaxy.csv"
```

### 3. Build the Cosmic Web
Run the streaming extractor:

```bash
python build_galaxy.py
```

### 4. Open in Obsidian
1. Open Obsidian and select **"Open folder as vault"** -> choose `./vault`.
2. Copy `templates/graph.json` into `./vault/.obsidian/graph.json` to activate the **Nebula Color Preset**.
3. Press `Ctrl + G` to open the **Graph View** and explore your offline Wikipedia universe!

---

## 🎨 Nebula Color Palette Preset

| Domain | Color | Hex |
| :--- | :--- | :--- |
| **Physics & Space** | Electric Cyan | `#00e5ff` |
| **Military & Ships** | Crimson Red | `#ff1744` |
| **History & Years** | Deep Amber | `#ffc400` |
| **AI & Technology** | Neon Green | `#00e676` |
| **Biology & Medicine** | Neon Violet | `#d500f9` |
| **Mathematics & Logic** | Electric Indigo | `#3d5afe` |
| **Arts & Culture** | Rose Pink | `#ff4081` |
| **General Reference** | Silver Mint | `#64ffda` |

---

## 📜 License

MIT License. Free to use, fork, and gift to the world.

*"Nammalukku uthavaathathu mathavangaluku uthavatum."* — **OpenSource Aandavar** 🚀
