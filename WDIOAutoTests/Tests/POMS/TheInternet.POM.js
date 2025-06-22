import { $, $$ } from "@wdio/globals";
import Page from "./Main.POM.js";

// create POM class
class TheInternet extends Page {
  // functions
  // ----------------------------------
  /**
   * @description load the internet to a specific page
   * @example await loadPage("login");
   * @param {String} path
   */
  async loadPage(path) {
    await super.open(path);
  }

  /**
   * @description Returns true/false indicating if your page is loaded
   * @param {String} path
   * @returns {Promise<Boolean>}
   */
  async checkPageLoaded(path) {
    return await super.verifyURL(path);
  }
  // ----------------------------------
}

export default new TheInternet();
