import express from 'express';
import { inspect } from 'util';
import { exec } from 'child_process';
import TelegramApi from './TelegramApi';
import createCert from './createCert';
import FileDatabase from './FileDatabase';
import fs from 'fs';
import https from 'https';

const token = process.env.TELEGRAM_BOT_TOKEN;
const port = process.env.WEBHOOK_PORT;
const url = process.env.WEBHOOK_URL;
const dbUrl = process.env.IBM_SQL_URL;
const adminId = process.env.TELEGRAM_ADMIN_ID;



if (token) {
  console.debug(`TOKEN: ${token}`)
} else {
  console.error("Set your Bot token with\n\n  TELEGRAM_BOT_TOKEN = ads:ASD \n\n ");
}

const api = new TelegramApi(token);
const app = express();
const certs = createCert("jj22.de");

api.sendMessage(adminId, "hi")

fs.writeFileSync('./public.pem', certs.public);
api.setWebhook("jj22.de").catch(console.error)
// const db = new FileDatabase(dbUrl);




export function devInit() {
  if (adminId) {
    console.debug(`ADMIN: ${adminId}`)
  } else {
    console.info("Set a communication id with\n\n    TELEGRAM_ADMIN_ID = 12345\n\n");
  }
  app.get('/', (req, res) => {
    const msg = req.query.msg;
    console.log(String(msg));
    res.send(`<html><body><input id='i'> as ${adminId}</input></body><script>document.getElementById('i').addEventListener('keyup', ev => {if (ev.key === 'Enter') {fetch('?msg='+ev.target.value); ev.target.value=''}});</script></html>`);
    //TODO remove start
    if (msg) {
      api.sendMessage(adminId, String(msg)).catch(console.error);
    }
    //TODO remove end
  });
}


app.post('/', (req, res) => {
  api.sendMessage(adminId, "post").catch(console.error);
  console.log(`api.sendMessage(${adminId}, ${inspect(req)})`)
  api.sendMessage(adminId, inspect(req, true, 2)).catch(console.error);
  res.send("");
})

app.listen(port, () => {
  console.log(`Express server listening on port ${port}`);
});