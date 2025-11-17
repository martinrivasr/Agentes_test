#!/usr/bin/env python3
"""
Script para actualizar links internos en páginas HTML limpias
Asegura que todos los enlaces entre páginas funcionen correctamente
"""

from bs4 import BeautifulSoup
from pathlib import Path
import sys
import urllib.parse

def is_internal_link(href):
    """
    Determina si un link es interno (relativo o del mismo dominio)
    """
    if not href:
        return False

    # Links que empiezan con #, /, ./ o ../ son internos
    if href.startswith('#') or href.startswith('./') or href.startswith('../'):
        return True

    # Links sin protocolo (http/https) son considerados internos
    if not href.startswith('http://') and not href.startswith('https://'):
        # Si termina en .html, .htm o no tiene extensión, es interno
        if href.endswith('.html') or href.endswith('.htm') or '.' not in href.split('/')[-1]:
            return True

    return False

def update_links_in_file(file_path, base_dir):
    """
    Actualiza todos los links internos en un archivo HTML
    """
    print(f"Actualizando links en: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    links_updated = 0

    # Actualizar tags <a href="">
    for tag in soup.find_all('a', href=True):
        href = tag['href']

        if is_internal_link(href):
            # Decodificar URL encoding
            decoded_href = urllib.parse.unquote(href)

            # Si el link apunta a /original/, cambiarlo a /clean/
            if '/original/' in decoded_href:
                tag['href'] = decoded_href.replace('/original/', '/clean/')
                links_updated += 1
            # Si es un link relativo sin carpeta, añadir referencia correcta
            elif decoded_href.endswith('.html') and '/' not in decoded_href:
                # El link está en la misma carpeta
                tag['href'] = decoded_href
            # Si es un link absoluto del tipo /page.html
            elif decoded_href.startswith('/') and decoded_href.endswith('.html'):
                # Convertir a relativo
                tag['href'] = '.' + decoded_href
                links_updated += 1

    # Actualizar tags <link href=""> (CSS, icons, etc.)
    for tag in soup.find_all('link', href=True):
        href = tag['href']

        if is_internal_link(href):
            decoded_href = urllib.parse.unquote(href)

            if '/original/' in decoded_href:
                tag['href'] = decoded_href.replace('/original/', '/clean/')
                links_updated += 1

    # Actualizar tags <script src="">
    for tag in soup.find_all('script', src=True):
        src = tag['src']

        if is_internal_link(src):
            decoded_src = urllib.parse.unquote(src)

            if '/original/' in decoded_src:
                tag['src'] = decoded_src.replace('/original/', '/clean/')
                links_updated += 1

    # Guardar archivo actualizado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    if links_updated > 0:
        print(f"  ✓ {links_updated} links actualizados\n")
    else:
        print(f"  • Sin cambios necesarios\n")

    return links_updated

def process_directory(directory):
    """
    Procesa todos los archivos HTML en un directorio
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Error: El directorio {directory} no existe")
        return

    html_files = list(dir_path.glob('**/*.html'))

    if not html_files:
        print(f"No se encontraron archivos HTML en: {directory}")
        return

    print(f"Encontrados {len(html_files)} archivos HTML\n")
    print("="*60)

    total_links = 0
    for html_file in html_files:
        links = update_links_in_file(html_file, dir_path)
        total_links += links

    print("="*60)
    print(f"✓ Proceso completado. {total_links} links totales actualizados.")

if __name__ == "__main__":
    # Directorio por defecto: /clean/
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    clean_dir = repo_root / "clean"

    # Permitir argumento personalizado
    if len(sys.argv) > 1:
        clean_dir = Path(sys.argv[1])

    print("Script de Actualización de Links")
    print("="*60)
    print(f"Directorio: {clean_dir}")
    print("="*60 + "\n")

    process_directory(clean_dir)
