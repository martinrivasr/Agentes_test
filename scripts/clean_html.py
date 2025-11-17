#!/usr/bin/env python3
"""
Script para limpiar archivos HTML capturados con SingleFile
MANTIENE la renderización exacta, SOLO remueve tracking y comentarios
"""

import re
from bs4 import BeautifulSoup, Comment
import os
import sys
from pathlib import Path

def clean_html_file(input_path, output_path):
    """
    Limpia un archivo HTML individual SIN romper la renderización
    """
    print(f"Limpiando: {input_path}")

    # Leer el archivo
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse con BeautifulSoup - IMPORTANTE: usar 'html.parser' para mantener estructura
    soup = BeautifulSoup(html_content, 'html.parser')

    stats = {
        'iframes': 0,
        'comments': 0,
        'canonical_links': 0,
        'meta_tags': 0
    }

    # 1. Remover SOLO comentarios de SingleFile
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment_text = str(comment).strip()
        # Solo remover comentarios de SingleFile
        if 'SingleFile' in comment_text or 'Page saved with' in comment_text or 'saved date:' in comment_text:
            comment.extract()
            stats['comments'] += 1

    # 2. Remover iframes de tracking (HubSpot, Evernote, etc.)
    for iframe in soup.find_all('iframe'):
        iframe.decompose()
        stats['iframes'] += 1

    # 3. Remover/actualizar links canónicos externos
    for link in soup.find_all('link', rel='canonical'):
        href = link.get('href', '')
        if href.startswith('http'):
            link.decompose()
            stats['canonical_links'] += 1

    # 4. Remover meta tags con URLs canónicas externas
    for meta in soup.find_all('meta'):
        if meta.get('name') == 'canonical' or meta.get('property') == 'og:url':
            content = meta.get('content', '')
            if content.startswith('http'):
                meta.decompose()
                stats['meta_tags'] += 1

    # 5. IMPORTANTE: NO usar prettify() - usar str() para mantener formato original
    # str(soup) mantiene la estructura HTML sin reformatear
    cleaned_html = str(soup)

    # Guardar archivo limpio
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_html)

    # Estadísticas
    original_size = os.path.getsize(input_path)
    cleaned_size = os.path.getsize(output_path)
    reduction = ((original_size - cleaned_size) / original_size) * 100 if original_size > 0 else 0

    print(f"  ✓ {stats['iframes']} iframes removidos")
    print(f"  ✓ {stats['comments']} comentarios SingleFile removidos")
    print(f"  ✓ {stats['canonical_links']} links canónicos removidos")
    print(f"  ✓ {stats['meta_tags']} meta tags externos removidos")
    print(f"  ✓ Tamaño: {original_size/1024/1024:.2f}MB → {cleaned_size/1024/1024:.2f}MB ({reduction:.1f}% reducción)")
    print(f"  ✓ Guardado en: {output_path}\n")

    return cleaned_size < original_size

def process_batch(input_dir, output_dir):
    """
    Procesa todos los archivos HTML de un directorio
    """
    import shutil

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Crear directorio de salida si no existe
    output_path.mkdir(parents=True, exist_ok=True)

    # Encontrar todos los archivos HTML
    html_files = list(input_path.glob('**/*.html'))

    if not html_files:
        print(f"No se encontraron archivos HTML en: {input_dir}")
        return

    print(f"Encontrados {len(html_files)} archivos HTML\n")
    print("="*60)

    # Procesar cada archivo
    files_copied = 0
    for html_file in html_files:
        # Mantener estructura de subdirectorios
        relative_path = html_file.relative_to(input_path)
        output_file = output_path / relative_path

        # Crear subdirectorios si es necesario
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Limpiar el archivo
        clean_html_file(str(html_file), str(output_file))

        # Copiar carpeta de archivos externos si existe (ej: pagina_files/)
        # Esto es para páginas guardadas con "Save Complete Webpage"
        external_folder_name = html_file.stem + '_files'
        external_folder = html_file.parent / external_folder_name

        if external_folder.exists() and external_folder.is_dir():
            output_external_folder = output_path / external_folder_name
            if output_external_folder.exists():
                shutil.rmtree(output_external_folder)
            shutil.copytree(external_folder, output_external_folder)
            print(f"  ✓ Copiada carpeta de archivos externos: {external_folder_name}")
            files_copied += 1

    print("="*60)
    print(f"✓ Proceso completado. {len(html_files)} archivos limpiados.")
    if files_copied > 0:
        print(f"✓ {files_copied} carpetas de archivos externos copiadas.")

if __name__ == "__main__":
    # Directorios por defecto
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    input_dir = repo_root / "original"
    output_dir = repo_root / "clean"

    # Permitir argumentos personalizados
    if len(sys.argv) > 1:
        input_dir = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])

    print("Script de Limpieza de HTML (PRESERVA RENDERIZACIÓN)")
    print("="*60)
    print(f"Directorio de entrada: {input_dir}")
    print(f"Directorio de salida:  {output_dir}")
    print("="*60 + "\n")

    process_batch(input_dir, output_dir)
