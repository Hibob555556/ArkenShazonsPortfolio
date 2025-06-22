// import needed deps
import TheInternet from "../POMS/TheInternet.POM.js";
import Login from "../POMS/Login.POM.js";

// normally information like this should be kept in a .env file
// for this example they are hard coded so that we are not
// uploading a .env file to the repo (that's bad practice)
const user   = "tomsmith";
const pass   = "SuperSecretPassword!";

// declare consts to be used in the file that should be able to be easily changed
const url    = "login";
const secUrl = "secure"

describe("The Internet", async () => {
  it("Step 1 | Should load the login page", async () => {
    // open the page
    await TheInternet.open(url);

    // check that the page loaded
    await expect(await TheInternet.checkPageLoaded(url)).toBeTruthy();
  });

  it("Step 2 | Should not allow login with an invalid username", async () => {
    // set the username and password
    await (await Login.usernameInput).setValue("BAD_USER");
    await (await Login.passwordInput).setValue(pass);

    // click the login button
    await (await Login.loginButton).click();

    // check that the invalid username message is displayed
    await expect(await Login.invalidUsernameMessage).toBeDisplayedInViewport();
  });

  it("Step 3 | Should not allow login with an invalid password", async () => {
    // set the username and password 
    await (await Login.usernameInput).setValue(user);
    await (await Login.passwordInput).setValue("BAD_PASS");

    // click the login button
    await (await Login.loginButton).click();

    // check that the invalid password message is displayed
    await expect(await Login.invalidPasswordMessage).toBeDisplayedInViewport();
  });

  it("Step 4 | Should not allow login with invalid credentials", async () => {
    // set the username and password
    await (await Login.usernameInput).setValue("BAD_USER");
    await (await Login.passwordInput).setValue("BAD_PASS");

    // click the login button
    await (await Login.loginButton).click();

    // check that the invalid username message is displayed
    await expect(await Login.invalidUsernameMessage).toBeDisplayedInViewport();
  });

  it("Step 5 | Should allow login with valid credentials", async () => {
    // set the username and password
    await (await Login.usernameInput).setValue(user);
    await (await Login.passwordInput).setValue(pass);

    // click the login button
    await (await Login.loginButton).click();

    // check that the successfull login message is displayed
    await expect(await Login.successfullLoginMessage).toBeDisplayedInViewport();

    // check that the correct page is loaded
    await expect(await TheInternet.checkPageLoaded(secUrl)).toBeTruthy();
  });
});
