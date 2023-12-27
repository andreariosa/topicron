const app = require("express")();
const server = require("http").createServer(app);
const path = require("path");
const port = 3000;

// From Express.js 4.x. documentation:
// The http module is no longer needed, unless you need to directly work with it (socket.io/SPDY/HTTPS).
const io = require("socket.io")(server);
const scraper = require("./scraper");

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "/index.html"));
});

app.use((req, res, next) => {
  res.status(404).send("Sorry can't find that!");
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Something broke!");
});

io.on("connection", async (socket) => {
  await scraper.open();
  await scraper.runEvents(socket);
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
