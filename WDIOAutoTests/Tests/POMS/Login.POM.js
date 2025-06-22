import { $, $$ } from "@wdio/globals";

class Login {
  // Form Inputs
  // -----------------------------------------------

  /**
   * @description Returns the username input
   * @readonly
   * @returns {Promise<WebdriverIO.Element>} input
   */
  get usernameInput() {
    return $(`//input[@id="username"]`);
  }

  /**
   * @description Returns the password input
   * @readonly
   * @returns {Promise<WebdriverIO.Element>} input
   */
  get passwordInput() {
    return $(`//input[@id="password"]`);
  }

  /**
   * @description Returns the login button
   * @readonly
   * @returns {Promise<WebdriverIO.Element>} button
   */
  get loginButton() {
    return $(`//i[text()=" Login"]//parent::button`);
  }
  // -----------------------------------------------
  // END - Form Inputs

  // Flash Messages
  // -----------------------------------------------

  /**
   * @description Returns the flash message that indicates an invalid username.
   * @readonly
   * @returns {Promise<WebdriverIO.Element>} div
   */
  get invalidUsernameMessage() {
    return $(`//div[contains(text(),"Your username is invalid!")]`);
  }

  /**
   * @description Returns the flash message that indicates an invalid password.
   * @readonly
   * @returns {Promise<WebdriverIO.Element>} div
   */
  get invalidPasswordMessage() {
    return $(`//div[contains(text(),"Your password is invalid!")]`);
  }

  /**
   * @description Returns the flash message that indicates a successfull login.
   * @readonly
   * @returns {Promise<WebdriverIO.Element>} div
   */
  get successfullLoginMessage() {
    return $(`//div[contains(text(),"You logged into a secure area!")]`);
  }
  // -----------------------------------------------
  // END - Flash Messages

  // Secure Area Buttons
  // -----------------------------------------------

  /**
   * @description Returns the logout button
   * @readonly
   * @returns {Promise<WebdriverIO.Element>} a
   */
  get logoutButton() {
    return $(`//a[@href="/logout"]`);
  }
}

export default new Login();
