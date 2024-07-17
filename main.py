# Importa FastAPI para crear la aplicación web y HTTPException para manejar errores.
# Request y Depends son utilizados para la gestión de dependencias y el acceso a los datos de la solicitud.
from fastapi import FastAPI, HTTPException, Request, Depends
# Importa APIKeyHeader para manejar la autenticación basada en la clave API.
from fastapi.security.api_key import APIKeyHeader
# Importa BaseModel de Pydantic para definir modelos de datos utilizados en las solicitudes y respuestas.
from pydantic import BaseModel
# Importa módulos de criptografía necesarios para trabajar con certificados x509 y OID (Object Identifier).
from cryptography import x509
from cryptography.x509.oid import NameOID
# Importa el módulo RSA para generar claves asimétricas.
from cryptography.hazmat.primitives.asymmetric import rsa
# Importa módulos para la serialización de claves y generación de hashes.
from cryptography.hazmat.primitives import serialization, hashes
# Importa el esquema de padding PKCS1v15 para las operaciones de firma.
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
# Importa el backend de criptografía predeterminado.
from cryptography.hazmat.backends import default_backend
# Importa módulos de fecha y hora para manejar la validez de los certificados.
from datetime import datetime, timedelta


app = FastAPI()

API_KEY = "9ddaa525-bfc2-4f74-92e0-43b7a028aee1"

# Configura la autenticación de la API Key utilizando el encabezado HTTP 'X-API-Key'.
api_key_header = APIKeyHeader(name="X-API-Key")

# Inicializa variables globales para almacenar la clave privada y el certificado de la CA.
ca_private_key = None
ca_certificate = None

# Define un modelo de datos para las solicitudes de generación de certificados de la CA que contiene el campo 'common_name'.
class CommonNameRequest(BaseModel):
    common_name: str

# Define un modelo de datos para las solicitudes de emisión de certificados que contiene el campo 'csr'.
class CSRRequest(BaseModel):
    csr: str
# Define un modelo de datos para las solicitudes de validación de certificados que contiene el campo 'crt'.
class CertificateRequest(BaseModel):
    crt: str

def GenerateCACertificate(commonName):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
        
    )
        # Genera una clave privada RSA de 2048 bits.

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, commonName),
    ])
        # Define el nombre del sujeto y del emisor del certificado utilizando el 'commonName' proporcionado.

    certificate = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(private_key, hashes.SHA256(), default_backend())
        # Construye y firma el certificado de la CA.
    return private_key, certificate
        # Devuelve la clave privada y el certificado.


def IssueCertificate(csr, ca_private_key, ca_certificate):
    certificate = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca_certificate.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(ca_private_key, hashes.SHA256(), default_backend())
        # Construye y firma un nuevo certificado utilizando la CA.
    return certificate
        # Devuelve el certificado emitido.


def ValidateCertificate(cert, ca_certificate):
    try:
        ca_public_key = ca_certificate.public_key()
        ca_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            PKCS1v15(),
            cert.signature_hash_algorithm,
        )
                # Verifica la firma del certificado utilizando la clave pública de la CA.
        return True
    except Exception as e:
        return False
            # Devuelve True si el certificado es válido, de lo contrario False.

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return api_key_header
        # Verifica la clave API proporcionada en el encabezado de la solicitud.


@app.post("/crypto/ca")
async def generate_ca_certificate(request: CommonNameRequest, api_key: str = Depends(get_api_key)):
    global ca_private_key, ca_certificate
    common_name = request.common_name
    ca_private_key, ca_certificate = GenerateCACertificate(common_name)
    cert_pem = ca_certificate.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    return {"cert": cert_pem}
        # Endpoint para generar el certificado de la CA. Requiere autenticación por API key.


@app.post("/crypto/crt")
async def issue_certificate(request: CSRRequest, api_key: str = Depends(get_api_key)):
    global ca_private_key, ca_certificate
    csr_pem = request.csr
    csr = x509.load_pem_x509_csr(csr_pem.encode('utf-8'), default_backend())
    certificate = IssueCertificate(csr, ca_private_key, ca_certificate)
    cert_pem = certificate.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    return {"crt": cert_pem}
        # Endpoint para emitir un certificado utilizando un CSR. Requiere autenticación por API key.


@app.post("/crypto/validate")
async def validate_certificate(request: CertificateRequest, api_key: str = Depends(get_api_key)):
    global ca_certificate
    cert_pem = request.crt
    cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())
    valid = ValidateCertificate(cert, ca_certificate)
    return {"valid": valid}
        # Endpoint para validar un certificado. Requiere autenticación por API key.


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # Inicia el servidor FastAPI utilizando Uvicorn.
