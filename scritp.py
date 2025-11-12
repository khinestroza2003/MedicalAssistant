import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import re
from typing import List, Dict, Optional

class WebConsultasScraperLimpio:
    def __init__(self):
        self.base_url = 'https://www.webconsultas.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Palabras a filtrar (navegación, menús, etc)
        self.palabras_basura = [
            'portada', 'noticias', 'leer más', 'también te puede interesar',
            'lo más leído', 'entrevista', 'más info', 'compartir contenido',
            'quiénes somos', 'ajuste de privacidad', 'belleza y bienestar',
            'mente y emociones', 'bebés y niños', 'embarazo', 'ejercicio y deporte',
            'test de psicología', 'métodos anticonceptivos', 'actividades fitness'
        ]
    
    def delay(self, seconds: float = 1.5):
        time.sleep(seconds)
    
    def es_texto_basura(self, texto: str) -> bool:
        """Detecta si el texto es navegación o contenido no relevante"""
        texto_lower = texto.lower()
        
        # Demasiado corto
        if len(texto) < 15:
            return True
        
        # Contiene palabras de navegación
        if any(palabra in texto_lower for palabra in self.palabras_basura):
            return True
        
        # Es un enlace de navegación (empieza con números)
        if re.match(r'^\d+[A-Z]', texto):
            return True
        
        # Contiene muchas mayúsculas seguidas (probablemente un título de sección)
        if re.search(r'[A-Z]{10,}', texto):
            return True
        
        return False
    
    def limpiar_texto(self, texto: str) -> str:
        """Limpia y normaliza texto"""
        if not texto:
            return ""
        # Eliminar espacios múltiples y saltos de línea
        texto = re.sub(r'\s+', ' ', texto)
        # Eliminar puntos suspensivos al final
        texto = re.sub(r'\.{3,}$', '', texto)
        return texto.strip()
    
    def obtener_lista_enfermedades(self) -> List[Dict[str, str]]:
        """Obtiene lista completa de enfermedades del índice principal"""
        print('\n📋 Obteniendo lista completa de enfermedades...')
        
        todas_enfermedades = []
        letras = 'abcdefghijklmnopqrstuvwxyz'
        
        for letra in letras:
            try:
                url = f'{self.base_url}/salud-al-dia/{letra}'
                response = self.session.get(url, timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar enlaces en el contenido principal
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    texto = self.limpiar_texto(link.get_text())
                    
                    # Filtrar solo enlaces de enfermedades
                    if ('/salud-al-dia/' in href and 
                        texto and 
                        not self.es_texto_basura(texto) and
                        len(texto) > 3 and
                        href.count('/') >= 3):  # URLs de enfermedades tienen más niveles
                        
                        url_completa = href if href.startswith('http') else f'{self.base_url}{href}'
                        
                        # Evitar duplicados
                        if not any(e['url'] == url_completa for e in todas_enfermedades):
                            todas_enfermedades.append({
                                'nombre': texto,
                                'url': url_completa
                            })
                
                self.delay(0.5)
                print(f'   {letra.upper()}: {len([e for e in todas_enfermedades if e["nombre"][0].lower() == letra])} enfermedades')
                
            except Exception as e:
                print(f'   Error en letra {letra}: {e}')
                continue
        
        print(f'\n✓ Total encontradas: {len(todas_enfermedades)} enfermedades')
        return todas_enfermedades
    
    def extraer_contenido_limpio(self, soup: BeautifulSoup, tipo: str) -> List[str]:
        """Extrae contenido limpio de listas y párrafos"""
        contenido = []
        
        # Estrategia 1: Buscar listas (ul, ol) - más probable que sean síntomas/causas
        for lista in soup.find_all(['ul', 'ol']):
            # Verificar que la lista está en el contenido principal, no en el menú
            parent = lista.find_parent(['nav', 'header', 'footer', 'aside'])
            if parent:
                continue
            
            for item in lista.find_all('li', recursive=False):
                texto = self.limpiar_texto(item.get_text())
                
                if (texto and 
                    not self.es_texto_basura(texto) and
                    15 < len(texto) < 300):
                    contenido.append(texto)
        
        # Estrategia 2: Si no hay listas suficientes, buscar en párrafos específicos
        if len(contenido) < 3:
            keywords = {
                'sintomas': ['síntoma', 'manifestación', 'signo', 'presenta', 
                            'dolor', 'fiebre', 'inflamación', 'náusea', 'sensación'],
                'causas': ['causa', 'debido', 'provocado', 'origina', 'factor',
                          'desencadena', 'produce', 'consecuencia']
            }
            
            palabras_clave = keywords.get(tipo, keywords['sintomas'])
            
            for p in soup.find_all('p'):
                # Ignorar párrafos en navegación
                parent = p.find_parent(['nav', 'header', 'footer', 'aside'])
                if parent:
                    continue
                
                texto_completo = p.get_text()
                
                # Buscar párrafos relevantes
                if any(keyword in texto_completo.lower() for keyword in palabras_clave):
                    # Dividir en oraciones
                    oraciones = re.split(r'[.;]', texto_completo)
                    for oracion in oraciones:
                        oracion = self.limpiar_texto(oracion)
                        if (oracion and 
                            not self.es_texto_basura(oracion) and
                            20 < len(oracion) < 400):
                            contenido.append(oracion)
        
        # Eliminar duplicados manteniendo orden
        contenido_limpio = []
        for item in contenido:
            if item not in contenido_limpio:
                contenido_limpio.append(item)
        
        return contenido_limpio[:20]  # Máximo 20 items
    
    def extraer_detalles_enfermedad(self, url: str, nombre: str) -> Optional[Dict]:
        """Extrae información detallada de una enfermedad"""
        try:
            print(f'\n   🔍 {nombre}')
            
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Limpiar el nombre (puede venir con texto extra)
            nombre_limpio = nombre.split('\n')[0].strip()
            if len(nombre_limpio) > 35:
                nombre_limpio = nombre_limpio[:35]
            
            enfermedad = {
                'nombre': nombre_limpio,
                'url': url,
                'descripcion': '',
                'sintomas': [],
                'causas': [],
                'tratamiento': []
            }
            
            # Extraer descripción (buscar el primer párrafo significativo en article)
            article = soup.find('article') or soup.find('main')
            if article:
                for p in article.find_all('p', limit=10):
                    # Ignorar párrafos en navegación
                    if p.find_parent(['nav', 'header', 'footer']):
                        continue
                    
                    texto = self.limpiar_texto(p.get_text())
                    if texto and not self.es_texto_basura(texto) and len(texto) > 80:
                        enfermedad['descripcion'] = texto[:400]
                        break
            
            # Buscar páginas específicas de síntomas y causas
            link_sintomas = soup.find('a', href=re.compile(r'sintomas|síntomas', re.I))
            link_causas = soup.find('a', href=re.compile(r'causas', re.I))
            
            # Extraer SÍNTOMAS
            if link_sintomas:
                url_sintomas = link_sintomas.get('href')
                if not url_sintomas.startswith('http'):
                    url_sintomas = f'{self.base_url}{url_sintomas}'
                
                print(f'      → Síntomas: {url_sintomas}')
                self.delay(1)
                
                try:
                    resp = self.session.get(url_sintomas, timeout=15)
                    soup_sintomas = BeautifulSoup(resp.content, 'html.parser')
                    enfermedad['sintomas'] = self.extraer_contenido_limpio(soup_sintomas, 'sintomas')
                except:
                    enfermedad['sintomas'] = self.extraer_contenido_limpio(soup, 'sintomas')
            else:
                enfermedad['sintomas'] = self.extraer_contenido_limpio(soup, 'sintomas')
            
            # Extraer CAUSAS
            if link_causas:
                url_causas = link_causas.get('href')
                if not url_causas.startswith('http'):
                    url_causas = f'{self.base_url}{url_causas}'
                
                print(f'      → Causas: {url_causas}')
                self.delay(1)
                
                try:
                    resp = self.session.get(url_causas, timeout=15)
                    soup_causas = BeautifulSoup(resp.content, 'html.parser')
                    enfermedad['causas'] = self.extraer_contenido_limpio(soup_causas, 'causas')
                except:
                    enfermedad['causas'] = self.extraer_contenido_limpio(soup, 'causas')
            else:
                enfermedad['causas'] = self.extraer_contenido_limpio(soup, 'causas')
            
            # Buscar tratamiento
            link_tratamiento = soup.find('a', href=re.compile(r'tratamiento', re.I))
            if link_tratamiento:
                url_trat = link_tratamiento.get('href')
                if not url_trat.startswith('http'):
                    url_trat = f'{self.base_url}{url_trat}'
                
                self.delay(1)
                try:
                    resp = self.session.get(url_trat, timeout=15)
                    soup_trat = BeautifulSoup(resp.content, 'html.parser')
                    enfermedad['tratamiento'] = self.extraer_contenido_limpio(soup_trat, 'tratamiento')
                except:
                    pass
            
            print(f'      ✓ {len(enfermedad["sintomas"])} síntomas | {len(enfermedad["causas"])} causas')
            
            self.delay(1.5)
            
            # Solo retornar si tiene contenido útil
            if enfermedad['sintomas'] or enfermedad['causas'] or enfermedad['descripcion']:
                return enfermedad
            return None
            
        except Exception as e:
            print(f'      ❌ Error: {e}')
            return None
    
    def guardar_json(self, enfermedades: List[Dict], archivo: str = 'enfermedades_limpio.json'):
        """Guarda en JSON"""
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(enfermedades, f, ensure_ascii=False, indent=2)
        print(f'\n✅ {archivo} - {len(enfermedades)} enfermedades')
    
    def guardar_csv(self, enfermedades: List[Dict], archivo: str = 'enfermedades_limpio.csv'):
        """Guarda en CSV"""
        with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Nombre', 'URL', 'Descripción', 'Síntomas', 'Causas', 'Tratamiento'])
            
            for e in enfermedades:
                writer.writerow([
                    e['nombre'],
                    e['url'],
                    e['descripcion'],
                    ' | '.join(e['sintomas']),
                    ' | '.join(e['causas']),
                    ' | '.join(e.get('tratamiento', []))
                ])
        print(f'✅ {archivo} - {len(enfermedades)} enfermedades')
    
    def ejecutar(self, max_enfermedades: int = None):
        """Ejecuta el scraping"""
        print('='*70)
        print('🚀 SCRAPER WEBCONSULTAS - VERSIÓN LIMPIA')
        print('='*70)
        
        # Obtener lista completa de enfermedades
        lista_enfermedades = self.obtener_lista_enfermedades()
        
        if max_enfermedades:
            lista_enfermedades = lista_enfermedades[:max_enfermedades]
            print(f'\n⚙️  Procesando solo {max_enfermedades} enfermedades...')
        
        todas_las_enfermedades = []
        total = len(lista_enfermedades)
        
        print(f'\n{"="*70}')
        print(f'📊 Extrayendo detalles de {total} enfermedades...')
        print(f'{"="*70}')
        
        for idx, enfermedad in enumerate(lista_enfermedades, 1):
            print(f'\n[{idx}/{total}]', end='')
            
            detalles = self.extraer_detalles_enfermedad(
                enfermedad['url'],
                enfermedad['nombre']
            )
            
            if detalles:
                todas_las_enfermedades.append(detalles)
        
        print(f'\n{"="*70}')
        print(f'✅ COMPLETADO: {len(todas_las_enfermedades)}/{total} enfermedades extraídas')
        print(f'{"="*70}\n')
        
        if todas_las_enfermedades:
            self.guardar_json(todas_las_enfermedades)
            self.guardar_csv(todas_las_enfermedades)
            print(f'\n📂 Archivos guardados con información LIMPIA')
        
        return todas_las_enfermedades


# ==================== EJECUCIÓN ====================

if __name__ == '__main__':
    scraper = WebConsultasScraperLimpio()
    
    print('\n🔧 CONFIGURACIÓN\n')
    print('Opciones:')
    print('  1. Prueba: 10 enfermedades (~10 minutos)')
    print('  2. Media: 50 enfermedades (~45 minutos)')
    print('  3. Completa: TODAS (VARIAS HORAS)\n')
    
    # CAMBIA ESTA CONFIGURACIÓN
    opcion = 3  # Cambiar a 2 o 3
    
    if opcion == 1:
        print('✓ Modo: PRUEBA (10 enfermedades)\n')
        enfermedades = scraper.ejecutar(max_enfermedades=1)
    elif opcion == 2:
        print('✓ Modo: MEDIA (50 enfermedades)\n')
        enfermedades = scraper.ejecutar(max_enfermedades=50)
    else:
        print('✓ Modo: COMPLETA (TODAS las enfermedades)\n')
        print('⚠️  Esto puede tardar VARIAS HORAS\n')
        enfermedades = scraper.ejecutar()
    
    print(f'\n🎉 ¡FINALIZADO! {len(enfermedades)} enfermedades procesadas')
    print(f'📁 Archivos: enfermedades_limpio.json y enfermedades_limpio.csv\n')