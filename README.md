# Aplicación de Operaciones Criptográficas Básicas

Esta aplicación permite realizar operaciones criptográficas básicas como generar una CA (Autoridad Certificadora), emitir certificados y validar certificados. Está construida con FastAPI y utiliza criptografía asimétrica.

## Requisitos

- Python 3.8 o superior
- pip (el gestor de paquetes de Python)
- Git (para clonar el repositorio)

## Instalación

1. Clona este repositorio:

   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_DIRECTORIO>


2. Instala las dependencias necesarias:
    ```sh
    pip install -r requirements.txt

3. Inicia el servidor FastAPI:
    ```sh
    uvicorn main:app --reload
    

## Uso

### Paso 1: Generar la CA (Autoridad Certificadora)


Para generar la CA, ejecuta el siguiente comando curl:

    
    curl --location --request POST 'http://localhost:8000/crypto/ca' \
    --header 'X-API-Key: 9ddaa525-bfc2-4f74-92e0-43b7a028aee1' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "common_name": "MyCA"
    }'

### Paso 2: Emitir un Certificado
#### 2.1: Generar un CSR (Certificate Signing Request)
Primero, ejecuta el script csr.py para generar un CSR que se guarda en un archivo csr.json:


    python csr.py

Este script generará un archivo csr.json con el siguiente contenido (ejemplo):

    
    {
        "csr": "-----BEGIN CERTIFICATE REQUEST-----\nMIICvDCCAaQCAQAwZjELMAkGA1UEBhMCVVMxEzARBgNVBAgMCkNhbGlmb3JuaWEx\nFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xEzARBgNVBAoMCk15IENvbXBhbnkxFTAT\nBgNVBAMMDG15ZG9tYWluLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC\nggEBALv6iF74dsq0Gv6jWFCnKGoYkvfQDEBc06tT7q9EtPJVe0lRtM17ZDgwVviX\n5/lD2w2Lj+lzN5g12Nethh046PXrctv2/+uzz/oQ/znecxs6RPNv4pnbsHIFyUzd\nY52xjynN76sIbnROVs54PNo2X2oEULyLSUEYuIpCagf0Vb7CCxKhn0za0fki4Ps/\nADbVDNL7HCXa+9aXsVzw2F281WflUqqLI90089DSKPa1KD4QFKoZijEAzqCtHwHm\ndEl8Eu0waQxN2flUYQ9PVBRZ84R4SjOruUzIWY3M+wnp8bMFTj8+rn83kM9qGGy5\nGOioZN3AidTrAb0OR58+PIu+4qECAwEAAaARMA8GCSqGSIb3DQEJDjECMAAwDQYJ\nKoZIhvcNAQELBQADggEBAD4/1TAlZrIiYNheUpTo/4B/ZPCIPCR7rA8nkHKxl3+x\n/XacDCc8ULugFjHE1Qz50xMT1EtRvekK6sGLiU0jeGGwrPPenOiVOSL1ATL7nAEk\niV0taZmm4ixJRaODU4eFo9O8GD2CI5QMkfJ3UjU6mHGx0/UgGp7O8oeiKVLxXSRM\nmAJgs3jvoFPgqpxPs6jHDlvp9Fi+mBJTc866SGPsXpDG0jkOUOWkQ+O/Z3XHDX/9\nmIsUS6X4MtZERAmYeZX4dIcFCzoksremU05fnYgQyGlGu8Us5Jc0QBnHXttrl/hR\nZirpejpkzQXa7FpP1fymjnKO0kP8BaXgV17Dyh0EOPA=\n-----END CERTIFICATE REQUEST-----"
    }
#### 2.2: Emitir el Certificado
Usa el archivo csr.json generado para emitir el certificado:

    
    curl --location --request POST 'http://localhost:8000/crypto/crt' \
    --header 'X-API-Key: 9ddaa525-bfc2-4f74-92e0-43b7a028aee1' \
    --header 'Content-Type: application/json' \
    --data @csr.json
### Paso 3: Validar un Certificado
#### 3.1: Guardar el Certificado Emitido
Pega la respuesta del comando anterior en un archivo llamado crt.json. El contenido del archivo será algo similar a esto:


    {
        "crt": "-----BEGIN CERTIFICATE-----\nMIIB8TCCAVmgAwIBAgI...\n-----END CERTIFICATE-----"
    }
#### 3.2: Validar el Certificado
Usa el siguiente comando curl para validar el certificado:


    curl --location --request POST 'http://localhost:8000/crypto/validate' \
    --header 'X-API-Key: 9ddaa525-bfc2-4f74-92e0-43b7a028aee1' \
    --header 'Content-Type: application/json' \
    --data @crt.json