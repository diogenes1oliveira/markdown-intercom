#!/usr/bin/env python3
"""Generate MkDocs nav structure from all .md files in docs/"""
import yaml
from pathlib import Path
from collections import defaultdict


def build_nav(docs_dir='docs'):
    """Build hierarchical nav structure from all .md files"""
    nav = []
    files_by_dir = defaultdict(list)
    
    # Collect all .md files, excluding drafts
    for md_file in sorted(Path(docs_dir).rglob('*.md')):
        if 'drafts' in str(md_file):
            continue
        rel_path = md_file.relative_to(docs_dir)
        rel_str = str(rel_path).replace('\\', '/')
        name = md_file.stem.replace('_', ' ').replace('=', ' ').title()
        # Clean up names
        name = name.replace('Devindex', 'Index').replace('Slipups', 'SLIPUPs')
        dir_path = rel_path.parent
        files_by_dir[dir_path].append((rel_str, name, md_file))
    
    # Build nav recursively
    def build_dir_nav(dir_path, prefix=''):
        items = files_by_dir.get(dir_path, [])
        if not items:
            return None
        
        # Sort: README first, then devindex, then alphabetical
        def sort_key(item):
            rel_str, name, _ = item
            if 'README' in rel_str:
                return (0, rel_str)
            elif 'devindex' in rel_str:
                return (1, rel_str)
            else:
                return (2, rel_str)
        
        items.sort(key=sort_key)
        
        nav_items = []
        for rel_str, name, _ in items:
            nav_items.append({name: rel_str})
        
        return nav_items
    
    # Top-level files
    root_files = build_dir_nav(Path('.'))
    if root_files:
        nav.extend(root_files)
    
    # Examples section
    examples_nav = []
    examples_dir = Path('examples')
    if examples_dir in files_by_dir:
        examples_files = build_dir_nav(examples_dir)
        if examples_files:
            examples_nav.extend(examples_files)
    
    # Subdirectories under examples
    for subdir in sorted(files_by_dir.keys()):
        if subdir == Path('.') or not str(subdir).startswith('examples/'):
            continue
        
        parts = subdir.parts
        if len(parts) == 1:  # examples/ itself
            continue
        
        # Build nested structure
        current = examples_nav
        for i, part in enumerate(parts[1:], 1):  # Skip 'examples'
            parent_path = Path('examples') / Path(*parts[1:i])
            dir_name = part.replace('=', ' ').replace('_', ' ').title()
            
            # Find or create section
            section = None
            for item in current:
                if isinstance(item, dict) and dir_name in item:
                    section = item[dir_name]
                    break
            
            if section is None:
                section = []
                current.append({dir_name: section})
            
            # Add files for this directory
            dir_files = build_dir_nav(subdir)
            if dir_files:
                section.extend(dir_files)
    
    if examples_nav:
        nav.append({'Examples': examples_nav})
    
    return nav


if __name__ == '__main__':
    nav = build_nav()
    print(yaml.dump({'nav': nav}, default_flow_style=False, sort_keys=False, allow_unicode=True))
