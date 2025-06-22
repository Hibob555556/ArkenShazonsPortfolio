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

    get invalidUsernameMessage () {
        return $(``);
    }
}

export default new Login();