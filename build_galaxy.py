import os
import re
import csv
import xml.etree.ElementTree as ET
import bz2file
import mwparserfromhell

# Configuration paths
DUMP_PATH = r"D:\wikipedia_galaxy\enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2"
OUTPUT_VAULT = r"D:\wikipedia_galaxy\vault"
CSV_PATH = r"D:\wikipedia_galaxy\wikipedia_galaxy.csv"

# Optimization: Pre-compile regex for faster text manipulation and filtering
META_PREFIXES = re.compile(r"^(Category|File|Image|Template|Help|Portal|Wikipedia|Draft|MediaWiki):", re.IGNORECASE)

# Ensure output directories exist
os.makedirs(OUTPUT_VAULT, exist_ok=True)

def sanitize_filename(title):
    """Removes characters forbidden by operating systems."""
    return re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")

def get_nested_path(title):
    """Creates a deep A/B/ structure so Windows doesn't choke on thousands of files."""
    clean_title = sanitize_filename(title)
    if not clean_title:
        return None, None
    
    char1 = clean_title[0].upper() if clean_title[0].isalnum() else "_"
    char2 = clean_title[1].upper() if (len(clean_title) > 1 and clean_title[1].isalnum()) else "_"
    
    folder_path = os.path.join(OUTPUT_VAULT, char1, char2)
    return folder_path, f"{clean_title}.md"

print("Initializing Galaxy Map CSV...")
with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Source", "Target"])

    print("Opening Wikipedia Chunk file via bz2file streamer... (Press Ctrl+C to stop)")
    
    count = 0
    csv_buffer = []
    BUFFER_SIZE = 5000  # Flushes more frequently for this smaller sample file
    
    with bz2file.open(DUMP_PATH, "rb") as xml_file:
        # Stream elements sequentially to keep RAM flat
        context = ET.iterparse(xml_file, events=("start", "end"))
        context = iter(context)
        event, root = next(context)
        
        # Local variables to accumulate data inside a <page> node
        title = None
        ns = None
        text = None
        
        for event, elem in context:
            # Strip out any XML namespace prefix entirely (e.g., '{http://...}title' -> 'title')
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            
            if event == "end":
                if tag == "title":
                    title = elem.text
                elif tag == "ns":
                    ns = elem.text
                elif tag == "text":
                    text = elem.text
                
                # Once we hit the closing tag of a page block, process it
                elif tag == "page":
                    if title and ns == "0" and text:
                        # Skip processing heavy lifting for redirect stubs
                        if not text.lower().startswith("#redirect"):
                            
                            # Parse MediaWiki syntax structure
                            wikicode = mwparserfromhell.parse(text)
                            
                            # 1. Isolate outgoing wiki connection links
                            connections = set()
                            for link in wikicode.filter_wikilinks():
                                target = str(link.title).split('#')[0].strip()
                                if target and not META_PREFIXES.match(target):
                                    connections.add(target)
                                    csv_buffer.append([title, target])
                            
                            # 2. Extract clean, plain markdown prose
                            clean_text = wikicode.strip_code()
                            
                            # 3. Safely linkify up to the top 30 keyword references
                            core_links = list(connections)[:30]
                            for conn in core_links:
                                if len(conn) > 3 and conn in clean_text:
                                    escaped_conn = re.escape(conn)
                                    clean_text = re.sub(rf'\b{escaped_conn}\b', f"[[{conn}]]", clean_text)
                            
                            # 4. Save markdown file inside the deep folder matrix
                            folder, filename = get_nested_path(title)
                            if folder:
                                os.makedirs(folder, exist_ok=True)
                                with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
                                    f.write(f"# {title}\n\n")
                                    f.write(clean_text)
                                    
                            count += 1
                            
                            # Keep disk writes efficient via batch operations
                            if len(csv_buffer) >= BUFFER_SIZE:
                                csv_writer.writerows(csv_buffer)
                                csv_buffer.clear()
                                
                            if count % 1000 == 0:
                                print(f"Successfully mapped {count:,} articles in the cosmic web...")
                    
                    # Essential: Clear current page data out of system memory
                    title, ns, text = None, None, None
                    elem.clear()
                    root.clear()
                    
        # Final flush for remaining connections in the memory buffer
        if csv_buffer:
            csv_writer.writerows(csv_buffer)

print(f"\nExtraction Finished! Total items mapped: {count:,}")
print(f"Your Obsidian vault folder is ready at: {OUTPUT_VAULT}")
print(f"Your Galaxy Map graph connection file is ready at: {CSV_PATH}")