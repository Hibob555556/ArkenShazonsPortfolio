// import needed deps
import TheInternet from "../POMS/TheInternet.POM.js";
import Login from "../POMS/Login.POM.js";

// normally information like this should be kept in a .env file
// for this example they are hard coded so that we are not 
// uploading a .env file to the repo (that's bad practice)
const user = "tomsmith";
const pass = "SuperSecretPassword";
const url  = "login"

describe("The Internet", async () => {
  it("Should load the login page", async () => {
    // open the page
    await TheInternet.open(url);
    // check that the page loaded
    await expect(await TheInternet.checkPageLoaded(url)).toBeTruthy();
  });

  it("Should not allow login with an invalid username", async () => {
    await (await Login.usernameInput).setValue("BAD_USER");
    await (await Login.passwordInput).setValue(pass);
    await (await Login.loginButton).click();
  });
});