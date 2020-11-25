import express from 'express';
const app = express();
const port = 8080;

if ('development' === app.get('env')) {
  app.get('/', (req, res) => {
    console.log(req);
    res.send("<html><body><input id='i'/></body><script>document.getElementById('i').addEventListener('keyup', ev => {if (ev.key === 'Enter') {fetch('?msg='+ev.target.value); ev.target.value=''}});</script></html>");
  })
}
// else process.env.NODE_ENV = 'production';


app.post('/', (req, res) => {
  res.send("");
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
