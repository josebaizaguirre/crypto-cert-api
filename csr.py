from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import json

# Generar clave privada del cliente
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
# Genera una clave privada RSA con un exponente público de 65537 y un tamaño de 2048 bits.

# Generar CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mydomain.com"),
])).sign(private_key, hashes.SHA256(), default_backend())
# Crea una solicitud de firma de certificado (CSR) con los atributos definidos y la firma con la clave privada utilizando el algoritmo SHA256.

# Convertir el CSR a formato PEM
csr_pem = csr.public_bytes(serialization.Encoding.PEM).decode('utf-8')
# Convierte la CSR a formato PEM (base64) y la decodifica a una cadena de texto.

print(csr_pem)
# Imprime la CSR en formato PEM.

# Guardar CSR en un archivo JSON
csr_data = {
    "csr": csr_pem
}
# Crea un diccionario con el CSR en formato PEM.

with open("csr.json", "w") as f:
    json.dump(csr_data, f, indent=4)
# Abre (o crea) un archivo llamado "csr.json" en modo escritura y guarda el diccionario CSR en formato JSON con una indentación de 4 espacios.

print("CSR guardado en csr.json")
