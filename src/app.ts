import express from 'express';
import TelegramApi from './TelegramApi';
import FileDatabase from './FileDatabase';


const app = express();
const port = 8080;
const token = process.env.TELEGRAM_BOT_TOKEN;
const dbUrl = process.env.IBM_SQL_URL;

if (process.env.TELEGRAM_BOT_TOKEN) {
  console.debug(`TOKEN: ${process.env.TELEGRAM_BOT_TOKEN}`)
} else {
  console.error("Set your Bot token with\n\n  TELEGRAM_BOT_TOKEN = ads:ASD \n\n ");
}
const api = new TelegramApi(token);
const db = new FileDatabase(dbUrl);

const adminId = process.env.TELEGRAM_ADMIN_ID;


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
    if (msg){
      api.sendMessage(adminId, String(msg));
    }
    //TODO remove end
  });
}


app.post('/', (req, res) => {
  api.sendMessage(adminId, String(req));
  res.send("");
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
