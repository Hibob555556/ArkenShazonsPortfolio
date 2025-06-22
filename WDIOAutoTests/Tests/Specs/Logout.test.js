// import needed deps
import Login from "../POMS/Login.POM.js";

// declare consts
const url = "login";

describe("The Internet", async () => {
  it("Step 1 | Should allow logout", async () => {
    // logout
    await (await Login.logoutButton).click();

    // check that the login page is loaded
    await expect(await TheInternet.checkPageLoaded(url)).toBeTruthy();
  });
});
