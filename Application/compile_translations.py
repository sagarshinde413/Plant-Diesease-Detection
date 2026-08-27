#!/usr/bin/env python
"""Compile translation files for the application"""
import os
import subprocess

def compile_translations():
    """Compile .po files to .mo files"""
    translations_dir = 'translations'
    
    for lang in ['hi', 'mr']:
        po_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
        mo_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.mo')
        
        if os.path.exists(po_file):
            print(f"Compiling {lang} translations...")
            try:
                # Use pybabel to compile
                cmd = f'pybabel compile -f -i {po_file} -o {mo_file}'
                subprocess.run(cmd, shell=True, check=True)
                print(f"✓ Compiled {lang} successfully")
            except Exception as e:
                print(f"✗ Error compiling {lang}: {e}")
        else:
            print(f"✗ Translation file not found: {po_file}")

if __name__ == '__main__':
    compile_translations()
