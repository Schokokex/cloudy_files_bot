import selfsigned from 'selfsigned';
export default function createCert(url){
    return selfsigned.generate([{ name: "commonName", value: url },{ name: "countryName", value: "DE" }], { keySize: 2048, algorithm: 'sha256',   pkcs7: true, days: 365 });
}