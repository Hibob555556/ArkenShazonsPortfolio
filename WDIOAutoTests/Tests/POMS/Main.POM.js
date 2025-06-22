export default class Page {
  async open(path) {
    await browser.url(`https://the-internet.herokuapp.com/${path}`);
  }

  /**
   * @description Checks the url of the page to see if it is correct.
   * @param {String} path
   * @returns {Promise<Boolean>} true/false
   */
  async verifyURL(path) {
    if (
      (await browser.getUrl()) == `https://the-internet.herokuapp.com/${path}`
    )
      return true;
    return false;
  }
}
