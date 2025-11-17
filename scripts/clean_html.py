#!/usr/bin/env python3
"""
Script para limpiar archivos HTML capturados con SingleFile
Remueve tracking scripts, consolida CSS, y mantiene todo el contenido visible
"""

import re
from bs4 import BeautifulSoup
import os
import sys
from pathlib import Path

def clean_html_file(input_path, output_path):
    """
    Limpia un archivo HTML individual
    """
    print(f"Limpiando: {input_path}")

    # Leer el archivo
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse con BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Remover iframes de tracking
    iframes_removed = 0
    for iframe in soup.find_all('iframe'):
        iframe.decompose()
        iframes_removed += 1

    # 2. Remover atributos no deseados
    unwanted_attrs = [
        'data-evernote-id',
        'data-wf-page',
        'data-wf-site',
        'data-wf-element-id',
        'data-singlefile-element',
        'data-singlefile-removed-hidden-element',
        'data-singlefile-hidden-content'
    ]

    attrs_removed = 0
    for tag in soup.find_all(True):
        for attr in unwanted_attrs:
            if tag.has_attr(attr):
                del tag[attr]
                attrs_removed += 1

    # 3. Remover clase js-evernote-checked
    classes_removed = 0
    for tag in soup.find_all(class_='js-evernote-checked'):
        if 'class' in tag.attrs:
            tag['class'] = [c for c in tag['class'] if c != 'js-evernote-checked']
            if not tag['class']:
                del tag['class']
            classes_removed += 1

    # 4. Consolidar todos los bloques CSS en uno solo
    css_blocks = []
    style_tags = soup.find_all('style')

    for style in style_tags:
        if style.string:
            css_blocks.append(style.string)
        style.decompose()

    # Crear un solo bloque de CSS en el head
    if css_blocks and soup.head:
        consolidated_style = soup.new_tag('style')
        consolidated_style.string = '\n'.join(css_blocks)
        soup.head.insert(0, consolidated_style)

    # 5. Remover comentarios de SingleFile
    comments = soup.find_all(string=lambda text: isinstance(text, type(soup.new_string(''))) and
                                                   text.strip().startswith('<!--'))
    for comment in comments:
        if 'SingleFile' in str(comment) or 'Page saved with' in str(comment):
            comment.extract()

    # Formatear HTML
    cleaned_html = soup.prettify()

    # Guardar archivo limpio
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_html)

    # Estadísticas
    original_size = os.path.getsize(input_path)
    cleaned_size = os.path.getsize(output_path)
    reduction = ((original_size - cleaned_size) / original_size) * 100

    print(f"  ✓ {iframes_removed} iframes removidos")
    print(f"  ✓ {attrs_removed} atributos removidos")
    print(f"  ✓ {classes_removed} clases removidas")
    print(f"  ✓ {len(style_tags)} bloques CSS consolidados en 1")
    print(f"  ✓ Tamaño: {original_size/1024/1024:.2f}MB → {cleaned_size/1024/1024:.2f}MB ({reduction:.1f}% reducción)")
    print(f"  ✓ Guardado en: {output_path}\n")

    return cleaned_size < original_size

def process_batch(input_dir, output_dir):
    """
    Procesa todos los archivos HTML de un directorio
    """
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
    for html_file in html_files:
        # Mantener estructura de subdirectorios
        relative_path = html_file.relative_to(input_path)
        output_file = output_path / relative_path

        # Crear subdirectorios si es necesario
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Limpiar el archivo
        clean_html_file(str(html_file), str(output_file))

    print("="*60)
    print(f"✓ Proceso completado. {len(html_files)} archivos limpiados.")

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

    print("Script de Limpieza de HTML")
    print("="*60)
    print(f"Directorio de entrada: {input_dir}")
    print(f"Directorio de salida:  {output_dir}")
    print("="*60 + "\n")

    process_batch(input_dir, output_dir)
