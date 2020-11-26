import selfsigned from 'selfsigned';
export default function createCert(name, address){
    return selfsigned.generate([{ name: name, value: address }], { days: 365 });
}