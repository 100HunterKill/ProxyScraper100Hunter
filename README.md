# ProxyScraper100Hunter

**ProxyScraper100Hunter** es una herramienta para recolectar y verificar proxies desde diversas fuentes en línea. Está diseñada para trabajar con diferentes protocolos de proxy y permite validar la funcionalidad de los proxies recolectados.

## Características

- **Protocolos Soportados**: `http`, `socks4`, `socks5`.
- **Fuentes de Proxies**: Recolecta proxies desde múltiples fuentes.
- **Verificación de Proxies**: Verifica si los proxies están funcionando correctamente.

## Instalación

### Requisitos

Asegúrate de tener [Python 3.8+](https://www.python.org/downloads/) y [pip](https://pip.pypa.io/en/stable/) instalados en tu sistema.

### Clonar el Repositorio

Primero, clona el repositorio desde GitHub:

git clone git@github.com:100HunterKill/ProxyScraper100Hunter.git
cd ProxyScraper100Hunter

### Instalar Dependencias

Instala las dependencias requeridas usando pip:

bash

pip install -r requirements.txt

### Uso
Ejecutar el Scraper

Para recolectar proxies de un protocolo específico, usa el siguiente comando:

bash

python3 run.py -p <protocol>

Donde <protocol> puede ser http, socks4, o socks5.

Ejemplo: Para recolectar proxies SOCKS5:

bash

python3 run.py -p socks5

### Archivos Generados

    proxies-<protocol>.txt: Contiene la lista de proxies recolectados.
    list-<protocol>.txt: Contiene la lista de proxies verificados.

### Verificar Proxies

El proceso de verificación se realiza automáticamente después de la recolección de proxies. Si deseas realizar la verificación por separado, asegúrate de ejecutar el script de verificación adecuado.
Scripts

    proxy_scraper.py: Script principal para recolectar proxies desde varias fuentes.
    proxy_checker.py: Script para verificar la funcionalidad de los proxies recolectados.

### Ejemplo de Uso de proxy_checker.py

Para verificar los proxies guardados en un archivo, usa el siguiente comando:

bash

python3 proxy_checker.py -p <protocol> -l proxies-<protocol>.txt -o list-<protocol>.txt -v

Donde <protocol> es el mismo protocolo utilizado durante la recolección.


### Contribución

¡Las contribuciones son bienvenidas! Si tienes sugerencias, mejoras, o encuentras problemas, por favor crea un issue o un pull request en el repositorio.
Cómo Contribuir

    Hacer un Fork: Realiza un fork del repositorio.
    Crear una Rama: Crea una nueva rama para tu característica o corrección de error.
    Hacer Commit y Push: Realiza cambios, haz commit y push a tu rama.
    Crear un Pull Request: Abre un pull request desde tu rama a la rama principal del repositorio.

### Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
Contacto

Para cualquier consulta o pregunta, puedes contactar al autor en 100hunterdream@gmail.com.

¡Gracias por usar ProxyScraper100Hunter!


Este `README.md` cubre los aspectos clave del proyecto y proporciona instrucciones claras sobre cómo usar y contribuir al repositorio. Puedes ajustar o agregar más detalles según lo necesites.
