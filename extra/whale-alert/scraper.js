const puppeteer = require("puppeteer");

let browser, page;

const scraper = {
  async open() {
    browser = await puppeteer.launch({ headless: "new" });
    page = await browser.newPage();

    await page.goto("https://whale-alert.io");
    await page.waitForSelector("#term-container", { timeout: 0 }).then(() => {
      console.log("Ready for scraping");
    });
  },
  async runEvents(socket) {
    // https://pptr.dev/api/puppeteer.page.exposefunction
    await page.exposeFunction("emitter", (...data) => {
      socket.emit(...data);
    });

    await page.evaluate(() => {
      var targetNode = document.querySelector("#term-container");

      // https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver
      var observer = new MutationObserver(function (mutations) {
        // Trigger this event whenever there is a change
        emitter("refresh", targetNode.innerText);
      });

      var config = {
        attributes: true,
        childList: true,
        characterData: true,
        subtree: true,
      };

      observer.observe(targetNode, config);
    });
  },
};

module.exports = scraper;
