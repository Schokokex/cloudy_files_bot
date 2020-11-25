import express from 'express';
const app = express();
const port = 8080;


export function devInit(){
  console.info("Set a communication id with\n\n    TELEGRAM_ADMIN_ID = 12345\n\n");
  app.get('/', (req, res) => {
    const msg = req.query.msg;
    res.send("<html><body><input id='i'/></body><script>document.getElementById('i').addEventListener('keyup', ev => {if (ev.key === 'Enter') {fetch('?msg='+ev.target.value); ev.target.value=''}});</script></html>");
  });
}


app.post('/', (req, res) => {
  res.send("");
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
