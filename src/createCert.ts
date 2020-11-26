import selfsigned from 'selfsigned';
export default function createCert(url){
    return selfsigned.generate([{ name: "commonName", value: url }], { days: 365 });
}